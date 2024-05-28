import random
import os
from deap import base, creator, tools
from krzyzowanie import (crossover_2nparent_parameter_wise, common_features_random_sample_climbing_crossover,
                         crossover_microbial, crossover_discrete, crossover_three_point)
from projekt5 import fitness_function_h, hyperellipsoid, fitness_function_d, discus
import config
import time
import matplotlib.pyplot as plt

chromosome_len = int(input("Podaj długość chromosu: ") or 5)
variables = int(input("Podaj liczbę zmiennych: ") or 5)
population_size = int(input("Podaj rozmiar populacji: ") or 10)
num_to_select = int(input("Podaj liczbę osobników do selekcji: ") or 4)

len_of_ind = variables * chromosome_len
config.n = len_of_ind

# Ustawienia wprowadzane przez użytkownika
config.a = float(input("Podaj wartość dla config.a: ") or -100)
config.b = float(input("Podaj wartość dla config.b: ") or 100)

# Wybór minimalizacji/maksymalizacji
minim_choice = input('Wybierz problem min lub maks ("min" -> minimalizacja, "max" -> maksymalizacja): ').strip().lower()
if minim_choice == "min":
    config.minim = True
else:
    config.minim = False

if config.minim:
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
else:
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len_of_ind)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Wybór funkcji
function_choice = input('Wybierz funkcję ("a" -> discuss, "b" -> hyperellipsoid): ').strip().lower()
if function_choice == "a":
    toolbox.register("evaluate", fitness_function_d)
    config.f = discus
elif function_choice == "b" or function_choice == '':
    toolbox.register("evaluate", fitness_function_h)
    config.f = hyperellipsoid
else:
    print("Nieprawidłowy wybór funkcji. Ustawiono domyślną wartość hyperellipsoid.")
    config.f = hyperellipsoid

population = toolbox.population(n=population_size)
# print("Przykładowa populacja:")
# for ind in population:
#     print(ind)

fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

selected_population = None

# Selekcja
# Metody selekcji
selection_methods = {
    'a': tools.selRandom,
    'b': tools.selBest,
    'c': tools.selWorst,
    'd': "tournament",  # Tutaj uwzględniamy tournsize dla turnieju
    'e': tools.selRoulette
}

print("\nWybierz metodę selekcji:")
print("a) Random")
print("b) Best")
print("c) Worst")
print("d) Tournament")
print("e) Roulette")

sel_choice = input("Wybierz metodę selekcji (a-e): ").lower()
selected_selection = selection_methods.get(sel_choice)

if selected_selection:
    if sel_choice == 'd':
        toolbox.register("select", tools.selTournament, k=num_to_select, tournsize=3)
    else:
        toolbox.register("select", selected_selection, k=num_to_select)
else:
    print("Niepoprawny wybór metody selekcji.")

# Krzyżowanie
# Metody krzyżowania
print("\nWybierz metodę krzyżowania:")
print("a) Uniform")
print("b) TwoPoint")
print("c) OnePoint")
print("d) 2N")
print("e) CommonFeaturesRandomSample")
print("f) Microbial")
print("g) Discrete")
print("h) Three Point")
print("i) Ordered")

cx_choice = input("Wybierz metodę krzyżowania (a-i): ").lower()

if cx_choice:
    if cx_choice == 'd':
        toolbox.register("cross", crossover_2nparent_parameter_wise)
    elif cx_choice == 'e':
        toolbox.register("cross", common_features_random_sample_climbing_crossover)
    elif cx_choice == 'f':
        toolbox.register("cross", crossover_microbial)
    elif cx_choice == 'g':
        toolbox.register("cross", crossover_discrete)
    elif cx_choice == 'h':
        toolbox.register("cross", crossover_three_point)
    elif cx_choice == 'i':
        toolbox.register("cross", tools.cxOrdered)
    elif cx_choice == 'a':
        toolbox.register("cross", tools.cxUniform, indpb=0.1)
    elif cx_choice == 'b':
        toolbox.register("cross", tools.cxTwoPoint)
    elif cx_choice == 'c':
        toolbox.register("cross", tools.cxOnePoint)
    else:
        print("Niepoprawny wybór metody krzyżowania.")
        exit()
