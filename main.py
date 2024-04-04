from Algorithms.Crossover.crossover_microbial import crossover_microbial
from Representation.population import  Population
from Algorithms.Crossover.crossover_uniform import crossover_uniform
from Algorithms.Inversion.inversion import inversion

'''
Do testowania dzialania
'''
population = Population(10, 5, 3)
print(population.get_population())

print(population.get_chromosomes_for_variable(0))
M_pool = population.get_chromosomes_for_variable(0)
#wynik = crossover_microbial(M_pool)
wynik = crossover_microbial(M_pool)
print(wynik)

print(inversion(wynik[0], 1))