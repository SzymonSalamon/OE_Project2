import random

def crossover_threepoint(M_pool):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1) != len(parent2):
        raise ValueError("Tablice muszą być tej samej długości.")
    point1 = random.randint(1, len(parent1) - 1)
    point2 = random.randint(point1, len(parent1) - 1)
    point3 = random.randint(point2, len(parent1) - 1)
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:point3] + parent2[point3:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:point3] + parent1[point3:]
    return child1, child2