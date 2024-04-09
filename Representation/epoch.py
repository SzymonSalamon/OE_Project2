from random import random

import numpy as np

from Algorithms.Crossover import crossover_common_features_random_sample_climbing
from Algorithms.Crossover.crossover_2nparent_parameter_wise import crossover_2nparent_parameter_wise
from Algorithms.Crossover.crossover_discrete import crossover_discrete
from Algorithms.Crossover.crossover_microbial import crossover_microbial
from Algorithms.Crossover.crossover_onepoint import crossover_onepoint
from Algorithms.Crossover.crossover_three_parent import crossover_three_parent
from Algorithms.Crossover.crossover_threepoint import crossover_threepoint
from Algorithms.Crossover.crossover_twopoint import crossover_twopoint
from Algorithms.Crossover.crossover_uniform import crossover_uniform
from Representation.population import Population


class Epoch:
    def __init__(self, population: Population, chromosome_length: int, var_number: int,
                 population_size: int, elite_individuals: int, selection_method, selection_config,
                 cross_prob: float, cross_method, mutation_prob: float, inversion_prob: float, function, a, b,
                 alpha=5, beta=5, minim=False):
        self.population = population
        self.chromosome_length = chromosome_length
        self.var_number = var_number
        self.population_size = population_size
        self.elite_individuals = elite_individuals
        self.selection_method = selection_method
        # selection config - dla turniejowego wielkość tunieju, dla selekcji najlepszych i ruletki liczba osobników
        self.selection_config = selection_config
        self.cross_prob = cross_prob
        self.cross_method = cross_method
        self.mutation_prob = mutation_prob
        self.inversion_prob = inversion_prob
        self.function = function
        self.a, self.b = a, b
        self.new_population = Population()
        self.population_to_cross = None
        self.selected_individuals = []
        # alpha i beta tylko dla crossover_common_features_random_sample_climbing
        self.alpha = alpha
        self.beta = beta
        self.minim = minim

    def generate_individuals_in_population(self):
        self.population.generate_individuals_pool(self.chromosome_length, self.var_number, self.population_size)

    def select_elite_individuals_for_new_population(self):
        sorted_individuals = self.population.evaluate_and_sort_individuals(self.function, self.a, self.b)
        for i in range(self.elite_individuals):
            elite_individual = self.population.individuals_pool[sorted_individuals[i][1]]
            self.new_population.add_individual_to_population(elite_individual)

    def selection(self):
        self.population_to_cross = self.selection_method(
            self.population, self.selection_config, self.function, self.a, self.b)

    def cross(self):
        while len(self.new_population.individuals_pool) < self.population_size:
            crosses_2_parents = [crossover_twopoint, crossover_threepoint, crossover_onepoint,
                                 crossover_microbial, crossover_discrete, crossover_uniform,
                                 crossover_common_features_random_sample_climbing]

            random_float = np.random.rand()
            if random_float < self.cross_prob:
                if self.cross_method in crosses_2_parents:
                    for individual in self.population_to_cross.get_random_individuals(2):
                        if len(self.new_population.individuals_pool) < self.population_size - self.elite_individuals:
                            self.new_population.add_individual_to_population(individual)

                elif self.cross_method == crossover_three_parent:
                    for individual in self.population_to_cross.get_random_individuals(3):
                        if len(self.new_population.individuals_pool) < self.population_size - self.elite_individuals:
                            self.new_population.add_individual_to_population(individual)

                elif self.cross_method == crossover_2nparent_parameter_wise:
                    for individual in self.population_to_cross.get_random_individuals(4):
                        if len(self.new_population.individuals_pool) < self.population_size - self.elite_individuals:
                            self.new_population.add_individual_to_population(individual)

            else:
                if self.cross_method == crossover_common_features_random_sample_climbing:
                    child = self.cross_method(self.population.individuals_pool, self.alpha, self.beta,
                                              self.a, self.b, self.function, self.minim)
                    self.new_population.add_individual_to_population(child)

                elif self.cross_method == crossover_microbial:
                    children = self.cross_method(self.population.individuals_pool, self.function, self.a, self.b)
                    while len(self.new_population.individuals_pool) < self.population_size:
                        self.new_population.add_individual_to_population(children.pop(0))

                if self.cross_method in crosses_2_parents:
                    self.cross_method()
