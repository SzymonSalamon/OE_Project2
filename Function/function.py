"""
Funkcje bedace celem minimalizacji
"""


def hyperellipsoid(x):
    n = len(x)
    suma = 0
    for i in range(n):
        for j in range(i+1):
            suma += (x[j] ** 2)
    return suma


def discus(x):
    n = len(x)
    suma = 0
    for i in range(1, n):
        suma = suma + x[i] ** 2
    return x[0] ** 2 + (10 ** 6) * suma
