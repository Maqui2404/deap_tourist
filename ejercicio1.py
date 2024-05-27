import random
import numpy as np
from deap import base, creator, tools, algorithms

# Definir los datos del problema
ITEMS = [
    {'value': 60, 'weight': 10},
    {'value': 100, 'weight': 20},
    {'value': 120, 'weight': 30}
]
MAX_WEIGHT = 50
N_ITEMS = len(ITEMS)

# Definir tipos de individuos y población
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Configurar la caja de herramientas
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=N_ITEMS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Definir la función de evaluación
def evaluate(individual):
    value = 0
    weight = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            value += ITEMS[i]['value']
            weight += ITEMS[i]['weight']
        if weight > MAX_WEIGHT:
            return 0,
    return value,

toolbox.register("evaluate", evaluate)

# Registrar operadores genéticos
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Ejecutar el algoritmo genético
population = toolbox.population(n=300)
NGEN = 40
CXPB = 0.5
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
print('Value: ', evaluate(best_ind)[0])
print('Items selected: ', [ITEMS[i] for i in range(len(best_ind)) if best_ind[i] == 1])
