import random

from Representation.individual import Individual


def crossover_gene_pooling_2(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child_individual = Individual(len(parent1.chromosomes), empty=True)

    avg_len = len(parent1.chromosomes)
    child_individual.chromosomes = random.sample(parent1.chromosomes + parent2.chromosomes, avg_len)

    return [child_individual]
