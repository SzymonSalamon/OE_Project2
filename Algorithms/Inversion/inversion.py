import random


def inversion(chromosome, inversion_rate):
    if random.random() <= inversion_rate:
        start_index = random.randint(0, len(chromosome) - 1)
        end_index = random.randint(start_index + 1, len(chromosome))

        inverted_genes = chromosome[start_index:end_index][::-1]
        chromosome[start_index:end_index] = inverted_genes
    return chromosome