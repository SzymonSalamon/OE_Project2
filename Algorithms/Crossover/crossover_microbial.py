import random


def f(x):
  return (x-1.) * (x-1.)

def decode(binary_num, a, b, n):
  """
    Funkcja dekodująca łańcuch binarny na wartość dziesiętną.
  """
  binary_num = ''.join(map(str, binary_num))
  decimal_num = int(binary_num, 2)
  return a + decimal_num * (b - a) / (2**n - 1)

def crossover_microbial(M_pool):
  n = len(M_pool[0])

  A, B = random.sample(M_pool, 2)

  dlugosc_segmentu = random.randint(1, n-1)
  max_alfa = n - dlugosc_segmentu
  alfa = random.randint(0, max_alfa - 1)

  if f(decode(A, -10, 10, n)) >= f(decode(B, -10, 10, n)):
    for i in range(alfa, alfa + dlugosc_segmentu):
      B[i] = A[i]
  else:
    for i in range(alfa, alfa+dlugosc_segmentu):
      A[i] = B[i]
  return A, B