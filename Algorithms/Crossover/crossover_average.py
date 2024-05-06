import random

from Representation.individual import Individual


def crossover_average(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child_individual = Individual(len(parent1.chromosomes), empty=True)

    for i_chrom in range(len(parent1.chromosomes)):

        child_individual.add_chromosome((parent1.chromosomes[i_chrom] +
                                        parent2.chromosomes[i_chrom]) / 2)

    return [child_individual]
