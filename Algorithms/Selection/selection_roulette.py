import numpy as np

from Function.function import hyperellipsoid
from Representation.population import Population


def selection_roulette(population: Population, num_of_individuals_to_select: int, function, a, b, minim):
    sum_of_function_values = 0
    if minim:
        for individual in population.individuals_pool:
            sum_of_function_values += 1./function(individual.decode(a, b))
    else:
        for individual in population.individuals_pool:
            sum_of_function_values += function(individual.decode(a, b))
    list_of_probabilities = []
    for individual in population.individuals_pool:
        list_of_probabilities.append(function(individual.decode(a, b)) / sum_of_function_values)

    #print(list_of_probabilities)
    selected_individuals = []
    while len(selected_individuals) < num_of_individuals_to_select:
        random_float = np.random.rand()
        for i in range(len(list_of_probabilities)):
            if random_float <= list_of_probabilities[i]:
                if i not in selected_individuals:
                    selected_individuals.append(i)
                break
            else:
                random_float -= list_of_probabilities[i]

    population_for_cross = Population()
    for i in selected_individuals:
        population_for_cross.add_individual_to_population(population.individuals_pool[i])

    return population_for_cross


# testpop = Population()
# testpop.generate_individuals_pool(10, 5, 20)
# selection_roulette(testpop, 5, hyperellipsoid, -10, 10, True)

