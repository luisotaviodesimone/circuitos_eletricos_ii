import os
import trab2luisotaviodesimone as t2
from plot import plot_bode_duo


def execute(netlist_file, current_type, desired_nodes, params, enable_print=False):
    frequencies, desired_nodes_modules, desired_nodes_phases = t2.main(
        f"{os.getcwd()}\\netlists\\{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    for i in range(len(desired_nodes)):
        plot_bode_duo(
            frequencies, desired_nodes_modules[i], desired_nodes_phases[i], netlist_file
        )


# execute("netlistAC1.txt", "AC", [1], [-2, 2, 100])  # AC1
# execute("netlistAC2.txt", "AC", [1], [-2, 2, 100])  # AC2
# execute("netlistAC3.txt", "AC", [2], [-2, 2, 100])  # AC3
# execute("netlistAC4.txt", "AC", [2, 3], [-2, 2, 100])  # AC4
# execute("netlistAC5.txt", "AC", [3], [-2, 2, 100])  # AC5
# TODO: Check why AC5 is not much similar to answer
execute("netlistAC6.txt", "AC", [2, 5], [-2, 2, 100])  # AC6


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
