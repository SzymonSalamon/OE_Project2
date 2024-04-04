import random
def crossover_onepoint(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1) != len(parent2):
        raise ValueError("Tablice muszą być tej samej długości.")
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2