import os
import trab2luisotaviodesimone as t2
from plot import plot_bode_duo
import numpy as np


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

    return voltage_matrix


def alternated_current():
    executeAC('netlistAC1.txt','AC',[1], [0.01, 100, 100])  # AC1
    executeAC('netlistAC2.txt','AC',[1], [0.01, 200, 100])  # AC2
    executeAC('netlistAC3.txt','AC',[2], [0.01, 100, 100])  # AC3
    executeAC('netlistAC4.txt','AC',[2,3], [0.01, 500, 1000])  # AC4
    executeAC('netlistAC5.txt','AC',[3], [0.01, 1000, 1000])  # AC5
    executeAC('netlistAC6.txt','AC',[2,5], [0.01, 2e3, 1000])  # AC6
    executeAC('netlistAC7.txt','AC',[2,7], [0.01, 100, 1000])  # AC7
    executeAC('netlistAC8.txt','AC',[4], [100, 100e3, 100])  # AC9
    executeAC('netlistAC9.txt','AC',[2,3,4,5,6], [0.01, 100, 1000])  # AC8
    executeAC('netlistAC10.txt','AC',[4,5], [0.01, 500, 1000]) # AC10


def compareDC(execution, result):
    print(
        f"{execution} == {result} \n",
        np.allclose(execution, result, rtol=1e-03, atol=1e-03),
        "\n",
    )


def continuous_current():
    print("netlistDC1.txt")
    compareDC(executeDC("netlistDC1.txt", "DC", [2], []), [6.0])  # DC1
    print("netlistDC2.txt")
    compareDC(
        executeDC("netlistDC2.txt", "DC", [2, 3, 5, 7, 9, 10], []),
        [8, 1, 8.4, 0.93333333, -5.6, -3.73333333],
    )  # DC2
    print("netlistDC3.txt")
    compareDC(
        executeDC("netlistDC3.txt", "DC", [1, 2, 3, 4, 5, 6, 7], []),
        [10.0, 5.7554841, 2.49323451, 4.37608413, 2.28100871, 5.7554841, 6.37608413],
    )  # DC3
    print("netlistDC4.txt")
    compareDC(executeDC("netlistDC4.txt", "DC", [2], []), [6.0])
    print("netlistDC5.txt")
    compareDC(executeDC("netlistDC5.txt", "DC", [2], []), [10.0])
    print("netlistDC6.txt")
    compareDC(executeDC("netlistDC6.txt", "DC", [3, 4, 5], []), [0.5, 0, 0])


alternated_current()

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
