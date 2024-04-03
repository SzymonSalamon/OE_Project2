import random
import numpy as np

def crossover_2nparent_parameter_wise(Pula_rodzicow, l=4, q=3):

  #wylosowanie l rodzicow
  M_pool = random.sample(Pula_rodzicow, l)
  Parameter_pool = [np.array_split(parent, q) for parent in M_pool]

  child_parameters = np.zeros((l, q), dtype=object)

  #funkcja krzyzowania jednopunktowego
  def crossover(vector1, vector2):
    crossover_point = np.random.randint(0, len(vector1))
    child = np.concatenate((vector1[:crossover_point], vector2[crossover_point:]))
    return child

  #Krzyzowanie jednpunktowe pomiedzy parametrami rodzicow
  for j in range(q):
    for i in range(l):
      m = np.random.randint(0, l-1)
      while m == i:
        m = np.random.randint(0, l-1)
      child_parameters[i][j] = crossover(Parameter_pool[i][j], Parameter_pool[m][j])

  #Tworzenie potomka z losowo wybranych parametrow
  children = []
  for i in range(l):
    child = np.array([])
    for j in range(q):
      z = np.random.randint(0, l-1)
      child = np.concatenate((child, child_parameters[z, j]))
    children.append(child.astype(int))
  return children