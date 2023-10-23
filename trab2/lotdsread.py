
import numpy as np
import lotdsstamp

def should_ignore_line(line: str) -> bool:
  return ['*', ' ', '', '\n'].count(line[0]) > 0

def read_file(filepath: str, g_matrix: np.ndarray, i_matrix: np.ndarray, w: float):
  with open(filepath) as f:
    for line in f:
      if should_ignore_line(line):
        continue
      elif line.startswith('I'):
        i_matrix = lotdsstamp.current_source(line, i_matrix)
      elif line.startswith('R'):
        g_matrix = lotdsstamp.resistence(line, g_matrix)
      elif line.startswith('G'):
        g_matrix = lotdsstamp.voltage_controlled_current_source(line, g_matrix)
      elif line.startswith('K'):
        g_matrix = lotdsstamp.transformer(line, g_matrix, w)
      elif line.startswith('C'):
        g_matrix = lotdsstamp.capacitor(line, g_matrix, w)
      else:
        raise Exception('Not known component')
  return g_matrix, i_matrix
