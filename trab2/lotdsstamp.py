import numpy as np

# NOTE: Ask how the modified stamps should be done

def current_source(line: str, I_matrix: np.ndarray):
  [name, drain_node, inject_node, current_type, value, *_] = line.split(' ')

  drain_node = int(drain_node)
  inject_node = int(inject_node)
  value = int(value)

  I_matrix[drain_node, 0] -= int(value)
  I_matrix[inject_node, 0] += int(value)

  return I_matrix

def voltage_source():
  pass

def resistence(line: str, G_matrix: np.ndarray):
  [name, from_node, to_node, value, *_] = line.split(' ')

  from_node = int(from_node)
  to_node = int(to_node)
  value = int(value)

  G_matrix[from_node,from_node] += 1/value
  G_matrix[from_node,to_node] -= 1/value
  G_matrix[to_node,from_node] -= 1/value
  G_matrix[to_node,to_node] += 1/value

  return G_matrix

def voltage_controlled_current_source(line: str, G_matrix: np.ndarray):
  [name, drain_node, inject_node, pos_control, neg_control, value, *_] = line.split(' ')

  drain_node = int(drain_node)
  inject_node = int(inject_node)
  pos_control = int(pos_control)
  neg_control = int(neg_control)
  value = int(value)

  G_matrix[drain_node, pos_control] += value
  G_matrix[drain_node, neg_control] -= value
  G_matrix[inject_node, pos_control] -= value
  G_matrix[inject_node, neg_control] += value

  return G_matrix

def current_controlled_current_source():
  pass

def inductor():
  pass

def transformer(line: str, G_matrix: np.ndarray, w: float):
  [name,
   from_node_1, to_node_1,
   from_node_2, to_node_2,
   inductor_value_1, inductor_value_2,
   mutual_inductor_value, *_] = line.split(' ')
  
  from_node_1 = int(from_node_1)
  to_node_1 = int(to_node_1)
  from_node_2 = int(from_node_2)
  to_node_2 = int(to_node_2)
  inductor_value_1 = int(inductor_value_1)
  inductor_value_2 = int(inductor_value_2)
  mutual_inductor_value = int(mutual_inductor_value)

  iab_column = np.zeros((G_matrix.shape[0] + 2, 1))
  iab_column[from_node_1, 0] = 1
  iab_column[to_node_1, 0] = -1

  iab_column[-2] = w*1j * inductor_value_1
  iab_column[-1] = w*1j * mutual_inductor_value

  icd_column = np.zeros((G_matrix.shape[0] + 2, 1))
  icd_column[from_node_2, 0] = 1
  icd_column[to_node_2, 0] = -1
  icd_column[-2] = w*1j * mutual_inductor_value
  icd_column[-1] = w*1j * inductor_value_2

  iab_row = np.zeros((1, G_matrix.shape[1]))
  iab_row[from_node_1] = -1
  iab_row[to_node_1] = 1

  icd_row = np.zeros((1, G_matrix.shape[1]))
  icd_row[from_node_2] = -1
  icd_row[to_node_2] = 1

  G_matrix = np.r_[G_matrix, iab_row, icd_row]
  G_matrix = np.c_[G_matrix, iab_column, icd_column]

  return G_matrix


def capacitor(line: str, G_matrix: np.ndarray, w: float):
  [name, from_node, to_node, value, *_] = line.split(' ')

  from_node = int(from_node)
  to_node = int(to_node)
  value = int(value)

  insertion = w * 1j * value

  G_matrix[from_node,from_node] += insertion
  G_matrix[from_node,to_node] -= insertion
  G_matrix[to_node,from_node] -= insertion
  G_matrix[to_node,to_node] += insertion

  return G_matrix
