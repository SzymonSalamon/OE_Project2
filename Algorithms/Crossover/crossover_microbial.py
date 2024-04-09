import random

from Function.function import discus
from Representation.individual import Individual


def crossover_microbial(M_pool, f, a, b):
    n = len(M_pool[0].chromosomes[0])

    A, B = random.sample(M_pool, 2)
    val_A = f(A.decode(a, b))
    val_B = f(B.decode(a, b))

    for i_chrom in range(len(A.chromosomes)):

        dlugosc_segmentu = random.randint(1, n - 1)
        max_alfa = n - dlugosc_segmentu
        alfa = random.randint(0, max_alfa - 1)

        if val_A >= val_B:
            for i in range(alfa, alfa + dlugosc_segmentu):
                B.chromosomes[i_chrom][i] = A.chromosomes[i_chrom][i]

        else:
            for i in range(alfa, alfa + dlugosc_segmentu):
                A.chromosomes[i_chrom][i] = B.chromosomes[i_chrom][i]

    return [A, B]


# m_p = [Individual(5, 5), Individual(5, 5)]
# print(m_p[0].chromosomes)
# print(m_p[1].chromosomes)
# kek1, kek2 = crossover_microbial(m_p, discus, -10, 10)
# print(kek1.chromosomes, "\n", kek2.chromosomes)
