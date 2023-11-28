import math
import numpy as np
from lotdsformatting import safe_list_get, color


def current_source(
    line: str,
    I_matrix: np.ndarray,
    circuit_current_type: str,
    time: float,
):
    [name, drain_node, inject_node, current_type, dc_value, *trans_params] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    dc_value = float(dc_value)
    amp = 0
    freq = 0
    phase = 0

    if (
        (circuit_current_type == "AC" and current_type == "DC")
        or (circuit_current_type == "DC" and current_type == "AC")
        or (circuit_current_type == "DC" and current_type == "SIN")
        or (circuit_current_type == "TRAN" and current_type == "DC")
        # or (circuit_current_type == "TRAN" and current_type == "AC")
    ):
        insertion = 0
    elif current_type == "SIN":
        [amp, freq, phase] = trans_params
        amp = float(amp)
        freq = float(freq)
        phase = float(phase)

        insertion = amp * math.cos(2 * math.pi * freq * time + phase * math.pi / 180)
    else:
        insertion = dc_value * np.exp(1j * phase)

    I_matrix[drain_node, 0] -= insertion
    I_matrix[inject_node, 0] += insertion

    return I_matrix


def voltage_source(
    line: str,
    G_matrix: np.ndarray,
    I_matrix: np.ndarray,
    circuit_current_type: str,
    time: float,
):
    [name, drain_node, inject_node, current_type, dc_value, *trans_params] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    dc_value = float(dc_value)

    amp = 0
    freq = 0
    phase = 0

    if current_type == "SIN":
        [amp, freq, phase] = trans_params
        amp = float(amp)
        freq = float(freq)
        phase = float(phase)

    if (
        (circuit_current_type == "AC" and current_type == "DC")
        or (circuit_current_type == "DC" and current_type == "AC")
        or (circuit_current_type == "DC" and current_type == "SIN")
        # or (circuit_current_type == "TRAN" and current_type == "DC")
        # or (circuit_current_type == "TRAN" and current_type == "AC")
    ):
        insertion = 0
    elif current_type == "DC":
        insertion = dc_value
    else:
        insertion = amp * math.cos(2 * math.pi * freq * time + phase * math.pi / 180)

    i_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    i_column[drain_node, 0] = 1
    i_column[inject_node, 0] = -1

    G_matrix = np.c_[G_matrix, i_column]

    i_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    i_row[0, drain_node] = -1
    i_row[0, inject_node] = 1

    G_matrix = np.r_[G_matrix, i_row]

    I_matrix = np.r_[I_matrix, np.array([[-insertion]])]

    return G_matrix, I_matrix


def resistence(line: str, G_matrix: np.ndarray):
    [name, from_node, to_node, value, *_] = line.split(" ")

    from_node = int(from_node)
    to_node = int(to_node)
    value = float(value)

    insertion = 1 / value

    G_matrix[from_node, from_node] += insertion
    G_matrix[from_node, to_node] -= insertion
    G_matrix[to_node, from_node] -= insertion
    G_matrix[to_node, to_node] += insertion

    return G_matrix


def capacitor(
    line: str,
    G_matrix: np.ndarray,
    I_matrix: np.ndarray,
    omega: float,
    circuit_current_type: str,
    step: float,
    V_matrix: np.ndarray,
    it0: float,
):
    [name, from_node, to_node, value, *_] = line.split(" ")

    from_node = int(from_node)
    to_node = int(to_node)
    value = float(value)

    if circuit_current_type != "TRAN":
        insertion = 1j * omega * value
        G_matrix[from_node, from_node] += insertion
        G_matrix[from_node, to_node] -= insertion
        G_matrix[to_node, from_node] -= insertion
        G_matrix[to_node, to_node] += insertion

        return G_matrix, I_matrix, 0

    else:
        insertion = step / (2 * value)

        G_matrix = resistence(f"R {from_node} {to_node} {insertion}", G_matrix)

        vt0 = V_matrix[from_node, -1] - V_matrix[to_node, -1]

        dc_current = ((2 * value) / step) * vt0.real + it0.real

        I_matrix = current_source(
            f"I {to_node} {from_node} DC {dc_current}",
            I_matrix,
            circuit_current_type,
            0,
        )

        previous_vt0 = safe_list_get(V_matrix, from_node, -2, 0)
        new_it0 = (2 * value / step) * (vt0 - previous_vt0) - it0

        return G_matrix, I_matrix, new_it0


