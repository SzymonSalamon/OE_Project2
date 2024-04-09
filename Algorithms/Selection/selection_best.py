from Representation.population import Population


def selection_best(population: Population, num_of_best_individuals: int, function, a, b):
    population.sorted_individuals = population.evaluate_and_sort_individuals(function, a, b)
    population_for_cross = Population()
    for i in range(num_of_best_individuals):
        index_of_i_best_individual = population.sorted_individuals[i][1]
        population_for_cross.add_individual_to_population(population.individuals_pool[index_of_i_best_individual])
    # for i in range(num_of_best_individuals):
    #     index_of_i_best_individual = population.sorted_individuals[len() - i][1]
    #     population_for_cross.add_individual_to_population(population.individuals_pool[index_of_i_best_individual])
    return population_for_cross
