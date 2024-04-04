import random

def crossover_uniform(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1) != len(parent2):
        raise ValueError("Tablice muszą być tej samej długości.")
    child = []
    for gene1, gene2 in zip(parent1, parent2):
        if random.random() <= 0.5:
            child.append(gene1)
        else:
            child.append(gene2)
    return child
