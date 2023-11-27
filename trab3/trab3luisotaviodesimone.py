from webbrowser import get
import numpy as np
from lotdsformatting import color, print_voltage_matrix, get_desired_nodes
import lotdsread
import sys
from typing import Tuple, Type


def create_g_matrix_and_i_matrix(filepath: str) -> Tuple[np.ndarray, np.ndarray, int]:
    max_node = 0

    with open(filepath) as f:
        for line in f:
            if lotdsread.should_ignore_line(line):
                continue

            _, node1, node2, *_ = line.split(" ")

            if int(node1) > max_node:
                max_node = int(node1)

            if int(node2) > max_node:
                max_node = int(node2)

    g_matrix = np.zeros((max_node + 1, max_node + 1), dtype=np.complex128)
    i_matrix = np.zeros((max_node + 1, 1), dtype=np.complex128)

    return g_matrix, i_matrix, max_node


def main(
    netlist_file: str,
    current_type: str,
    desired_nodes: list[int],
    params: list = [0, 0, 0],
    enable_print: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray] | np.ndarray:
    g_matrix, i_matrix, max_node = create_g_matrix_and_i_matrix(netlist_file)
    voltage_matrix_0 = np.array(params[1])[..., None]  # transpose array

    if current_type == "DC":
        tol = params[0]
        k = 0

        voltage_matrix = voltage_matrix_0
        while k < 100:
            mounted_g_matrix, mounted_i_matrix = lotdsread.read_file(
                netlist_file, g_matrix, i_matrix, current_type, 0, voltage_matrix_0
            )

            mounted_g_matrix = mounted_g_matrix[1:, 1:]
            mounted_i_matrix = mounted_i_matrix[1:]

            voltage_matrix = np.linalg.solve(mounted_g_matrix, mounted_i_matrix)

            print(voltage_matrix)

            if np.max(np.abs(voltage_matrix[:max_node] - voltage_matrix_0[1:])) < tol:
                break

            k += 1
            voltage_matrix_0 = np.vstack((np.array([0]), voltage_matrix[:max_node]))

        result = np.array([])
        for i in range(len(desired_nodes)):
            result = np.append(result, voltage_matrix[desired_nodes[i] - 1, 0].real)

        return result

    elif current_type == "TRAN":
        tol = params[0]

        k = 0
        voltage_matrix = voltage_matrix_0
        while k < 100:
            mounted_g_matrix, mounted_i_matrix = lotdsread.read_file(
                netlist_file, g_matrix, i_matrix, current_type, 0, voltage_matrix
            )

            mounted_g_matrix = mounted_g_matrix[1:, 1:]
            mounted_i_matrix = mounted_i_matrix[1:]

            voltage_matrix = np.linalg.solve(mounted_g_matrix, mounted_i_matrix)

            if np.max(np.abs(voltage_matrix - voltage_matrix_0)) < tol:
                break

            k += 1
            voltage_matrix_0 = np.vstack((np.array([0]), voltage_matrix))

        return voltage_matrix

    else:
        (start_point, end_point, number_of_points) = params
        frequencies = np.logspace(
            np.log10(start_point), np.log10(end_point), number_of_points
        )

        desired_voltage_modules = np.zeros(
            (len(desired_nodes), frequencies.shape[0]), dtype=np.complex128
        )
        desired_voltage_phases = np.zeros(
            (len(desired_nodes), frequencies.shape[0]), dtype=np.complex128
        )

        for i in range(len(frequencies)):
            g_matrix, i_matrix, max_node = create_g_matrix_and_i_matrix(netlist_file)

            omega = float(frequencies[i] * 2 * np.pi)

            mounted_g_matrix, mounted_i_matrix = lotdsread.read_file(
                netlist_file, g_matrix, i_matrix, current_type, omega
            )

            mounted_g_matrix = mounted_g_matrix[1:, 1:]
            mounted_i_matrix = mounted_i_matrix[1:]

            voltage_matrix = np.linalg.solve(mounted_g_matrix, mounted_i_matrix)

            for j in range(len(desired_nodes)):
                desired_voltage_modules[j, i] = 20 * np.log10(
                    np.abs(voltage_matrix[desired_nodes[j] - 1])
                )
                desired_voltage_phases[j, i] = np.degrees(
                    np.angle(voltage_matrix[desired_nodes[j] - 1])
                )
        return frequencies, desired_voltage_modules, desired_voltage_phases
