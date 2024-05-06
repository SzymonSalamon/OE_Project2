import random

from Representation.individual import Individual


def crossover_mixer_a(a, b, alfa=0.5, beta=0.5):
    lower = min(a, b)
    upper = max(a, b)
    d1 = abs(a - b)
    return random.uniform(lower - d1 * alfa, upper + - d1 * beta)


def crossover_multiparent(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    n = len(parent1.chromosomes)
    parents = [parent1.chromosomes, parent2.chromosomes]

    child1_individual = Individual(len(parent1.chromosomes), empty=True)
    child2_individual = Individual(len(parent1.chromosomes), empty=True)

    offspring = []
    for j in range(2):
        child = []
        for i in range(n):
            k = random.choice([idx for idx in range(2) if idx != j])
            child_feature = crossover_mixer_a(parents[j][i], parents[k][i])
            child.append(child_feature)
        offspring.append(child)

    child1_individual.chromosomes = offspring[0]
    child2_individual.chromosomes = offspring[1]

    return [child1_individual, child2_individual]
