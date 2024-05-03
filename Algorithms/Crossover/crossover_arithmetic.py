import random

import numpy as np

from Representation.individual import Individual
def crossover_arithmetic(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    alpha = random.uniform(0, 1)
    child1_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), empty=True)
    child2_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), empty=True)
    for i in len(parent1.chromosomes):

    for i_chrom in range(len(parent1.chromosomes)):
        point1 = random.randint(0, len(parent1.chromosomes[0]) - 1)

        child1 = np.concatenate((parent1.chromosomes[i_chrom][:point1],
                                 parent2.chromosomes[i_chrom][point1:]))
        child2 = np.concatenate((parent2.chromosomes[i_chrom][:point1],
                                 parent1.chromosomes[i_chrom][point1:]))

        child1_individual.add_chromosome(child1)
        child2_individual.add_chromosome(child2)

    return [child1_individual, child2_individual]