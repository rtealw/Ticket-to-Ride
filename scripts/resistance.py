import numpy as np
from numpy import linalg
from termcolor import colored

test_matrix = np.array([[0,2,0,0,0,0],
                        [2,0,1,0,0,0],
                        [0,1,0,1,1,0],
                        [0,0,1,0,0,1],
                        [0,0,1,0,0,1],
                        [0,0,0,1,1,0]])

def generate_laplacian(array):
  dimension = len(array)
  laplacian = np.zeros((dimension, dimension))
  for row_index in range(dimension):
    laplacian[row_index, row_index] = np.sum(array[row_index])
  return laplacian - array

def ellens_resistance(laplacian, vertex_i, vertex_j):
  # https://www.nas.ewi.tudelft.nl/people/Piet/papers/LAA_2011_EffectiveResistance.pdf
  dimension = len(laplacian)
  e = np.zeros(dimension)
  e[vertex_i] = 1
  e[vertex_j] = -1
  laplacian_inverse = linalg.pinv(laplacian)
  resistance = np.matmul(e, laplacian_inverse)
  resistance = np.matmul(resistance, e)
  return np.round(resistance, 10)

def wu_resistance(laplacian, vertex_i, vertex_j):
  # https://arxiv.org/pdf/math-ph/0402038.pdf
  resistance = 0
  eigen_values = linalg.eig(laplacian)[0]
  eigen_vectors = linalg.eig(laplacian)[1]
  num_eigen = len(eigen_values)
  for index in range(num_eigen):
    eigen_value = eigen_values[index]
    eigen_vector = np.transpose(eigen_vectors)[index]
    if eigen_value > 0:
      resistance += (eigen_vector[vertex_i] - eigen_vector[vertex_j]) ** 2 / eigen_value
  return np.round(resistance, 10)

def find_resistance(array, vertex_i, vertex_j):
  laplacian = generate_laplacian(array)
  ellens_res = ellens_resistance(laplacian, vertex_i, vertex_j)
  wu_res = wu_resistance(laplacian, vertex_i, vertex_j)
  if ellens_res != wu_res:
    print("Resistances are not equal: ")
    print(ellens_res)
    print(wu_res)
  return ellens_res

if __name__ == '__main__':
    print("Running tests...", end=" ")
    test_result = find_resistance(test_matrix, 1, 3)
    if test_result == 1.75:
      print(colored("Success!", 'green'))
    else:
      print(colored("Failure :(", 'red'))
        