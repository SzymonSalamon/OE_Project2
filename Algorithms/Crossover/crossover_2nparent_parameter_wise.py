import random
import numpy as np

from Representation.individual import Individual


# funkcja krzyzowania jednopunktowego
def crossover(vector1, vector2):
    crossover_point = np.random.randint(0, len(vector1))
    child = np.concatenate((vector1[:crossover_point], vector2[crossover_point:]))
    return child


def crossover_2nparent_parameter_wise(Pula_rodzicow, l=4, q=3):
    # wylosowanie l rodzicow
    M_pool = random.sample(Pula_rodzicow, l)
    children = []
    for i in range(l):
        children.append(Individual(len(M_pool[0].chromosomes[0]), len(M_pool[0].chromosomes), True))

    for i_chrom in range(len(M_pool[0].chromosomes)):
        Parameter_pool = [np.array_split(parent.chromosomes[i_chrom], q) for parent in M_pool]

        child_parameters = np.zeros((l, q), dtype=object)

        # Krzyzowanie jednopunktowe pomiedzy parametrami rodzicow
        for j in range(q):
            for i in range(l):
                m = np.random.randint(0, l - 1)
                while m == i:
                    m = np.random.randint(0, l - 1)
                child_parameters[i][j] = crossover(Parameter_pool[i][j], Parameter_pool[m][j])

        # Tworzenie potomka z losowo wybranych parametrow
        for i in range(l):
            chromosome = []
            for j in range(q):
                z = np.random.randint(0, l - 1)
                chromosome.extend(child_parameters[z, j])
            children[i].add_chromosome(chromosome)
    return children


m_p = [Individual(9, 2), Individual(9, 2), Individual(9, 2), Individual(9, 2)]
print(m_p[0].chromosomes)
print(m_p[1].chromosomes)
kek1 = crossover_2nparent_parameter_wise(m_p)
print(kek1[0].chromosomes, "\n", kek1[1].chromosomes)
