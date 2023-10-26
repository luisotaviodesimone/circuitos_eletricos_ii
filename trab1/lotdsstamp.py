import numpy as np


def current_source(line: str, matrix: np.ndarray):
    [name, drain_node, inject_node, current_type, value, *_] = line.split(" ")

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    value = int(value)

    matrix[drain_node, 0] -= int(value)
    matrix[inject_node, 0] += int(value)

    return matrix


def resistence(line: str, matrix: np.ndarray):
    [name, from_node, to_node, value, *_] = line.split(" ")

    from_node = int(from_node)
    to_node = int(to_node)
    value = int(value)

    matrix[from_node, from_node] += 1 / value
    matrix[from_node, to_node] -= 1 / value
    matrix[to_node, from_node] -= 1 / value
    matrix[to_node, to_node] += 1 / value

    return matrix


def controlled_voltage_source(line: str, matrix: np.ndarray):
    [name, drain_node, inject_node, pos_control, neg_control, value, *_] = line.split(
        " "
    )

    drain_node = int(drain_node)
    inject_node = int(inject_node)
    pos_control = int(pos_control)
    neg_control = int(neg_control)
    value = int(value)

    matrix[drain_node, pos_control] += value
    matrix[drain_node, neg_control] -= value
    matrix[inject_node, pos_control] -= value
    matrix[inject_node, neg_control] += value

    return matrix
