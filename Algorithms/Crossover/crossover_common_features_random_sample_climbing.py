import random
import numpy as np

def f(x):
  return (x-1.) * (x-1.)
def decode(binary_num, a, b, n):
  """
    Funkcja dekodująca łańcuch binarny na wartość dziesiętną.
  """
  binary_num = ''.join(map(str, binary_num))
  decimal_num = int(binary_num, 2)
  return a + decimal_num * (b - a) / (2**n - 1)


def crossover_common_features_random_sample_climbing(Pula_rodzicow, alpha, beta, a, b, minim = False):

  """
    Powielanie z lokalnym dostrajaniem.
    Common Features/Random Sample Climbing Crossover.

    Funkcja wyliczająca potomka C krzyżując rodziców A i B
    używając powyższego operatora krzyżowania.


    :param n: Długość łańcucha binarnego.
    :param alpha: Liczba pętli zewnętrznych, określająca ile instancji V będzie poddawane losowym mutacjom.
    :param beta: Liczba pętli wewnętrznych, określająca ilu losowym mutacjom polegnie każda instancja V.
    :param a: Pierwsza, mniejsza liczba określająca dolną granicę zakresu w którym poszukiwane jest rozwiązanie.
    :param b: Druga, większa liczba określająca górną granicę zakresu w którym poszukiwane jest rozwiązanie.
    :param minim: Wartość typu bool określająca czy funkcja rozwiązuje problem minimalizacji.
                  Domyślnie ma wartość false - rozwiązywany jest problem maksymalizacji.
  """
  A, B = random.sample(Pula_rodzicow, 2)
  n = len(A)

  V = np.zeros(n, dtype = int)

  for i in range(n):
    if A[i] == B[i] == 1:
      V[i] = 1
  best = V.copy()

  for i in range(alpha):

    temp = V.copy()

    for j in range(beta):

      lambd = np.random.randint(1, n + 1)

      positions_to_mutate = np.random.choice(range(0, n), lambd, replace = False)

      for position in positions_to_mutate:
        temp[position] += 1
        temp[position] %= 2

      if minim:
        if f(decode(temp, a, b, n)) < f(decode(best, a, b, n)):
          best = temp.copy()

      elif f(decode(temp, a, b, n)) > f(decode(best, a, b, n)):
          best = temp.copy()
  return best