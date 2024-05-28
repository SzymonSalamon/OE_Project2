import random
import config


def individual(icls):
    genome = list()
    for x in range(0, 40):
        genome.append(random.randint(0, 1))
    return icls(genome)


def decodeInd(individual):
    a, b, n = config.a, config.b, config.len_genome
    decoded_values = []
    for i in range(0, len(individual), n):
        chromo = individual[i:i + n]
        binary_num_str = ''.join(map(str, chromo))
        decimal_num = int(binary_num_str, 2)
        decoded_value = a + decimal_num * (b - a) / (2 ** n - 1)
        decoded_values.append(decoded_value)
    return decoded_values


def fitness_function_h(individual):
    ind = decodeInd(individual)
    result = hyperellipsoid(ind)
    return result,

def fitness_function_d(individual):
    ind = decodeInd(individual)
    result = discus(ind)
    return result,

def fitness_function_h_r(individual):
    result = hyperellipsoid(individual)
    return result,

def fitness_function_d_r(individual):
    result = discus(individual)
    return result,


def hyperellipsoid(individual):
    n = len(individual)
    suma = 0
    for i in range(n):
        for j in range(i + 1):
            suma += (individual[j] ** 2)
    return suma


def discus(individual):
    n = len(individual)
    suma = 0
    for i in range(1, n):
        suma = suma + individual[i] ** 2
    return individual[0] ** 2 + (10 ** 6) * suma

