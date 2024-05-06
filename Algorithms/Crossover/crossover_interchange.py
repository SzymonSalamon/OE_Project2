import random

from Representation.individual import Individual


def crossover_interchange(M_pool, function, alpha, minim=False):
    X, Y = random.sample(M_pool, 2)
    Z = []
    W = []
    V = []
    Q = []
    n = len(X.chromosomes)

    for i in range(n):
        Z.append((X.chromosomes[i] + Y.chromosomes[i]) / 2)
        W.append((1 - alpha) * X.chromosomes[i] + alpha * max(X.chromosomes[i], Y.chromosomes[i]))
        V.append((1 - alpha) * X.chromosomes[i] + alpha * min(X.chromosomes[i], Y.chromosomes[i]))
        Q.append(((X.chromosomes[i] + X.chromosomes[i]) * (1 - alpha) +
                  (X.chromosomes[i] + Y.chromosomes[i]) * alpha) / 2)

    scores = [function(chromosome) for chromosome in [Z, W, V, Q]]
    best_chromosomes = [Z, W, V, Q][scores.index(max(scores))]
    if minim is True:
        best_chromosomes = [Z, W, V, Q][scores.index(min(scores))]

    child_individual = Individual(len(X.chromosomes), empty=True)
    child_individual.chromosomes = best_chromosomes

    return [child_individual]
