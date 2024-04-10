import random

from Representation.individual import Individual

'''
Klasa Population, przechowujaca populacje chromosomow.
chromosome_length - dlugosc chromosomow
var_number - liczba zmiennych badanej funkcji n-zmiennych
^^ argumenty przekazywane do obiektu klasy Chromosome

population_size - wielkosc populacji
'''


class Population:
    def __init__(self):
        self.population_size = None
        self.individuals_pool = []

    def generate_individuals_pool(self, chromosome_length, var_number, population_size):
        individuals_pool = []
        for _ in range(population_size):
            individual = Individual(chromosome_length, var_number)
            individuals_pool.append(individual)
        self.individuals_pool = individuals_pool

    def get_chromosomes_for_individual(self, variable_index):
        """
        Zwraca wszystkie chromosomy odpowiadające danemu argumentowi w funkcji n zmiennych.

        :param variable_index: Indeks zmiennej, dla której pobieramy chromosomy.
        :return: Lista chromosomów odpowiadających danemu argumentowi.
        """
        chromosomes_for_variable = []
        for individual in self.individuals_pool:
            chromosomes_for_variable.append(individual.chromosomes[variable_index])
        return chromosomes_for_variable

    def get_population(self):
        for individual in self.individuals_pool:
            print(individual.chromosomes)

    def add_individual_to_population(self, individual: Individual):
        self.individuals_pool.append(individual)

    def evaluate_and_sort_individuals(self, function, a, b, minim):
        func_values = []
        for i in range(len(self.individuals_pool)):
            func_values.append((function(self.individuals_pool[i].decode(a, b)), i))

        if minim:
            sorted_func_values = sorted(func_values, key=lambda x: x[0])
        else:
            sorted_func_values = sorted(func_values, key=lambda x: x[0], reverse=True)

        return sorted_func_values

    def get_average(self, function, a, b):
        func_values_sum = 0
        for i in range(len(self.individuals_pool)):
            func_values_sum += function(self.individuals_pool[i].decode(a, b))

        return func_values_sum / len(self.individuals_pool)

    def get_best_individual(self, function, a, b, minim):
        best_ind = self.individuals_pool[0]
        best_ind_val = function(self.individuals_pool[0].decode(a, b))

        for i in range(1, len(self.individuals_pool)):
            val = function(self.individuals_pool[i].decode(a, b))
            if minim:
                if val < best_ind_val:
                    best_ind = self.individuals_pool[i]
                    best_ind_val = val
            else:
                if val > best_ind_val:
                    best_ind = self.individuals_pool[i]
                    best_ind_val = val

        return best_ind, best_ind_val

    def get_random_individuals(self, num_individuals):
        return random.sample(self.individuals_pool, num_individuals)


