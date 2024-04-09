import random

from Representation.individual import Individual


def crossover_discrete(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child_individual = Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), True)

    for i_chrom in range(len(parent1.chromosomes)):
        chromosome = []
        for gene1, gene2 in zip(parent1.chromosomes[i_chrom], parent2.chromosomes[i_chrom]):
            if random.random() <= 0.5:
                chromosome.append(gene1)
            else:
                chromosome.append(gene2)
        child_individual.add_chromosome(chromosome)

    return child_individual


# m_p = [Individual(5, 5), Individual(5, 5)]
# print(m_p[0].chromosomes)
# print(m_p[1].chromosomes)
# kek1 = crossover_discrete(m_p)
# print(kek1.chromosomes)