def voltage_controlled_current_source(line: str, G_matrix: np.ndarray):
    [name, drain_node, inject_node, pos_control, neg_control, value, *_] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    pos_control = int(pos_control)
    neg_control = int(neg_control)
    value = float(value)

    G_matrix[drain_node, pos_control] += value
    G_matrix[drain_node, neg_control] -= value
    G_matrix[inject_node, pos_control] -= value
    G_matrix[inject_node, neg_control] += value

    return G_matrix


def current_controlled_current_source(
    line: str, G_matrix: np.ndarray, I_matrix: np.ndarray
):
    [
        name,
        drain_node,
        inject_node,
        drain_control_node,
        inject_control_node,
        value,
        *_,
    ] = line.split(" ")

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    drain_control_node = int(drain_control_node)
    inject_control_node = int(inject_control_node)
    value = float(value)

    i_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    i_column[drain_node, 0] = value
    i_column[inject_node, 0] = -value
    i_column[drain_control_node, 0] = 1
    i_column[inject_control_node, 0] = -1

    G_matrix = np.c_[G_matrix, i_column]

    i_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    i_row[0, drain_control_node] = -1
    i_row[0, inject_control_node] = 1

    G_matrix = np.r_[G_matrix, i_row]

    I_matrix = np.r_[I_matrix, np.zeros((1, 1), dtype=np.complex128)]

    return G_matrix, I_matrix


def current_controlled_voltage_source(
    line: str, G_matrix: np.ndarray, I_matrix: np.ndarray
):
    [
        name,
        pos_node,
        neg_node,
        from_control_node,
        to_control_node,
        value,
        *_,
    ] = line.split(" ")

    pos_node = int(pos_node)
    neg_node = int(neg_node)
    from_control_node = int(from_control_node)
    to_control_node = int(to_control_node)
    value = float(value)

    ix_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    ix_column[from_control_node, 0] = 1
    ix_column[to_control_node, 0] = -1

    iy_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    iy_column[pos_node, 0] = 1
    iy_column[neg_node, 0] = -1

    G_matrix = np.c_[G_matrix, ix_column, iy_column]

    ix_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    ix_row[0, from_control_node] = -1
    ix_row[0, to_control_node] = 1

    iy_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    iy_row[0, pos_node] = -1
    iy_row[0, neg_node] = 1
    iy_row[0, -2] = value

    G_matrix = np.r_[G_matrix, ix_row, iy_row]

    I_matrix = np.r_[I_matrix, np.zeros((2, 1), dtype=np.complex128)]

    return G_matrix, I_matrix


def voltage_controlled_voltage_source(
    line: str, G_matrix: np.ndarray, I_matrix: np.ndarray
):
    [
        name,
        pos_node,
        neg_node,
        pos_control_node,
        neg_control_node,
        value,
        *_,
    ] = line.split(" ")

    pos_node = int(pos_node)
    neg_node = int(neg_node)
    pos_control_node = int(pos_control_node)
    neg_control_node = int(neg_control_node)
    value = float(value)

    i_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    i_column[pos_node, 0] = 1
    i_column[neg_node, 0] = -1

    G_matrix = np.c_[G_matrix, i_column]

    i_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    i_row[0, pos_node] = -1
    i_row[0, neg_node] = 1
    i_row[0, pos_control_node] = value
    i_row[0, neg_control_node] = -value

    G_matrix = np.r_[G_matrix, i_row]

    I_matrix = np.r_[I_matrix, np.zeros((1, 1), dtype=np.complex128)]

    return G_matrix, I_matrix


