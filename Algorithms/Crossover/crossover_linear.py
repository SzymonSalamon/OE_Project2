import random

from Representation.individual import Individual


def crossover_linear(M_pool, function, minim=False):
    parent1, parent2 = random.sample(M_pool, 2)
    if len(parent1.chromosomes) != len(parent2.chromosomes):
        raise ValueError("Tablice muszą być tej samej długości.")

    child1_individual = Individual(len(parent1.chromosomes), empty=True)
    child2_individual = Individual(len(parent1.chromosomes), empty=True)

    child1_chromosomes = []
    child2_chromosomes = []
    child3_chromosomes = []

    for i_chrom in range(len(parent1.chromosomes)):
        child1_chromosomes.append(0.5 * parent1.chromosomes[i_chrom] +
                                  0.5 * parent2.chromosomes[i_chrom])
        child2_chromosomes.append(1.5 * parent1.chromosomes[i_chrom] -
                                  0.5 * parent2.chromosomes[i_chrom])
        child3_chromosomes.append(-0.5 * parent1.chromosomes[i_chrom] +
                                  1.5 * parent2.chromosomes[i_chrom])

    func_values = []
    children_chromosomes = [child1_chromosomes, child2_chromosomes, child3_chromosomes]

    for i in range(len(children_chromosomes)):
        func_values.append((function(children_chromosomes[i]), i))

    if minim:
        sorted_func_values = sorted(func_values, key=lambda x: x[0])
    else:
        sorted_func_values = sorted(func_values, key=lambda x: x[0], reverse=True)

    child1_individual.chromosomes = locals()['child' + str(sorted_func_values[0][1] + 1) + '_chromosomes']
    child2_individual.chromosomes = locals()['child' + str(sorted_func_values[1][1] + 1) + '_chromosomes']

    return [child1_individual, child2_individual]
