from flask import Flask, request, jsonify, render_template
import random
import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

distance_matrix = [
    [0, 1100, 1000, 1300, 300, 556, 769, 200, 300, 800],  # Lima
    [1100, 0, 510, 380, 1134, 1736, 1608, 1240, 900, 340],  # Cusco
    [1000, 510, 0, 450, 930, 1500, 1380, 1120, 760, 440],  # Arequipa
    [1300, 380, 450, 0, 1350, 1920, 1780, 1420, 1080, 620],  # Puno
    [300, 1134, 930, 1350, 0, 831, 1045, 380, 460, 950],  # Ica
    [556, 1736, 1500, 1920, 831, 0, 207, 440, 760, 1500],  # Trujillo
    [769, 1608, 1380, 1780, 1045, 207, 0, 650, 920, 1350],  # Chiclayo
    [200, 1240, 1120, 1420, 380, 440, 650, 0, 500, 850],  # Nazca
    [300, 900, 760, 1080, 460, 760, 920, 500, 0, 1100],  # Paracas
    [800, 340, 440, 620, 950, 1500, 1350, 850, 1100, 0],  # Huaraz
]

city_names = ["Lima", "Cusco", "Arequipa", "Puno", "Ica", "Trujillo", "Chiclayo", "Nazca", "Paracas", "Huaraz"]
city_descriptions = {
    "Lima": "Capital del Perú, conocida por sus museos, plazas históricas y gastronomía.",
    "Cusco": "Antigua capital del Imperio Inca, famosa por sus ruinas arqueológicas y cercanía a Machu Picchu.",
    "Arequipa": "Conocida como la Ciudad Blanca, famosa por su arquitectura colonial y el Cañón del Colca.",
    "Puno": "Ciudad a orillas del Lago Titicaca, famosa por sus festivales y cultura aymara.",
    "Ica": "Conocida por sus bodegas de vino y la cercana Huacachina, un oasis en el desierto.",
    "Trujillo": "Ciudad costera conocida por sus sitios arqueológicos como Chan Chan y Huacas del Sol y de la Luna.",
    "Chiclayo": "Conocida como la Capital de la Amistad, cerca de las tumbas reales de Sipán.",
    "Nazca": "Famosa por las Líneas de Nazca, geoglifos antiguos en el desierto.",
    "Paracas": "Conocida por la Reserva Nacional de Paracas y las Islas Ballestas.",
    "Huaraz": "Ubicada en la cordillera de los Andes, conocida por sus paisajes montañosos y trekking."
}
N_CITIES = len(distance_matrix)

def eval_tsp(individual):
    distance = 0
    for i in range(len(individual) - 1):
        distance += distance_matrix[individual[i]][individual[i + 1]]
    distance += distance_matrix[individual[-1]][individual[0]]  # Return to the starting city
    return distance,

def recommend_nearby_cities(destination, max_distance=500):
    nearby_cities = []
    for i, distance in enumerate(distance_matrix[destination]):
        if distance > 0 and distance <= max_distance:
            nearby_cities.append(city_names[i])
    return nearby_cities

@app.route('/')
def index():
    return render_template('index.html', cities=city_names)

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.json
    start_city = data['start_city']
    end_city = data['end_city']

    # Definir tipos de individuos y población
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(N_CITIES), N_CITIES)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", eval_tsp)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

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

    best_ind = tools.selBest(population, 1)[0]

    # Obtener la ruta desde start_city hasta end_city
    best_route = [start_city] + [i for i in best_ind if i != start_city and i != end_city] + [end_city]
    best_distance = eval_tsp(best_ind)[0]

    # Recomendar ciudades en el camino
    recommended_cities_on_route = []
    for i in range(len(best_route) - 1):
        if best_route[i] != start_city and best_route[i] != end_city:
            recommended_cities_on_route.append(city_names[best_route[i]])

    # Recomendar ciudades cercanas al destino
    recommended_cities_near_destination = recommend_nearby_cities(end_city)

    return jsonify({
        'route': [city_names[i] for i in best_route],
        'distance': best_distance,
        'recommended_cities_on_route': recommended_cities_on_route,
        'recommended_cities_near_destination': recommended_cities_near_destination,
        'city_descriptions': {city: city_descriptions[city] for city in city_names}
    })

@app.route('/resource_management')
def resource_management():
    return render_template('resource_management.html')

@app.route('/knapsack', methods=['POST'])
def knapsack():
    data = request.json
    ITEMS = data['items']
    MAX_WEIGHT = data['max_weight']
    N_ITEMS = len(ITEMS)

    # Definir tipos de individuos y población
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

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
    selected_items = [ITEMS[i] for i in range(len(best_ind)) if best_ind[i] == 1]

    # Graficar la evolución del valor máximo
    gen = logbook.select("gen")
    max_fit = logbook.select("max")
    avg_fit = logbook.select("avg")

    plt.plot(gen, max_fit, label="Máximo")
    plt.plot(gen, avg_fit, label="Promedio")
    plt.xlabel("Generación")
    plt.ylabel("Valor")
    plt.title("Evolución del Valor en el Problema de la Mochila")
    plt.legend(loc="upper left")
    plt.grid()

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({
        'best_ind': best_ind,
        'value': evaluate(best_ind)[0],
        'selected_items': selected_items,
        'plot_url': plot_url
    })

if __name__ == '__main__':
    app.run(debug=True)
