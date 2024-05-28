import random
import numpy as np

from projekt5 import decodeInd
import config


def cx_one_point(ind1, ind2):
    """
    Executes a one point crossover on the input :term:`sequence`
    individuals.
    The two individuals are modified in place. The resulting individuals
    will
    respectively have the length of the other.
    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    This function uses the :func:`~random.randint` function from the
    python base :mod:`random` module.
    """
    size = min(len(ind1), len(ind2))
    cxpoint = random.randint(1, size - 1)
    ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    return ind1, ind2


def crossover_onep(vector1, vector2):
    crossover_point = np.random.randint(0, len(vector1))
    child = np.concatenate((vector1[:crossover_point], vector2[crossover_point:]))
    return child


def crossover_2nparent_parameter_wise(parent1, parent2):
    l = 4
    q = 2
    Pula_rodzicow = [parent1, parent1, parent2, parent2]

    if len(Pula_rodzicow[0]) % q != 0:
        raise ValueError("Długość chromosomów rodziców musi byc podzielna przez q")

        # sprawdzenie, czy liczba rodziców jest mniejsza lub równa niż liczebność populacji
    if len(Pula_rodzicow) < l:
        raise ValueError("Liczba rodziców nie może być większa od liczebności populacji!")

        # wylosowanie l rodzicow
    M_pool = random.sample(Pula_rodzicow, l)
    Parameter_pool = [np.array_split(parent, q) for parent in M_pool]

    child_parameters = np.zeros((l, q), dtype=object)

    def crossover(vector1, vector2):
        crossover_point = np.random.randint(0, len(vector1))
        child = np.concatenate((vector1[:crossover_point], vector2[crossover_point:]))
        return child

    for j in range(q):
        for i in range(l):
            m = np.random.randint(0, l - 1)
            while m == i:
                m = np.random.randint(0, l - 1)
            child_parameters[i][j] = crossover(Parameter_pool[i][j], Parameter_pool[m][j])

    children = []
    for i in range(l):
        child = np.array([])
        for j in range(q):
            z = np.random.randint(0, l - 1)
            child = np.concatenate((child, child_parameters[z, j]))
        children.append(child.astype(int))
    return children[0], children[1]


def common_features_random_sample_climbing_crossover(parent1, parent2):
    A, B = parent1, parent2

    n = len(A)
    V = np.zeros(n, dtype=int)

    f, n = config.f, config.len_genome
    minim = config.minim

    alpha, beta = 5, 5

    for i in range(n):
        if A[i] == B[i] == 1:
            V[i] = 1

    best = V.copy()
    sec_best = V.copy()

    for i in range(alpha):

        temp = V.copy()

        for j in range(beta):

            lambd = np.random.randint(1, n + 1)
            positions_to_mutate = np.random.choice(range(0, n), lambd, replace=False)

            for position in positions_to_mutate:
                temp[position] += 1
                temp[position] %= 2

            temp_value = f(decodeInd(temp))
            best_value = f(decodeInd(best))
            sec_best_value = f(decodeInd(sec_best))

            if minim:
                if temp_value < best_value:
                    sec_best = best.copy()
                    best = temp.copy()
                elif temp_value < sec_best_value:
                    sec_best = temp.copy()
            else:
                if temp_value > best_value:
                    sec_best = best.copy()
                    best = temp.copy()
                elif temp_value > sec_best_value:
                    sec_best = temp.copy()

    return best, sec_best


def crossover_microbial(A, B):
    f = config.f
    minim = config.minim
    n = len(A)
    dlugosc_segmentu = random.randint(1, n-1)

    max_alfa = n - dlugosc_segmentu
    alfa = random.randint(0, max_alfa - 1)

    if not minim:
        if f(decodeInd(A)) >= f(decodeInd(B)):
            for i in range(alfa, alfa + dlugosc_segmentu):
                B[i] = A[i]
        else:
            for i in range(alfa, alfa + dlugosc_segmentu):
                A[i] = B[i]
    else:
        if f(decodeInd(A)) < f(decodeInd(B)):
            for i in range(alfa, alfa + dlugosc_segmentu):
                B[i] = A[i]
        else:
            for i in range(alfa, alfa + dlugosc_segmentu):
                A[i] = B[i]
    return A, B


def crossover_discrete(parent1, parent2):
    child1_individual = []
    child2_individual = []

    for gene1, gene2 in zip(parent1, parent2):
        if random.random() <= 0.5:
            child1_individual.append(gene1)
            child2_individual.append(gene2)
        else:
            child1_individual.append(gene2)
            child2_individual.append(gene1)

    return child1_individual, child2_individual


def crossover_three_point(ind1, ind2):
    size = min(len(ind1), len(ind2))

    cxpoints = sorted(random.sample(range(1, size), 3))

    ind1[cxpoints[0]:cxpoints[1]], ind2[cxpoints[0]:cxpoints[1]] = ind2[cxpoints[0]:cxpoints[1]], ind1[cxpoints[0]:cxpoints[1]]
    ind1[cxpoints[2]:], ind2[cxpoints[2]:] = ind2[cxpoints[2]:], ind1[cxpoints[2]:]

    return ind1, ind2



# a=-2
# b=2
# minim=False
# n=4
# f=projekt5.hyperellipsoid
# a1, b1 = common_features_random_sample_climbing_crossover([1,0,0,0, 0,0,0,1, 0,0,1,1, 0,0,1,1], [1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,0,0])
# print(a1, b1)
# print(decodeInd(a1), decodeInd(b1))
