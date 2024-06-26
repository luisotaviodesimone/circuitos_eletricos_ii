import numpy as np
from lotdsformatting import color, print_voltage_matrix
import lotdsread
import sys


def create_g_matrix_and_i_matrix(filepath: str) -> (np.ndarray, np.ndarray):
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

    g_matrix = np.zeros((max_node + 1, max_node + 1))
    i_matrix = np.zeros((max_node + 1, 1))

    return g_matrix, i_matrix


def main(netlist_file: str, enable_print: bool = False) -> np.ndarray:
    g_matrix, i_matrix = create_g_matrix_and_i_matrix(netlist_file)

    mounted_g_matrix, mounted_i_matrix = lotdsread.read_file(
        netlist_file, g_matrix, i_matrix
    )

    mounted_g_matrix = mounted_g_matrix[1:, 1:]
    mounted_i_matrix = mounted_i_matrix[1:]

    voltage_matrix = np.linalg.solve(mounted_g_matrix, mounted_i_matrix)

    if enable_print:
        print_voltage_matrix(voltage_matrix, netlist_file)

    return voltage_matrix


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception(color("Please, provide a netlist file", "red"))

    netlist = f"./netlists/{sys.argv[1]}.txt"

    result = main(netlist)

    print(result)
