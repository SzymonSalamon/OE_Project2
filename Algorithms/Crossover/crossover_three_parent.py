import random

def crossover_three_parent(Pula_rodzicow):
    parent1, parent2, parent3 = random.sample(Pula_rodzicow, 3)
    childrens = []
    point = random.randint(1, len(parent1) - 1)
    childrens.append(crossover_onepoint(parent1, parent2,point))
    childrens.append(crossover_onepoint(parent2, parent1,point))
    point = random.randint(1, len(parent1) - 1)
    childrens.append(crossover_onepoint(parent3, childrens[0],point))
    return childrens
def crossover_onepoint(parent1, parent2, crossover_point):
    if len(parent1) != len(parent2):
        raise ValueError("Tablice muszą być tej samej długości.")
    child = []
    child.extend(parent1[:crossover_point])
    child.extend(parent2[crossover_point:])
    return child