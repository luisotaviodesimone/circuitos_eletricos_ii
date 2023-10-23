import numpy as np
# from colorama import Fore, Style

color_dict = {
    "red": '\033[91m', # Fore.RED,
    "green": '\033[92m', # Fore.GREEN,
    "blue": '\033[94m',# Fore.BLUE,
    "reset": '\033[0m' # Style.RESET_ALL
}

def color(text, color):
  return f"{color_dict[color]}{text}{color_dict['reset']}"

def print_voltage_matrix(voltage_matrix: np.ndarray, filepath: str):

  print(f"\n{color('Printing from netlist', 'blue')} {color(filepath, 'red')}\n")

  print(f"{color('Voltage Matrix:', 'blue')}\n", voltage_matrix, "\n")
  for i in range(len(voltage_matrix)):
    print(f"\nNode {i + 1}: {color(voltage_matrix[i,0], 'green')} {color('V', 'blue')}\n")
