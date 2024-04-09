import random

from Representation.individual import Individual


def crossover_uniform(M_pool, probability=0.5):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child1_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), True)
    child2_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), True)

    for i_chrom in range(len(parent1.chromosomes)):
        child1, child2 = [], []
        for gene1, gene2 in zip(parent1.chromosomes[i_chrom], parent2.chromosomes[i_chrom]):
            if random.random() < probability:

                child1.append(gene1)
                child2.append(gene2)
            else:

                child1.append(gene2)
                child2.append(gene1)
        child1_individual.add_chromosome(child1)
        child2_individual.add_chromosome(child2)

    return [child1_individual, child2_individual]


# m_p = [Individual(5, 5), Individual(5, 5)]
# print(m_p[0].chromosomes)
# print(m_p[1].chromosomes)
# kek1, kek2 = crossover_uniform(m_p)
# print(kek1.chromosomes, "\n", kek2.chromosomes)
