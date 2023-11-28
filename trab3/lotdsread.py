import numpy as np
import lotdsstamp


def should_ignore_line(line: str) -> bool:
    return ["*", " ", "", "\n"].count(line[0]) > 0


def read_file(
    filepath: str,
    g_matrix: np.ndarray,
    i_matrix: np.ndarray,
    circuit_current_type: str,
    omega: float = 0,
    v_matrix_0: np.ndarray = np.array([]),
    time: float = 0,
    step: float = 0,
    it0: float = 0,
):
    with open(filepath) as f:
        for line in f:
            if should_ignore_line(line):
                continue
            elif line.startswith("R"):
                g_matrix = lotdsstamp.resistence(line, g_matrix)
            elif line.startswith("C"):
                g_matrix, i_matrix, it0 = lotdsstamp.capacitor(
                    line,
                    g_matrix,
                    i_matrix,
                    omega,
                    circuit_current_type,
                    step,
                    v_matrix_0,
                    it0,
                )
            elif line.startswith("L"):
                g_matrix, i_matrix, it0 = lotdsstamp.inductor(
                    line,
                    g_matrix,
                    i_matrix,
                    omega,
                    circuit_current_type,
                    step,
                    it0,
                    v_matrix_0,
                )
            elif line.startswith("I"):
                i_matrix = lotdsstamp.current_source(
                    line, i_matrix, circuit_current_type, time
                )
            elif line.startswith("V"):
                g_matrix, i_matrix = lotdsstamp.voltage_source(
                    line, g_matrix, i_matrix, circuit_current_type, time
                )
            elif line.startswith("G"):
                g_matrix = lotdsstamp.voltage_controlled_current_source(line, g_matrix)
            elif line.startswith("H"):
                g_matrix, i_matrix = lotdsstamp.current_controlled_voltage_source(
                    line, g_matrix, i_matrix
                )
            elif line.startswith("E"):
                g_matrix, i_matrix = lotdsstamp.voltage_controlled_voltage_source(
                    line, g_matrix, i_matrix
                )
            elif line.startswith("F"):
                g_matrix, i_matrix = lotdsstamp.current_controlled_current_source(
                    line, g_matrix, i_matrix
                )
            elif line.startswith("K"):
                g_matrix, i_matrix = lotdsstamp.transformer(
                    line, g_matrix, i_matrix, omega
                )
            elif line.startswith("D"):
                g_matrix, i_matrix = lotdsstamp.diode(
                    line,
                    g_matrix,
                    i_matrix,
                    v_matrix_0,
                    omega,
                    time,
                    circuit_current_type,
                )
            else:
                raise Exception("Not known component")

    return g_matrix, i_matrix, it0
