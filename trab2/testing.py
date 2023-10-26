import os
import trab2luisotaviodesimone as t2
from plot import plot_bode_duo


def executeAC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    frequencies, desired_nodes_modules, desired_nodes_phases = t2.main(
        f"{os.getcwd()}\\netlists\\{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    for i in range(len(desired_nodes)):
        plot_bode_duo(
            frequencies,
            desired_nodes_modules[i],
            desired_nodes_phases[i],
            netlist_file,
            desired_nodes[i],
        )


def executeDC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    voltage_matrix = t2.main(
        f"{os.getcwd()}\\netlists\\{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    print("voltage_matrix", voltage_matrix, end="\n\n", sep="\n")

    return voltage_matrix


def alternated_current():
    executeAC("netlistAC1.txt", "AC", [1], [-2, 2, 100])  # AC1
    executeAC("netlistAC2.txt", "AC", [1], [-2, 2, 100])  # AC2
    executeAC("netlistAC3.txt", "AC", [2], [-2, 2, 100])  # AC3
    executeAC("netlistAC4.txt", "AC", [2, 3], [-2, 2, 100])  # AC4
    executeAC("netlistAC5.txt", "AC", [3], [-2, 2, 100])  # AC5
    executeAC("netlistAC6.txt", "AC", [2, 5], [-2, 2, 100])  # AC6
    executeAC("netlistAC7.txt", "AC", [2, 7], [-2, 2, 100])  # AC7
    executeAC("netlistAC9.txt", "AC", [2, 3, 4, 5, 6], [-2, 2, 100])  # AC9
    # TODO: AC8 is not working, either a ComplexWarning, RuntimeWarning, OverflowWarning or a Singular Matrix is happening
    executeAC("netlistAC8.txt", "AC", [4], [-2, 2, 100])  # AC8
    # TODO: AC10 is not working, either a ComplexWarning, RuntimeWarning, OverflowWarning or a Singular Matrix is happening
    executeAC("netlistAC10.txt", "AC", [4, 5], [0.01, 500, 1000])  # AC10


alternated_current()


def continuous_current():
    print(executeAC("netlistDC1.txt", "DC", [2], []) == [6.0])  # DC1
    print(
        executeAC("netlistDC2.txt", "DC", [2, 3, 5, 7, 9, 10], [])
        == [8, 1, 8.4, 0.93333333, -5.6, -3.73333333]
    )  # DC2


continuous_current()

"""
Params:
netlist_file: filename of the netlist file
current_type: 'DC' or 'AC'
desired_nodes: list of nodes to be printed
params: [initial_frequency, final_frequency, number_of_points_per_decade]
enable_print: print voltage matrix

Example call:
main('netlist1.txt', 'DC', [1,2], [])
main('netlist1.txt', 'AC', [1,2], [0.1,1e6, 100])
"""
