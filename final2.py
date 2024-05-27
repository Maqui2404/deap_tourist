import random
import numpy as np
from deap import base, creator, tools, algorithms

# Ejemplo de matriz de distancias entre 5 ciudades
distance_matrix = [
    [0, 2, 9, 10, 7],
    [2, 0, 6, 4, 3],
    [9, 6, 0, 8, 4],
    [10, 4, 8, 0, 5],
    [7, 3, 4, 5, 0]
]

N_CITIES = len(distance_matrix)

def eval_tsp(individual):
    distance = 0
    for i in range(len(individual) - 1):
        distance += distance_matrix[individual[i]][individual[i + 1]]
    distance += distance_matrix[individual[-1]][individual[0]]  # Return to the starting city
    return distance,

def get_user_input():
    num_cities = int(input("Ingrese el número de ciudades: "))
    cities = []
    for i in range(num_cities):
        distances = list(map(int, input(f"Ingrese las distancias desde la ciudad {i+1} a las demás (separadas por espacios): ").split()))
        cities.append(distances)
    return cities

def main():
    global distance_matrix
    distance_matrix = get_user_input()
    N_CITIES = len(distance_matrix)

    # Definir tipos de individuos y población
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # Configurar la caja de herramientas
    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(N_CITIES), N_CITIES)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Registrar la función de evaluación
    toolbox.register("evaluate", eval_tsp)

    # Registrar operadores genéticos
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Ejecutar el algoritmo genético
    population = toolbox.population(n=300)
    NGEN = 40
    CXPB = 0.7
    MUTPB = 0.2

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=stats, verbose=True)

    # Obtener el mejor individuo
    best_ind = tools.selBest(population, 1)[0]
    print('Best individual: ', best_ind)
    print('Distance: ', eval_tsp(best_ind)[0])
    print('Route: ', best_ind)

if __name__ == "__main__":
    main()
