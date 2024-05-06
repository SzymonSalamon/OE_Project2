import random
import numpy as np

from Representation.individual import Individual


# Define the main algorithm for the maximum problem.
def crossover_variant_A(M_pool, function, minim=False):
    """
    Implementacja algorytmu wariantu A dla problemu maksymalizacji.

    :param rodzice: Lista wektorów rodziców (struktura przypominająca 2D array).
    :param n: Liczba składników każdego wektora rodzica.
    :param MAX: Liczba iteracji do wykonania.
    :return: Wektor potomka (1D array), reprezentujący rozwiązanie.
    """
    # Wybieramy parę rodziców
    X_t, Y_t = random.sample(M_pool, 2)
    X, Y = X_t.chromosomes, Y_t.chromosomes
    # Inicjalizujemy najlepszego jako pierwszego rodzica
    Best = np.copy(X_t.chromosomes)

    n = len(X_t.chromosomes)

    MAX = 10
    # Perform the algorithm MAX times
    for _ in range(MAX):
        Z = np.empty(n)

        # Losujemy liczbę z przedziału (0, 1)
        alpha = np.random.uniform(0, 1)

        # Generujemy potomka
        for i in range(n):
            Z[i] = alpha * X[i] + (1 - alpha) * Y[i]

        # Jeśli nowy potomek jest lepszy niż dotychczasowy najlepszy, sam staje się najlepszym
        if not minim:
            if function(Z) > function(Best):
                Best = Z
        else:
            if function(Z) < function(Best):
                Best = Z

    child_individual = Individual(len(X), empty=True)
    child_individual.chromosomes = Best

    return [child_individual]
