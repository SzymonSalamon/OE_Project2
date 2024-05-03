import numpy as np
import random

'''
Klasa chromosom, przechowujaca tablice n argumentow w reprezentacji binarnej
length - dlugosc chromosomu
n - liczba zmiennych w funkcji n-zmiennych
'''


class Individual:
    def __init__(self, n, a=0.0, b=1.0, empty=False):
        self.a = a
        self.b = b
        self.n = n
        if not empty:
            self.chromosomes = self.generate_chromosomes()
        else:
            self.chromosomes = []

    def generate_chromosomes(self):
        chromosomes = []
        for _ in range(self.n):
            chromosomes.append(random.uniform(self.a, self.b))
        return chromosomes

    def add_chromosome(self, chromosome):
        self.chromosomes.append(chromosome)