def inductor(
    line: str,
    G_matrix: np.ndarray,
    I_matrix: np.ndarray,
    w: float,
    circuit_current_type: str,
    step: float,
    it0: float,
    V_matrix: np.ndarray,
):
    [name, from_node, to_node, value, *_] = line.split(" ")
    from_node = int(from_node)
    to_node = int(to_node)
    value = float(value)

    if circuit_current_type != "TRAN":
        i_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
        i_column[from_node, 0] = 1
        i_column[to_node, 0] = -1

        G_matrix = np.c_[G_matrix, i_column]

        i_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
        i_row[0, from_node] = -1
        i_row[0, to_node] = 1
        i_row[0, -1] = w * 1j * value

        G_matrix = np.r_[G_matrix, i_row]

        I_matrix = np.r_[I_matrix, np.zeros((1, 1), dtype=np.complex128)]

        return G_matrix, I_matrix, 0
    else:
        insertion = 2 * value / step

        G_matrix = resistence(f"R {from_node} {to_node} {insertion}", G_matrix)

        vt0 = V_matrix[from_node, -1] - V_matrix[to_node, -1]

        dc_current = ((step / (2 * value)) * vt0.real) + it0.real

        I_matrix = current_source(
            f"I {from_node} {to_node} DC {dc_current}",
            I_matrix,
            circuit_current_type,
            0,
        )

        previous_vt0 = safe_list_get(V_matrix, from_node, -2, 0)
        new_it0 = (2 * value / step) * (vt0 - previous_vt0) - it0

        return G_matrix, I_matrix, new_it0


def transformer(line: str, G_matrix: np.ndarray, I_matrix: np.ndarray, w: float):
    [
        name,
        from_node_1,
        to_node_1,
        from_node_2,
        to_node_2,
        inductor_value_1,
        inductor_value_2,
        mutual_inductor_value,
        *_,
    ] = line.split(" ")

    from_node_1 = int(from_node_1)
    to_node_1 = int(to_node_1)
    from_node_2 = int(from_node_2)
    to_node_2 = int(to_node_2)
    inductor_value_1 = float(inductor_value_1)
    inductor_value_2 = float(inductor_value_2)
    mutual_inductor_value = float(mutual_inductor_value)

    iab_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    iab_column[from_node_1, 0] = 1
    iab_column[to_node_1, 0] = -1

    icd_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    icd_column[from_node_2, 0] = 1
    icd_column[to_node_2, 0] = -1

    G_matrix = np.c_[G_matrix, iab_column, icd_column]

    iab_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    iab_row[0, from_node_1] = -1
    iab_row[0, to_node_1] = 1
    iab_row[0, -2] = w * 1j * inductor_value_1
    iab_row[0, -1] = w * 1j * mutual_inductor_value

    icd_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    icd_row[0, from_node_2] = -1
    icd_row[0, to_node_2] = 1
    icd_row[0, -2] = w * 1j * mutual_inductor_value
    icd_row[0, -1] = w * 1j * inductor_value_2

    G_matrix = np.r_[G_matrix, iab_row, icd_row]

    I_matrix = np.r_[I_matrix, np.zeros((2, 1), dtype=np.complex128)]

    return G_matrix, I_matrix


def diode(
    line: str,
    G_matrix: np.ndarray,
    I_matrix: np.ndarray,
    V_matrix: np.ndarray,
    omega: float,
    time: float,
    circuit_current_type: str,
):
    [name, pos_node, neg_node, Is, nVt, *_] = line.split(" ")

    pos_node = int(pos_node)
    neg_node = int(neg_node)
    Is = float(Is)
    nVt = float(nVt)

    where_to_get_tension_from = 0  # Because the tension in the node doesn't change
    if circuit_current_type == "TRAN":
        where_to_get_tension_from = (
            -1
        )  # Because the tension in the node is from the last round

    pos_node_tension = V_matrix[pos_node, where_to_get_tension_from]
    neg_node_tension = V_matrix[neg_node, where_to_get_tension_from]

    Vd = pos_node_tension.real - neg_node_tension.real

    if (pos_node_tension.real - neg_node_tension.real) > 1:
        Vd = 1

    elif (pos_node_tension.real - neg_node_tension.real) < -20:
        Vd = -20

    G0 = (Is * (math.e ** (Vd / nVt))) / nVt
    I0 = Is * (math.e ** (Vd / nVt) - 1) - G0 * Vd

    G_matrix = resistence(f"R {neg_node} {pos_node} {1/G0}", G_matrix)
    I_matrix = current_source(f"I {pos_node} {neg_node} DC {I0}", I_matrix, "DC", time)

    return G_matrix, I_matrix
