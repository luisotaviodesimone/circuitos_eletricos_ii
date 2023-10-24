import os

import numpy as np
import trab2luisotaviodesimone as t2
import lotdsread
from plot import plot_bode_duo, plot_bode_uni


# dir_name = f'{os.getcwd()}/netlists/'
# params_file = open(f'{dir_name}ParametrosEntradaMain.txt', 'r')
# for params in params_file.readlines():
#   if lotdsread.should_ignore_line(params):
#     continue

frequencies, desired_nodes_modules, desired_nodes_phases = t2.main(
    # (f'{os.getcwd()}\\netlists\\netlistAC1.txt','AC',[1], [-2, 2, 100], True) # AC1
    # f"{os.getcwd()}/netlists/netlistAC2.txt",
    # "AC",
    # [1],
    # [-2, 2, 100],
    # False  # AC2
    # f"{os.getcwd()}/netlists/netlistAC3.txt",
    # "AC",
    # [1, 2],
    # [-2, 2, 100],
    # False,  # AC3

    # f"{os.getcwd()}/netlists/netlistAC4.txt",
    # "AC",
    # [2, 3],
    # [-2, 2, 100],
    # False,  # AC4

    f"{os.getcwd()}/netlists/netlistAC5.txt",
    "AC",
    [3],
    [-2, 2, 100],
    False,  # AC5
)

for i in range(len([2, 3])):
    plot_bode_duo(frequencies, desired_nodes_modules[i], desired_nodes_phases[i])

# eval(execution)

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
