import random
import numpy as np

from projekt5 import decodeInd
import config


def crossover_arithmetic(parent1, parent2):
    alpha = random.uniform(0, 1)
    child1 = []
    child2 = []

    for i_chrom in range(len(parent1)):
        child1_new_chrom = (alpha * parent1[i_chrom] + (1 - alpha) * parent2[i_chrom])
        child2_new_chrom = (alpha * parent2[i_chrom] + (1 - alpha) * parent1[i_chrom])

        child1.append(child1_new_chrom)
        child2.append(child2_new_chrom)

    return child1, child2


def crossover_average(parent1, parent2):
    child = []

    for i_chrom in range(len(parent1)):
        child.append((parent1[i_chrom] + parent2[i_chrom]) / 2)

    return child,


def crossover_blend_alpha(parent1, parent2):
    alpha = config.alpha
    child1 = []
    child2 = []

    for i_chrom in range(len(parent1)):
        min_val = min(parent1[i_chrom], parent2[i_chrom])
        max_val = max(parent1[i_chrom], parent2[i_chrom])
        d = abs(parent1[i_chrom] - parent2[i_chrom])
        min_val -= d * alpha
        max_val += d * alpha

        min_val = max(min_val, config.a)
        max_val = min(max_val, config.b)

        child1.append(random.uniform(min_val, max_val))
        child2.append(random.uniform(min_val, max_val))

    return child1, child2


def crossover_blend_alpha_beta(parent1, parent2):
    alpha = config.alpha
    beta = config.beta

    child1 = []
    child2 = []

    for i_chrom in range(len(parent1)):
        min_val = min(parent1[i_chrom], parent2[i_chrom])
        max_val = max(parent1[i_chrom], parent2[i_chrom])
        d = abs(parent1[i_chrom] - parent2[i_chrom])
        min_val -= d * alpha
        max_val += d * beta
        min_val = max(min_val, config.a)
        max_val = min(max_val, config.b)

        child1.append(random.uniform(min_val, max_val))
        child2.append(random.uniform(min_val, max_val))

    return child1, child2


def crossover_gene_pooling_2(parent1, parent2):
    avg_len = len(parent1)
    combined_genes = parent1 + parent2
    random.shuffle(combined_genes)

    child1 = combined_genes[:avg_len]
    child2 = combined_genes[avg_len:]

    return child1, child2


def crossover_interchange(parent1, parent2):
    X = parent1
    Y = parent2
    Z = []
    W = []
    V = []
    Q = []
    n = len(X)
    function = config.f
    alpha = config.alpha
    minim = config.minim

    a, b = config.a, config.b

    for i in range(n):
        Z.append((X[i] + Y[i]) / 2)
        W.append((1 - alpha) * X[i] + alpha * max(X[i], Y[i]))
        V.append((1 - alpha) * X[i] + alpha * min(X[i], Y[i]))
        Q.append(((X[i] + X[i]) * (1 - alpha) + (X[i] + Y[i]) * alpha) / 2)

    scores = [function(chromosome) for chromosome in [Z, W, V, Q]]
    best_chromosomes = [Z, W, V, Q][scores.index(max(scores))]
    second_best_chromosomes = [chromosome for _, chromosome in sorted(zip(scores, [Z, W, V, Q]), reverse=True)][1]
    if minim is True:
        best_chromosomes = [Z, W, V, Q][scores.index(min(scores))]
        second_best_chromosomes = [chromosome for _, chromosome in sorted(zip(scores, [Z, W, V, Q]), reverse=False)][1]

    best_chromosomes = [a if x < a else b if x > b else x for x in best_chromosomes]
    second_best_chromosomes = [a if x < a else b if x > b else x for x in second_best_chromosomes]

    return best_chromosomes, second_best_chromosomes


def crossover_linear(parent1, parent2):
    minim = config.minim
    function = config.f

    child1_chromosomes = []
    child2_chromosomes = []
    child3_chromosomes = []

    for i_chrom in range(len(parent1)):
        child1_chromosomes.append(0.5 * parent1[i_chrom] + 0.5 * parent2[i_chrom])
        child2_chromosomes.append(1.5 * parent1[i_chrom] - 0.5 * parent2[i_chrom])
        child3_chromosomes.append(-0.5 * parent1[i_chrom] + 1.5 * parent2[i_chrom])

    children_chromosomes = [child1_chromosomes, child2_chromosomes, child3_chromosomes]
    func_values = [(function(child), idx) for idx, child in enumerate(children_chromosomes)]

    if minim:
        sorted_func_values = sorted(func_values, key=lambda x: x[0])
    else:
        sorted_func_values = sorted(func_values, key=lambda x: x[0], reverse=True)

    best_child1 = children_chromosomes[sorted_func_values[0][1]]
    best_child2 = children_chromosomes[sorted_func_values[1][1]]

    return best_child1, best_child2


def crossover_mixer_a(a, b, alfa=0.5, beta=0.5):
    lower = min(a, b)
    upper = max(a, b)
    d1 = abs(a - b)
    return random.uniform(lower - d1 * alfa, upper + - d1 * beta)


def crossover_multiparent(parent1, parent2):
    n = len(parent1)
    parents = [parent1, parent2]

    offspring = []
    for j in range(2):
        child = []
        for i in range(n):
            k = random.choice([idx for idx in range(2) if idx != j])
            child_feature = crossover_mixer_a(parents[j][i], parents[k][i])
            child.append(child_feature)
        offspring.append(child)

    child1 = offspring[0]
    child2 = offspring[1]

    return child1, child2


def crossover_variant_A(X_t, Y_t):
    X, Y = X_t, Y_t
    Best1 = np.copy(X)
    Best2 = np.copy(Y)
    n = len(X)
    MAX = 10

    minim = config.minim
    function = config.f

    for _ in range(MAX):
        Z = np.empty(n)
        alpha = np.random.uniform(0, 1)
        for i in range(n):
            Z[i] = alpha * X[i] + (1 - alpha) * Y[i]

        if not minim:
            if function(Z) > function(Best1):
                Best2 = Best1
                Best1 = Z
            elif function(Z) > function(Best2):
                Best2 = Z
        else:
            if function(Z) < function(Best1):
                Best2 = Best1
                Best1 = Z
            elif function(Z) < function(Best2):
                Best2 = Z

    child1 = Best1.tolist()
    child2 = Best2.tolist()

    return child1, child2

