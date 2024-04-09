import random


def mutation_single_point(chromosome, mutation_rate):
    if random.random() <= mutation_rate:
        index = random.randint(0, len(chromosome) - 1)
        chromosome[index] = 1 if chromosome[index] == 0 else 0
    return chromosome
