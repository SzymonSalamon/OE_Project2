import copy

import numpy as np

from Algorithms.Crossover import crossover_common_features_random_sample_climbing
from Algorithms.Crossover import crossover_2nparent_parameter_wise
from Algorithms.Crossover import crossover_discrete
from Algorithms.Crossover import crossover_microbial
from Algorithms.Crossover import crossover_onepoint
from Algorithms.Crossover import crossover_three_parent
from Algorithms.Crossover import crossover_threepoint
from Algorithms.Crossover import crossover_twopoint
from Algorithms.Crossover import crossover_uniform
from Algorithms.Inversion.inversion import inversion
from Representation.population import Population


class Epoch:
    def __init__(self, population: Population, chromosome_length: int, var_number: int,
                 population_size: int, elite_individuals: int, selection_method, selection_config,
                 cross_prob: float, cross_method, mutation_prob: float, mutation_method, inversion_prob: float,
                 function, a, b, epoch_amount, num_of_epoch=1,
                 alpha=5, beta=5, minim=True):
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
        self.mutation_method = mutation_method
        self.inversion_prob = inversion_prob
        self.function = function
        self.a, self.b = a, b
        self.new_population = Population()
        self.population_to_cross = None
        self.epoch_amount = epoch_amount
        self.num_of_epoch = num_of_epoch
        # alpha i beta tylko dla crossover_common_features_random_sample_climbing
        self.alpha = alpha
        self.beta = beta
        self.minim = minim
        self.elites = []

    def generate_individuals_in_population(self):
        self.population.generate_individuals_pool(self.chromosome_length, self.var_number, self.population_size)

    def select_elite_individuals_for_new_population(self):
        self.elites = []
        sorted_individuals = self.population.evaluate_and_sort_individuals(self.function, self.a, self.b, self.minim)
        for i in range(self.elite_individuals):
            elite_individual = self.population.individuals_pool[sorted_individuals[i][1]]
            self.elites.append(copy.deepcopy(elite_individual))

    def selection(self):
        self.population_to_cross = self.selection_method(
            self.population, self.selection_config, self.function, self.a, self.b, self.minim)

    def cross(self):
        while len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals):
            crosses_2_parents = [crossover_onepoint, crossover_twopoint, crossover_threepoint,
                                 crossover_microbial, crossover_discrete, crossover_uniform,
                                 crossover_common_features_random_sample_climbing]

            random_float = np.random.rand()
            if random_float > self.cross_prob:
                if self.cross_method in crosses_2_parents:
                    for individual in self.population_to_cross.get_random_individuals(2):
                        if len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals):
                            self.new_population.add_individual_to_population(individual)

                elif self.cross_method == crossover_three_parent:
                    for individual in self.population_to_cross.get_random_individuals(3):
                        if len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals):
                            self.new_population.add_individual_to_population(individual)

                elif self.cross_method == crossover_2nparent_parameter_wise:
                    for individual in self.population_to_cross.get_random_individuals(4):
                        if len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals):
                            self.new_population.add_individual_to_population(individual)

            else:
                if self.cross_method == crossover_common_features_random_sample_climbing:
                    child = self.cross_method(self.population_to_cross.individuals_pool, self.alpha, self.beta,
                                              self.a, self.b, self.function, self.minim)
                    self.new_population.add_individual_to_population(child)

                elif self.cross_method == crossover_microbial:
                    children = self.cross_method(self.population_to_cross.individuals_pool, self.function,
                                                 self.a, self.b)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        self.new_population.add_individual_to_population(children.pop(0))

                elif (self.cross_method in crosses_2_parents or
                      self.cross_method == crossover_2nparent_parameter_wise or
                      self.cross_method == crossover_three_parent):
                    children = self.cross_method(self.population_to_cross.individuals_pool)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        self.new_population.add_individual_to_population(children.pop(0))

    def mutation(self):
        for individual in self.new_population.individuals_pool:
            for chromosome_index in range(len(individual.chromosomes)):
                individual.chromosomes[chromosome_index] = self.mutation_method(
                    individual.chromosomes[chromosome_index],
                    self.mutation_prob)

    def inversion(self):
        for individual in self.new_population.individuals_pool:
            for chromosome_index in range(len(individual.chromosomes)):
                individual.chromosomes[chromosome_index] = inversion(individual.chromosomes[chromosome_index],
                                                                     self.inversion_prob)

    def add_elites(self):
        for elite in self.elites:
            self.new_population.add_individual_to_population(elite)

    def run_epoch(self):

        self.select_elite_individuals_for_new_population()
        self.selection()
        self.cross()
        self.mutation()
        self.inversion()
        self.add_elites()

        best_ind, best_ind_val = self.new_population.get_best_individual(self.function, self.a, self.b, self.minim)
        # print("Best:", best_ind_val)
        avg = self.new_population.get_average(self.function, self.a, self.b)
        # print("Average:", avg)
        # for ind in self.new_population.individuals_pool:
        #     print(self.function(ind.decode(self.a, self.b)))
        values_of_individuals = self.new_population.evaluate_and_sort_individuals(
            self.function, self.a, self.b, self.minim)
        values_of_individuals = [t[0] for t in values_of_individuals]
        std_deviation = np.std(values_of_individuals)
        # print("STD:", std_deviation)

        with open('Data/test/plik_epoki_i_srednia_disc4.txt', 'a') as file:
            file.write(str(avg) + '\n')

        with open('Data/test/plik_odchylenie_standardowe_disc4.txt', 'a') as file:
            file.write(str(std_deviation) + '\n')

        with open('Data/test/plik_najlepsza_wartosc_disc4.txt', 'a') as file:
            file.write(str(best_ind_val) + '\n')

        return self.new_population
