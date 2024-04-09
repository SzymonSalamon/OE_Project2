import random

from Representation.individual import Individual


def crossover_three_parent(M_pool):
    parent1, parent2, parent3 = random.sample(M_pool, 3)

    children = []
    for i in range(3):
        children.append(Individual(len(parent1.chromosomes[0]), len(parent1.chromosomes), True))

    for i_chrom in range(len(parent1.chromosomes)):
        point = random.randint(1, len(parent1.chromosomes[0]) - 1)
        children[0].add_chromosome(crossover_onepoint(parent1.chromosomes[i_chrom], parent2.chromosomes[i_chrom], point))
        children[1].add_chromosome(crossover_onepoint(parent2.chromosomes[i_chrom], parent1.chromosomes[i_chrom], point))
        point = random.randint(1, len(parent1.chromosomes[0]) - 1)
        children[2].add_chromosome(crossover_onepoint(parent3.chromosomes[i_chrom], children[0].chromosomes[i_chrom], point))

    return children


def crossover_onepoint(parent1, parent2, crossover_point):
    if len(parent1) != len(parent2):
        raise ValueError("Tablice muszą być tej samej długości.")
    child = []
    child.extend(parent1[:crossover_point])
    child.extend(parent2[crossover_point:])
    return child


# m_p = [Individual(5, 5), Individual(5, 5), Individual(5, 5), Individual(5,5)]
# print(m_p[0].chromosomes)
# print(m_p[1].chromosomes)
# kek1 = crossover_three_parent(m_p)
# print(kek1[0].chromosomes, "\n", kek1[1].chromosomes, "\n", kek1[2].chromosomes)
