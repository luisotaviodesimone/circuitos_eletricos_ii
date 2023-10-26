import numpy as np
import lotdsstamp


def should_ignore_line(line: str) -> bool:
    return ["*", " ", "", "\n"].count(line[0]) > 0


def read_file(filepath: str, g_matrix: np.ndarray, i_matrix: np.ndarray):
    with open(filepath) as f:
        for line in f:
            if should_ignore_line(line):
                continue
            elif line.startswith("I"):
                i_matrix = lotdsstamp.current_source(line, i_matrix)
            elif line.startswith("R"):
                g_matrix = lotdsstamp.resistence(line, g_matrix)
            elif line.startswith("G"):
                g_matrix = lotdsstamp.controlled_voltage_source(line, g_matrix)
            else:
                raise Exception("Not known component")
    return g_matrix, i_matrix
