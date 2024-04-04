import random

def mutation_edge(chromosome, mutation_rate):
    if random.random() <= mutation_rate:
        chromosome[-1] = 1 if chromosome[-1] == 0 else 0
    return chromosome