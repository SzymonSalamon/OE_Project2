from Representation.chromosome import Chromosome

'''
Klasa Population, przechowujaca populacje chromosomow.
chromosome_length - dlugosc chromosomow
var_number - liczba zmiennych badanej funkcji n-zmiennych
^^ argumenty przekazywane do obiektu klasy Chromosome

population_size - wielkosc populacji
'''
class Population:
    def __init__(self, chromosome_length, var_number, population_size):
        self.population_size = population_size
        self.chromosome_pool = self.generate_chromosome_pool(chromosome_length, var_number)

    def generate_chromosome_pool(self, chromosome_length, var_number):
        chromosomes = []
        for _ in range(self.population_size):
            chromosome = Chromosome(chromosome_length, var_number)
            chromosomes.append(chromosome)
        return chromosomes

    def get_chromosomes_for_variable(self, variable_index):
        """
        Zwraca wszystkie chromosomy odpowiadające danemu argumentowi w funkcji n zmiennych.

        :param variable_index: Indeks zmiennej, dla której pobieramy chromosomy.
        :return: Lista chromosomów odpowiadających danemu argumentowi.
        """
        chromosomes_for_variable = []
        for chromosome in self.chromosome_pool:
            chromosomes_for_variable.append(chromosome.chromosomes[variable_index])
        return chromosomes_for_variable

    def get_population(self):
        for chromosome in self.chromosome_pool:
            print(chromosome.chromosomes)

# population = Population(16, 2, 5)
# for chromosome in population.chromosome_pool:
#     print(chromosome.chromosomes)