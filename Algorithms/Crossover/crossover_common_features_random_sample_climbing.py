import copy
import random
import numpy as np

from Function.function import discus
from Representation.individual import Individual


def decode(binary_num, a, b, n):
    """
    Funkcja dekodująca łańcuch binarny na wartość dziesiętną.
    """
    binary_num = ''.join(map(str, binary_num))
    decimal_num = int(binary_num, 2)
    return a + decimal_num * (b - a) / (2 ** n - 1)


def crossover_common_features_random_sample_climbing(Pula_rodzicow, alpha, beta, a, b, f, minim=False):
    """
    Powielanie z lokalnym dostrajaniem.
    Common Features/Random Sample Climbing Crossover.

    Funkcja wyliczająca potomka C krzyżując rodziców A i B
    używając powyższego operatora krzyżowania.


    :param alpha: Liczba pętli zewnętrznych, określająca ile instancji V będzie poddawane losowym mutacjom.
    :param beta: Liczba pętli wewnętrznych, określająca ilu losowym mutacjom polegnie każda instancja V.
    :param a: Pierwsza, mniejsza liczba określająca dolną granicę zakresu w którym poszukiwane jest rozwiązanie.
    :param b: Druga, większa liczba określająca górną granicę zakresu w którym poszukiwane jest rozwiązanie.
    :param f: Funkcja
    :param minim: Wartość typu bool określająca czy funkcja rozwiązuje problem minimalizacji.
                  Domyślnie ma wartość false - rozwiązywany jest problem maksymalizacji.
    """
    A, B = random.sample(Pula_rodzicow, 2)
    n = len(A.chromosomes[0])
    V = Individual(n, len(A.chromosomes))
    individuals = []
    for i in range(alpha * beta):
        individuals.append(Individual(n, len(A.chromosomes), True))

    ind_index = 0

    for chromosome_index in range(len(A.chromosomes)):
        # A, B, V chrom
        A_chrom = A.chromosomes[chromosome_index]
        B_chrom = B.chromosomes[chromosome_index]
        V_chrom = V.chromosomes[chromosome_index]

        for i in range(n):
            if A_chrom[i] == B_chrom[i] == 1:
                V_chrom[i] = 1
            else:
                V_chrom[i] = 0

        for i in range(alpha):

            temp = copy.deepcopy(V_chrom)

            for j in range(beta):
                lambd = np.random.randint(1, n + 1)

                positions_to_mutate = np.random.choice(range(0, n), lambd, replace=False)

                for position in positions_to_mutate:
                    temp[position] += 1
                    temp[position] %= 2

                individuals[ind_index].add_chromosome(temp)
                ind_index += 1
                if ind_index == alpha * beta:
                    ind_index = 0

    best = None
    best_val = None

    for individual in individuals:
        if best is None:
            best = individual
            best_val = f(individual.decode(a, b))
        else:
            val = f(individual.decode(a, b))

            if not minim:
                if val > best_val:
                    best = individual
                    best_val = val

            else:
                if val < best_val:
                    best = individual
                    best_val = val

    return best

# m_p = [Individual(5, 5), Individual(5, 5)]
# print(m_p[0].chromosomes)
# print(m_p[1].chromosomes)
# kek1 = crossover_common_features_random_sample_climbing(m_p, 5, 5, -10, 10, discus, True)
# print(kek1.chromosomes, discus(kek1.decode(-10, 10)))
# print(discus([-10]))
# print(discus([10, 10, 10, 10, 10]))
# print(discus([2, 5, 0, 0, 2]))
# print(discus(kek1.decode(-10, 10)))
