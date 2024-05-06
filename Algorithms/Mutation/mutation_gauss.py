import random
import numpy as np


def mutation_gauss(individual, mutation_rate, a, b):
    if random.random() <= mutation_rate:
        for i_chrom in range(len(individual.chromosomes)):
            i_chrom_val = individual.chromosomes[i_chrom]
            d = np.random.normal(0, 1)
            while (i_chrom_val + d) < a or (i_chrom_val + d) > b:
                d = np.random.normal(0, 1)
            individual.chromosomes[i_chrom] = i_chrom_val + d
    return individual
