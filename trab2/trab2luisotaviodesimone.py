import math
import numpy as np
import sympy as sp
from lotdsformatting import color, print_voltage_matrix
import lotdsread
import sys

from typing import Tuple, Type

def create_g_matrix_and_i_matrix(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
  max_node = 0

  with open(filepath) as f:
    
    for line in f:
      if lotdsread.should_ignore_line(line):
        continue

      _, node1, node2, *_ = line.split(' ')
      
      if int(node1) > max_node:
        max_node = int(node1)
      
      if int(node2) > max_node:
        max_node = int(node2)

  g_matrix = np.zeros((max_node + 1, max_node + 1), dtype=np.complex128)
  i_matrix = np.zeros((max_node + 1, 1), dtype=np.complex128)

  return g_matrix, i_matrix

def main(netlist_file: str, current_type: str, desired_nodes: list[int], params: list = [0,0,0], enable_print: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

  g_matrix, i_matrix = create_g_matrix_and_i_matrix(netlist_file)

  if current_type == 'DC':
    mounted_g_matrix, mounted_i_matrix = lotdsread.read_file(netlist_file, g_matrix, i_matrix, params[0] * 2 * math.pi)

    mounted_g_matrix = mounted_g_matrix[1:,1:]
    mounted_i_matrix = mounted_i_matrix[1:]

    voltage_matrix = np.linalg.solve(mounted_g_matrix, mounted_i_matrix)

    if enable_print: print_voltage_matrix(voltage_matrix, netlist_file)

    return voltage_matrix, np.zeros(()), np.zeros(())

  else: # AC
    frequencies = np.logspace(params[0], params[1], params[2])

    voltage_modules = np.zeros(frequencies.shape)
    voltage_phases = np.zeros(frequencies.shape)

    for i in range(len(frequencies)):
      w = frequencies[i] * 2 * math.pi
      mounted_g_matrix, mounted_i_matrix = lotdsread.read_file(netlist_file, g_matrix, i_matrix, w)

      mounted_g_matrix = mounted_g_matrix[1:,1:]
      mounted_i_matrix = mounted_i_matrix[1:]

      voltage_matrix = np.linalg.solve(mounted_g_matrix, mounted_i_matrix)

      voltage_modules[i] = np.abs(voltage_matrix)
      voltage_phases[i] = np.degrees(np.angle(voltage_matrix))

      if enable_print: print_voltage_matrix(voltage_matrix, netlist_file)

    desired_nodes_modules = np.zeros((len(desired_nodes), len(frequencies)))
    desired_nodes_phases = np.zeros((len(desired_nodes), len(frequencies)))

    # TODO: check if this is correctly getting the desired nodes array of results
    for i in range(len(desired_nodes)):
      desired_nodes_modules[i] = np.array(voltage_modules[desired_nodes[i]-1])
      desired_nodes_phases[i] = np.array(voltage_phases[desired_nodes[i]-1])

    return frequencies, desired_nodes_modules, desired_nodes_phases

if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise Exception(color('Please, provide a netlist file', 'red'))

  netlist = f"./netlists/{sys.argv[1]}.txt"

  # result = main(netlist)

  # print(result)
