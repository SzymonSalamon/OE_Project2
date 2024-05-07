import copy

import numpy as np

from Algorithms.Crossover import crossover_common_features_random_sample_climbing, crossover_arithmetic, \
    crossover_average, crossover_blend_alpha, crossover_blend_alpha_beta, crossover_gene_pooling_2, crossover_linear, \
    crossover_multiparent, crossover_interchange, crossover_variant_A
from Representation.population import Population


class Epoch:
    def __init__(self, population: Population, var_number: int,
                 population_size: int, elite_individuals: int, selection_method, selection_config,
                 cross_prob: float, cross_method, mutation_prob: float, mutation_method, inversion_prob: float,
                 function, a, b, epoch_amount, num_of_epoch=1,
                 alpha=5, beta=5, minim=True):
        self.population = population
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
        self.population.generate_individuals_pool(self.a, self.b, self.var_number, self.population_size)

    def select_elite_individuals_for_new_population(self):
        self.elites = []
        sorted_individuals = self.population.evaluate_and_sort_individuals(self.function, self.minim)
        for i in range(self.elite_individuals):
            elite_individual = self.population.individuals_pool[sorted_individuals[i][1]]
            self.elites.append(copy.deepcopy(elite_individual))

    def selection(self):
        self.population_to_cross = self.selection_method(
            self.population, self.selection_config, self.function, self.minim)

    def check_chromosomes_between_a_b(self, individual):
        for i in range(len(individual.chromosomes)):
            if individual.chromosomes[i] < self.a:
                individual.chromosomes[i] = self.a
            elif individual.chromosomes[i] > self.b:
                individual.chromosomes[i] = self.b
        return individual

    def cross(self):
        while len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals):

            random_float = np.random.rand()

            if random_float > self.cross_prob:
                for individual in self.population_to_cross.get_random_individuals(2):
                    if len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals):
                        checked_ind = self.check_chromosomes_between_a_b(individual)
                        self.new_population.add_individual_to_population(checked_ind)

            else:
                if self.cross_method == crossover_blend_alpha:
                    children = self.cross_method(self.population_to_cross.individuals_pool, self.alpha)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        checked_ind = self.check_chromosomes_between_a_b(children.pop(0))
                        self.new_population.add_individual_to_population(checked_ind)

                elif self.cross_method == crossover_blend_alpha_beta:
                    children = self.cross_method(self.population_to_cross.individuals_pool, self.alpha, self.beta)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        checked_ind = self.check_chromosomes_between_a_b(children.pop(0))
                        self.new_population.add_individual_to_population(checked_ind)

                elif self.cross_method == crossover_linear or self.cross_method == crossover_variant_A:
                    children = self.cross_method(self.population_to_cross.individuals_pool, self.function, self.minim)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        checked_ind = self.check_chromosomes_between_a_b(children.pop(0))
                        self.new_population.add_individual_to_population(checked_ind)

                elif self.cross_method == crossover_interchange:
                    children = self.cross_method(self.population_to_cross.individuals_pool, self.function, self.alpha,
                                                 self.minim)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        checked_ind = self.check_chromosomes_between_a_b(children.pop(0))
                        self.new_population.add_individual_to_population(checked_ind)

                else:
                    children = self.cross_method(self.population_to_cross.individuals_pool)
                    while (len(self.new_population.individuals_pool) < (self.population_size - self.elite_individuals)
                           and children != []):
                        checked_ind = self.check_chromosomes_between_a_b(children.pop(0))
                        self.new_population.add_individual_to_population(checked_ind)

    def mutation(self):
        for i in range(len(self.new_population.individuals_pool)):
            individual = self.mutation_method(
                self.new_population.individuals_pool[i],
                self.mutation_prob,
                self.a, self.b)

            self.new_population.individuals_pool[i] = individual

    def add_elites(self):
        for elite in self.elites:
            self.new_population.add_individual_to_population(elite)

    def run_epoch(self):

        self.select_elite_individuals_for_new_population()
        self.selection()
        self.cross()
        self.mutation()
        self.add_elites()

        best_ind, best_ind_val = self.new_population.get_best_individual(self.function, self.minim)
        # print("Best:", best_ind_val)
        avg = self.new_population.get_average(self.function)
        # print("Average:", avg)
        # for ind in self.new_population.individuals_pool:
        #     print(ind.chromosomes)
        #     print(self.function(ind.chromosomes))
        values_of_individuals = self.new_population.evaluate_and_sort_individuals(
            self.function, self.minim)
        values_of_individuals = [t[0] for t in values_of_individuals]

        std_deviation = np.std(values_of_individuals)
        # print("STD:", std_deviation)

        with open('Data/testrzecz/epoki_i_srednia.txt', 'a') as file:
            file.write(str(avg) + '\n')

        with open('Data/testrzecz/odchylenie_standardowe.txt', 'a') as file:
            file.write(str(std_deviation) + '\n')

        with open('Data/testrzecz/najlepsza_wartosc.txt', 'a') as file:
            file.write(str(best_ind_val) + '\n')

        with open('Data/testrzecz/najlepszy_osobnik.txt', 'a') as file:
            file.write(str(best_ind.chromosomes) + '\n')

        return self.new_population
