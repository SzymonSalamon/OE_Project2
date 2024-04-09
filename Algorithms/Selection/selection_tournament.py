
import random

from Representation.population import Population


def selection_tournament(population: Population, tournament_size: int, function, a, b):
    population_for_cross = []
    individuals = population.individuals_pool
    tournaments = split_list_into_sublists(individuals, tournament_size)

    for tournament in tournaments:
        best_ind = tournament[0]
        best_ind_val = function(best_ind.decode(a, b))

        for individual in tournament[1:]:
            val = function(individual.decode(a, b))
            if val > best_ind_val:
                best_ind = individual
                best_ind_val = val

        population_for_cross.append(best_ind)

    return population_for_cross


def split_list_into_sublists(lst, n):
    random.shuffle(lst)

    sublist_length = len(lst) // n

    sublists = [lst[i:i + sublist_length] for i in range(0, len(lst), sublist_length)]

    return sublists




