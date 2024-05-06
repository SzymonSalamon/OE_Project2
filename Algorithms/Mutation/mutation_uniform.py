import random


def mutation_uniform(individual, mutation_rate, a, b):
    if random.random() <= mutation_rate:
        rand_ind = random.randint(0, len(individual.chromosomes) - 1)
        individual.chromosomes[rand_ind] = random.uniform(a, b)
    return individual
