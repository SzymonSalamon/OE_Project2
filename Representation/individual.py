import numpy as np

'''
Klasa chromosom, przechowujaca tablice n argumentow w reprezentacji binarnej
length - dlugosc chromosomu
n - liczba zmiennych w funkcji n-zmiennych
'''


class Individual:
    def __init__(self, length, n, empty=False):
        self.length = length
        self.n = n
        if not empty:
            self.chromosomes = self.generate_chromosomes()
        else:
            self.chromosomes = []

    def generate_chromosomes(self):
        chromosomes = []
        for _ in range(self.n):
            chromosomes.append(np.random.randint(0, 2, self.length))
        return chromosomes

    def add_chromosome(self, chromosome):
        self.chromosomes.append(chromosome)

    def decode(self, a, b):
        """
        Funkcja dekodująca łańcuch binarny na wartości dziesiętne dla każdego chromosomu.
        """
        decoded_values = []
        for binary_num in self.chromosomes:
            binary_num_str = ''.join(map(str, binary_num))
            decimal_num = int(binary_num_str, 2)
            decoded_value = a + decimal_num * (b - a) / (2 ** self.length - 1)
            decoded_values.append(decoded_value)
        return decoded_values
