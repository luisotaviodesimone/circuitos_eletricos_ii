import os
import trab2luisotaviodesimone as t2
import lotdsread

dir_name = f'{os.getcwd()}/netlists/'
params_file = open(f'{dir_name}ParametrosEntradaMain.txt', 'r')
for params in params_file.readlines():
  if lotdsread.should_ignore_line(params):
    continue
  t2.main(f'{os.getcwd()}\\netlists\\netlistAC1.txt','AC',[1], [0.01, 100, 100], False)


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