else:
    print("Niepoprawny wybór metody krzyżowania.")
    exit()

# Mutacja
# Metody mutacji
mutation_methods = {
    'a': tools.mutShuffleIndexes,
    'b': tools.mutFlipBit
}

print("\nWybierz metodę mutacji:")
print("a) ShuffleIndexes")
print("b) FlipBit")

mut_choice = input("Wybierz metodę mutacji (a-b): ").lower()
selected_mutation = mutation_methods.get(mut_choice)

if selected_mutation:
    toolbox.register("mutate", selected_mutation, indpb=0.1)
else:
    print("Niepoprawny wybór metody mutacji.")
    exit()


probabilityMutation = 0.1
probabilityCrossover = 0.9
numberIteration = 1000

g = 0
numberElitism = 2

start_time = time.time()  # Początkowy czas


pliki_do_usuniecia = [
    "Data/epoki_i_srednia.txt",
    "Data/najlepsza_wartosc.txt",
    "Data/odchylenie_standardowe.txt",
    "Data/wykres_test.jpg"
]

for plik in pliki_do_usuniecia:
    if os.path.exists(plik):
        try:
            os.remove(plik)
            print(f"Plik {plik} został usunięty.")
        except Exception as e:
            print(f"Wystąpił błąd przy usuwaniu pliku {plik}: {e}")
    else:
        print(f"Plik {plik} nie istnieje.")


while g < numberIteration:
    g = g + 1

    # Select the next generation individuals
    selected = toolbox.select(population)
    offspring = [toolbox.clone(ind) for ind in selected]

    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))
    listElitism = []
    for x in range(0, numberElitism):
        listElitism.append(tools.selBest(population, 1)[0])

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):

        # cross two individuals with probability CXPB
        if random.random() < probabilityCrossover:
            toolbox.cross(child1, child2)

            # fitness values of the children
            # must be recalculated later
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        # mutate an individual with probability MUTPB
        if random.random() < probabilityMutation:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Gather all the fitnesses in one list and print the stats
    fits = [ind.fitness.values[0] for ind in population]

    population[:] = offspring + listElitism

    length = len(population)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)
    std = abs(sum2 / length - mean ** 2) ** 0.5
    best_ind = tools.selBest(population, 1)[0]

    if g < 4 or g > numberIteration - 3:
        print("-- Generation %i --" % g)
        print(" Evaluated %i individuals" % len(invalid_ind))
        print(" Min %s" % min(fits))
        print(" Max %s" % max(fits))
        print(" Avg %s" % mean)
        print(" Std %s" % std)

        print("Best individual is %s, value = %s" % (best_ind, best_ind.fitness.values[0]))

    with open('Data/epoki_i_srednia.txt', 'a') as file:
        file.write(str(mean) + '\n')

    with open('Data/odchylenie_standardowe.txt', 'a') as file:
        file.write(str(std) + '\n')

    with open('Data/najlepsza_wartosc.txt', 'a') as file:
        file.write(str(best_ind.fitness.values[0]) + '\n')

    with open('Data/najlepszy_osobnik.txt', 'a') as file:
        file.write(str(best_ind) + '\n')

end_time = time.time()  # Końcowy czas
elapsed_time = end_time - start_time  # Obliczenie czasu wykonania

print("-- End of (successful) evolution --")

# Wczytanie danych z plików tekstowych
with open('Data/odchylenie_standardowe.txt', 'r') as file:
    std_dev_lines = file.readlines()
    std_dev_values = [float(line.strip()) for line in std_dev_lines]

with open('Data/najlepsza_wartosc.txt', 'r') as file:
    best_value_lines = file.readlines()
    best_values = [float(line.strip()) for line in best_value_lines]

with open('Data/epoki_i_srednia.txt', 'r') as file:
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
plt.savefig('Data/wykres_test.jpg', dpi=300)  # Zapisuje wykresy jako plik JPEG
plt.show()
# Wyświetlenie okna dialogowego z informacją o czasie wykonania
print("Czas wykonania funkcji", f"Funkcja wykonana w czasie: {elapsed_time:.2f} sekundy")
