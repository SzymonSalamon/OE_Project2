import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt

from Algorithms.Crossover import crossover_arithmetic, crossover_average, crossover_blend_alpha, \
    crossover_blend_alpha_beta, crossover_gene_pooling_2, crossover_linear, crossover_multiparent, \
    crossover_interchange, crossover_variant_A
from Algorithms.Crossover.crossover_2nparent_parameter_wise import crossover_2nparent_parameter_wise
from Algorithms.Crossover.crossover_common_features_random_sample_climbing import \
    crossover_common_features_random_sample_climbing
from Algorithms.Crossover.crossover_discrete import crossover_discrete
from Algorithms.Crossover.crossover_microbial import crossover_microbial
from Algorithms.Crossover.crossover_onepoint import crossover_onepoint
from Algorithms.Crossover.crossover_three_parent import crossover_three_parent
from Algorithms.Crossover.crossover_threepoint import crossover_threepoint
from Algorithms.Crossover.crossover_twopoint import crossover_twopoint
from Algorithms.Crossover.crossover_uniform import crossover_uniform
from Algorithms.Mutation.mutation_edge import mutation_edge
from Algorithms.Mutation.mutation_gauss import mutation_gauss
from Algorithms.Mutation.mutation_single_point import mutation_single_point
from Algorithms.Mutation.mutation_two_point import mutation_two_point
from Algorithms.Mutation.mutation_uniform import mutation_uniform
from Algorithms.Selection.selection_best import selection_best
from Algorithms.Selection.selection_roulette import selection_roulette
from Algorithms.Selection.selection_tournament import selection_tournament
from Function.function import hyperellipsoid, discus
from Representation.epoch import Epoch
from Representation.population import Population


class GeneticAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm Parameters")

        # Domyślne wartości dla parametrów
        default_values = {
            "Length of the chromosomes": "10",
            "Number of variables for function": "2",
            "Size of population": "10",
            "Amount of individuals for elite selection": "2",
            "Size of tournament / number of individuals for selections": "4",
            "Probability of crossover": "0.9",
            "Probability of mutation": "0.1",
            "Probability of inversion": "0.1",
            "Begin of the range": "-65.536",
            "End of the range": "65.536",
            "Number of epochs": "200",
            "(CFRSC crossover) alpha": "0.1",
            "(CFRSC crossover) beta": "0.2"
        }
        
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))
        style.configure('TMenubutton', font=('Arial', 12))

        parameters_frame = ttk.Frame(root)
        parameters_frame.pack(padx=10, pady=10)

        # Label and Entry widgets for each parameter
        parameters = [
            ("Number of variables for function", "var_number"),
            ("Size of population", "population_size"),
            ("Amount of individuals for elite selection", "elite_individuals"),
            ("Size of tournament / number of individuals for selections", "selection_config"),
            ("Probability of crossover", "cross_prob"),
            ("Probability of mutation", "mutation_prob"),
            ("Probability of inversion", "inversion_prob"),
            ("Begin of the range", "a"),
            ("End of the range", "b"),
            ("Number of epochs", "epoch_amount"),
            ("(CFRSC crossover) alpha", "alpha"),
            ("(CFRSC crossover) beta", "beta")
        ]

        self.entries = {}
        for i, (label_text, param_name) in enumerate(parameters):
            label = ttk.Label(parameters_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            default_value = default_values.get(label_text, "")
            entry = ttk.Entry(parameters_frame)
            entry.insert(0, default_value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[param_name] = entry

        # Dropdowns for selection, crossover, mutation, function, and optimization type
        self.selection_methods = ["Selection", "best", "roulette", "tournament"]
        self.selection_var = tk.StringVar(root)
        self.selection_var.set(self.selection_methods[0])
        selection_dropdown = ttk.OptionMenu(parameters_frame, self.selection_var, *self.selection_methods)
        selection_dropdown.grid(row=len(parameters), column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.crossover_methods = ["Crossover", "arithmetic", "average",
                                  "blend_alpha", "blend_alpha_beta", "gene_pooling_2", "linear", "multiparent",
                                  "interchange", "variant_A"]
        self.crossover_var = tk.StringVar(root)
        self.crossover_var.set(self.crossover_methods[0])
        crossover_dropdown = ttk.OptionMenu(parameters_frame, self.crossover_var, *self.crossover_methods)
        crossover_dropdown.grid(row=len(parameters) + 1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.mutation_methods = ["Mutation", "gauss", "uniform"]
        self.mutation_var = tk.StringVar(root)
        self.mutation_var.set(self.mutation_methods[0])
        mutation_dropdown = ttk.OptionMenu(parameters_frame, self.mutation_var, *self.mutation_methods)
        mutation_dropdown.grid(row=len(parameters) + 2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        function_methods = ["Function", "hyperellipsoid", "discus"]
        self.function_var = tk.StringVar(root)
        self.function_var.set(function_methods[0])
        function_dropdown = ttk.OptionMenu(parameters_frame, self.function_var, *function_methods)
        function_dropdown.grid(row=len(parameters) + 3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        optimization_types = ["Optimization ", "min", "max"]
        self.optimization_var = tk.StringVar(root)
        self.optimization_var.set(optimization_types[0])
        optimization_dropdown = ttk.OptionMenu(parameters_frame, self.optimization_var, *optimization_types)
        optimization_dropdown.grid(row=len(parameters) + 4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Button to start the process
        start_button = ttk.Button(root, text="Start", command=self.start_process)
        start_button.pack(pady=10)

    def start_process(self):
        for filename in os.listdir("Data/testrzecz/"):
            file_path = os.path.join("Data/testrzecz/", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        parameters = {}
        for param_name, entry_widget in self.entries.items():
            parameters[param_name] = entry_widget.get()

        # Wyodrębnij nazwy wybranych metod
        selection_method_name = self.selection_var.get()
        crossover_method_name = self.crossover_var.get()
        mutation_method_name = self.mutation_var.get()

        function_name = self.function_var.get()

        if function_name == "hyperellipsoid":
            selected_function = hyperellipsoid
        else:
            selected_function = discus

        if selection_method_name == "best":
            selection_function = selection_best
        elif selection_method_name == "roulette":
            selection_function = selection_roulette
        else:
            selection_function = selection_tournament

        crossover_methods = {
            "arithmetic": crossover_arithmetic,
            "average": crossover_average,
            "blend_alpha": crossover_blend_alpha,
            "blend_alpha_beta": crossover_blend_alpha_beta,
            "gene_pooling_2": crossover_gene_pooling_2,
            "linear": crossover_linear,
            "multiparent": crossover_multiparent,
            "interchange": crossover_interchange,
            "variant_A": crossover_variant_A,
            "onepoint": crossover_onepoint,
            "twopoint": crossover_twopoint,
            "threepoint": crossover_threepoint,
            "microbial": crossover_microbial,
            "discrete": crossover_discrete,
            "uniform": crossover_uniform,
            "common_features_random_sample_climbing": crossover_common_features_random_sample_climbing,
            "three_parent": crossover_three_parent,
            "2nparent_parameter_wise": crossover_2nparent_parameter_wise,
        }
        crossover_function = crossover_methods.get(crossover_method_name, crossover_twopoint)

        if mutation_method_name == "gauss":
            mutation_function = mutation_gauss
        else:
            mutation_function = mutation_uniform

        parameters["optimization_type"] = self.optimization_var.get()
        if parameters["optimization_type"] == "min":
            parameters["optimization_type"] = True
        else:
            parameters["optimization_type"] = False
        parameters["var_number"] = int(parameters["var_number"])
        parameters["population_size"] = int(parameters["population_size"])
        parameters["elite_individuals"] = int(parameters["elite_individuals"])
        parameters["selection_config"] = int(parameters["selection_config"])
        parameters["epoch_amount"] = int(parameters["epoch_amount"])
        parameters["cross_prob"] = float(parameters["cross_prob"])
        parameters["mutation_prob"] = float(parameters["mutation_prob"])
        parameters["inversion_prob"] = float(parameters["inversion_prob"])
        parameters["alpha"] = float(parameters["alpha"])
        parameters["beta"] = float(parameters["beta"])
        parameters["a"] = float(parameters["a"])
        parameters["b"] = float(parameters["b"])

        first_epoch = Epoch(Population(), parameters["var_number"],
                            parameters["population_size"], parameters["elite_individuals"],
                            selection_function, parameters["selection_config"], parameters["cross_prob"],
                            crossover_function, parameters["mutation_prob"], mutation_function,
                            parameters["inversion_prob"], selected_function, parameters["a"], parameters["b"],
                            parameters["epoch_amount"], 1, parameters["alpha"], parameters["beta"],
                            parameters["optimization_type"])

        first_epoch.generate_individuals_in_population()
        start_time = time.time()  # Początkowy czas
        for i in range(parameters["epoch_amount"]):
            first_epoch.population = first_epoch.run_epoch()
            first_epoch.new_population = Population()
        end_time = time.time()  # Końcowy czas
        elapsed_time = end_time - start_time  # Obliczenie czasu wykonania

        # Wczytanie danych z plików tekstowych
        with open('Data/testrzecz/odchylenie_standardowe.txt', 'r') as file:
            std_dev_lines = file.readlines()
            std_dev_values = [float(line.strip()) for line in std_dev_lines]

        with open('Data/testrzecz/najlepsza_wartosc.txt', 'r') as file:
            best_value_lines = file.readlines()
            best_values = [float(line.strip()) for line in best_value_lines]

        with open('Data/testrzecz/epoki_i_srednia.txt', 'r') as file:
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
        plt.savefig('Data/test/wykres_test.jpg', dpi=300)  # Zapisuje wykresy jako plik JPEG
        plt.show()
        # Wyświetlenie okna dialogowego z informacją o czasie wykonania
        messagebox.showinfo("Czas wykonania funkcji", f"Funkcja wykonana w czasie: {elapsed_time:.2f} sekundy")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()
