from re import I
import numpy as np

# NOTE: Ask how the modified stamps should be done


def current_source(line: str, I_matrix: np.ndarray):
    [name, drain_node, inject_node, current_type, value_or_amp, *phase] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    value_or_amp = float(value_or_amp)

    if len(phase) == 0:
        phase = 0
    else:
        phase = float(phase[0])

    insertion = value_or_amp * np.exp(1j * phase)

    I_matrix[drain_node, 0] -= insertion
    I_matrix[inject_node, 0] += insertion

    return I_matrix


def voltage_source(line: str, G_matrix: np.ndarray, I_matrix: np.ndarray):
    [name, drain_node, inject_node, current_type, value_or_amp, *phase] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    value_or_amp = float(value_or_amp)

    if len(phase) == 0:
        phase = 0
    else:
        phase = float(phase[0])

    insertion = value_or_amp * np.exp(1j * phase)

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
    value = int(value)

    insertion = 1 / value

    G_matrix[from_node, from_node] += insertion
    G_matrix[from_node, to_node] -= insertion
    G_matrix[to_node, from_node] -= insertion
    G_matrix[to_node, to_node] += insertion

    return G_matrix


def capacitor(line: str, G_matrix: np.ndarray, w: float):
    [name, from_node, to_node, value, *_] = line.split(" ")

    from_node = int(from_node)
    to_node = int(to_node)
    value = int(value)

    insertion = 1j * w * value

    G_matrix[from_node, from_node] += insertion
    G_matrix[from_node, to_node] -= insertion
    G_matrix[to_node, from_node] -= insertion
    G_matrix[to_node, to_node] += insertion

    return G_matrix


def voltage_controlled_current_source(line: str, G_matrix: np.ndarray):
    [name, drain_node, inject_node, pos_control, neg_control, value, *_] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    pos_control = int(pos_control)
    neg_control = int(neg_control)
    value = int(value)

    G_matrix[drain_node, pos_control] += value
    G_matrix[drain_node, neg_control] -= value
    G_matrix[inject_node, pos_control] -= value
    G_matrix[inject_node, neg_control] += value

    return G_matrix

def current_controlled_current_source():
    pass


def inductor(line: str, G_matrix: np.ndarray, I_matrix: np.ndarray, w: float):
    [name, from_node, to_node, value, *_] = line.split(" ")
    from_node = int(from_node)
    to_node = int(to_node)
    value = float(value)

    i_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    i_column[from_node, 0] = 1
    i_column[to_node, 0] = -1

    G_matrix = np.c_[G_matrix, i_column]

    i_row = np.zeros((1, G_matrix.shape[1]), dtype=np.complex128)
    i_row[0, from_node] = -1
    i_row[0, to_node] = 1
    i_row[0, -1] = w * 1j * value

    G_matrix = np.r_[G_matrix, i_row]

    I_matrix = np.r_[I_matrix, np.zeros((1, 1))]

    return G_matrix, I_matrix


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
    # iab_column[-2] = w * 1j * inductor_value_1
    # iab_column[-1] = w * 1j * mutual_inductor_value

    icd_column = np.zeros((G_matrix.shape[0], 1), dtype=np.complex128)
    icd_column[from_node_2, 0] = 1
    icd_column[to_node_2, 0] = -1
    # icd_column[-2] = w * 1j * mutual_inductor_value
    # icd_column[-1] = w * 1j * inductor_value_2

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

    I_matrix = np.r_[I_matrix, np.zeros((2, 1))]

    return G_matrix, I_matrix
