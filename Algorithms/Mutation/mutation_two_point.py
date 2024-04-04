import random

def mutation_two_point(chromosome, mutation_rate):
    if random.random() <= mutation_rate:
        indexes = random.sample(range(len(chromosome)), 2)
        for index in indexes:
            chromosome[index] = 1 if chromosome[index] == 0 else 0
    return chromosome