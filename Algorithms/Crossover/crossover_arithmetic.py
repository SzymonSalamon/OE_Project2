import random

from Representation.individual import Individual


def crossover_arithmetic(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    alpha = random.uniform(0, 1)
    child1_individual = Individual(len(parent1.chromosomes), empty=True)
    child2_individual = Individual(len(parent1.chromosomes), empty=True)

    for i_chrom in range(len(parent1.chromosomes)):
        child1_new_chrom = (alpha * parent1.chromosomes[i_chrom] +
                            (1 - alpha) * parent2.chromosomes[i_chrom])
        child2_new_chrom = (alpha * parent2.chromosomes[i_chrom] +
                            (1 - alpha) * parent1.chromosomes[i_chrom])

        child1_individual.add_chromosome(child1_new_chrom)
        child2_individual.add_chromosome(child2_new_chrom)

    return [child1_individual, child2_individual]
