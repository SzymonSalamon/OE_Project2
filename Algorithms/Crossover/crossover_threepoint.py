import random

import numpy as np

from Representation.individual import Individual


def crossover_threepoint(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child1_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), True)
    child2_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), True)

    for i_chrom in range(len(parent1.chromosomes)):
        point1 = random.randint(0, len(parent1.chromosomes[0]) - 3)
        point2 = random.randint(point1, len(parent1.chromosomes[0]) - 2)
        point3 = random.randint(point2, len(parent1.chromosomes[0]) - 1)

        child1 = np.concatenate((parent1.chromosomes[i_chrom][:point1],
                                 parent2.chromosomes[i_chrom][point1:point2],
                                 parent1.chromosomes[i_chrom][point2:point3],
                                 parent2.chromosomes[i_chrom][point3:]))
        child2 = np.concatenate((parent2.chromosomes[i_chrom][:point1],
                                 parent1.chromosomes[i_chrom][point1:point2],
                                 parent2.chromosomes[i_chrom][point2:point3],
                                 parent1.chromosomes[i_chrom][point3:]))

        child1_individual.add_chromosome(child1)
        child2_individual.add_chromosome(child2)

    return [child1_individual, child2_individual]


# m_p = [Individual(5, 5), Individual(5, 5)]
# print(m_p[0].chromosomes)
# print(m_p[1].chromosomes)
# kek1, kek2 = crossover_threepoint(m_p)
# print(kek1.chromosomes, "\n", kek2.chromosomes)
