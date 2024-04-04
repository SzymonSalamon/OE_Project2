import random

def crossover_uniform(M_pool, probability=0.5):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1) != len(parent2):
        raise ValueError("Tablice muszą być tej samej długości.")
    child1, child2 = [], []
    for gene1, gene2 in zip(parent1, parent2):
        if random.random() < probability:
            child1.append(gene1)
            child2.append(gene2)
        else:
            child1.append(gene2)
            child2.append(gene1)
    return child1, child2
