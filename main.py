from Algorithms.Crossover.crossover_microbial import crossover_microbial
from Representation.population import  Population
from Algorithms.Crossover.crossover_uniform import crossover_uniform
from Algorithms.Inversion.inversion import inversion

'''
Do testowania dzialania
'''
# population = Population(10, 5, 3)
# print(population.get_population())
#
# print(population.get_chromosomes_for_variable(0))
# M_pool = population.get_chromosomes_for_variable(0)
# #wynik = crossover_microbial(M_pool)
# wynik = crossover_microbial(M_pool)
# print(wynik)
#
# print(inversion(wynik[0], 1))

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Wczytanie danych z plików tekstowych
with open('Data/plik_odchylenie_standardowe_big.txt', 'r') as file:
    std_dev_lines = file.readlines()
    std_dev_values = [float(line.strip()) for line in std_dev_lines]

with open('Data/plik_najlepsza_wartosc_big.txt', 'r') as file:
    best_value_lines = file.readlines()
    best_values = [float(line.strip()) for line in best_value_lines]

with open('Data/plik_epoki_i_srednia_big.txt', 'r') as file:
    mean_lines = file.readlines()
    mean_values = [float(line.strip()) for line in mean_lines]

# Tworzenie wykresów
plt.figure(figsize=(10, 8))

# Tworzenie listy indeksów jako wartości osi X
epochs = list(range(len(std_dev_values)))

# Wykres odchylenia standardowego
plt.subplot(3, 1, 1)
plt.plot(epochs, std_dev_values, marker='s', color='r', label='Odchylenie standardowe')
plt.title('Odchylenie standardowe, średnia wartość i najlepsza wartość w zależności od epoki')
plt.xlabel('Epoka')
plt.ylabel('Odchylenie standardowe')
plt.legend()

# Wykres średnich wartości
plt.subplot(3, 1, 2)
plt.plot(epochs, mean_values, marker='o', color='b', label='Średnia wartość')
plt.title('Średnia wartość w zależności od epoki')
plt.xlabel('Epoka')
plt.ylabel('Średnia wartość')
plt.legend()

# Wykres najlepszych wartości
plt.subplot(3, 1, 3)
plt.plot(epochs, best_values, marker='^', color='g', label='Najlepsza wartość')
plt.title('Najlepsza wartość w zależności od epoki')
plt.xlabel('Epoka')
plt.ylabel('Najlepsza wartość')
plt.legend()

# Zapisywanie wykresów jako pliki JPEG
plt.tight_layout()  # Zapewnia, że etykiety nie będą się nakładać na siebie
plt.savefig('Data/wykresy_big.jpg', dpi=300)  # Zapisuje wykresy jako plik JPEG
plt.show()