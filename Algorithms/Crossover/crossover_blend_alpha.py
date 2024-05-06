import random

from Representation.individual import Individual


def crossover_blend_alpha(M_pool, alpha):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child1_individual = Individual(len(parent1.chromosomes), empty=True)
    child2_individual = Individual(len(parent1.chromosomes), empty=True)

    for i_chrom in range(len(parent1.chromosomes)):
        min_val = min(parent1.chromosomes[i_chrom], parent2.chromosomes[i_chrom])
        max_val = max(parent1.chromosomes[i_chrom], parent2.chromosomes[i_chrom])
        d = abs(parent1.chromosomes[i_chrom] - parent2.chromosomes[i_chrom])
        min_val -= d * alpha
        max_val += d * alpha

        child1_individual.add_chromosome(random.uniform(min_val, max_val))
        child2_individual.add_chromosome(random.uniform(min_val, max_val))

    return [child1_individual, child2_individual]
