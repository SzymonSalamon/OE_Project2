def decodeInd(individual):
    global a, b, n
    a = -3
    b = 3
    n = 4
    decoded_values = []
    for i in range(0, len(individual), n):
        chromo = individual[i:i + n]
        binary_num_str = ''.join(map(str, chromo))
        decimal_num = int(binary_num_str, 2)
        decoded_value = a + decimal_num * (b - a) / (2 ** n - 1)
        decoded_values.append(decoded_value)
    return decoded_values

print(decodeInd([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]))

def fitness_function_h(individual):
  ind = decodeInd(individual)
  result = hyperellipsoid(ind)
  return result

def hyperellipsoid(individual):
   n = len(individual)
   suma = 0
   for i in range(n):
    for j in range(i + 1):
     suma += (individual[j] ** 2)
   return suma

print(fitness_function_h([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]))