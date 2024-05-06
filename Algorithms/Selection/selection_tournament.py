
import random

from Representation.population import Population


def selection_tournament(population: Population, tournament_size: int, function, minim):
    population_for_cross = Population()
    individuals = population.individuals_pool
    tournaments = split_list_into_sublists(individuals, tournament_size)

    for tournament in tournaments:
        best_ind = tournament[0]
        best_ind_val = function(best_ind.chromosomes)

        for individual in tournament[1:]:
            val = function(individual.chromosomes)
            if minim:
                if val < best_ind_val:
                    best_ind = individual
                    best_ind_val = val
            else:
                if val > best_ind_val:
                    best_ind = individual
                    best_ind_val = val

        population_for_cross.add_individual_to_population(best_ind)

    return population_for_cross


def split_list_into_sublists(lst, n):
    random.shuffle(lst)

    sublist_length = len(lst) // n

    sublists = [lst[i:i + sublist_length] for i in range(0, len(lst), sublist_length)]

    return sublists




