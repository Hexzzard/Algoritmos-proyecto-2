import numpy as np
import matplotlib.pyplot as plt

# Parámetros del algoritmo genético
NUM_GENES = 10
NUM_POBLACION = 100
NUM_GENERACIONES = 100
PROB_MUTACION = 0.1

# Función objetivo (fitness)
def calcular_fitness(vector):
    return abs(np.sum(vector) - 1)

# Normalización de los valores del vector
def normalizar(vector):
    return vector / np.sum(vector)

# Crear un cromosoma aleatorio
def crear_cromosoma():
    return np.random.rand(NUM_GENES)

# Crear la población inicial
def crear_poblacion():
    return np.array([crear_cromosoma() for _ in range(NUM_POBLACION)])

# Selección de cromosomas utilizando ruleta
def seleccionar_cromosomas(poblacion, fitness):
    prob_acumulada = np.cumsum(fitness)
    r = np.random.rand(len(poblacion))
    seleccionados = []

    for rand in r:
        seleccionado = np.where(prob_acumulada >= rand)[0][0]
        seleccionados.append(poblacion[seleccionado])

    return np.array(seleccionados)

# Cruce de cromosomas utilizando punto de cruce
def cruzar_cromosomas(padres):
    hijos = []

    for i in range(0, len(padres), 2):
        padre1 = padres[i]
        padre2 = padres[i+1]
        punto_cruce = np.random.randint(1, NUM_GENES)
        hijo1 = np.concatenate((padre1[:punto_cruce], padre2[punto_cruce:]))
        hijo2 = np.concatenate((padre2[:punto_cruce], padre1[punto_cruce:]))
        hijos.extend([hijo1, hijo2])

    return np.array(hijos)

# Mutación de un cromosoma
def mutar(cromosoma):
    for i in range(len(cromosoma)):
        if np.random.rand() < PROB_MUTACION:
            cromosoma[i] = np.random.rand()
    return cromosoma

# Llenar la población con el mejor cromosoma de la generación anterior
def llenar_poblacion(poblacion, mejor_cromosoma):
    poblacion[-1] = mejor_cromosoma
    return poblacion

# Algoritmo genético
poblacion = crear_poblacion()
mejor_fitness_generacion = []

plt.figure()
plt.ion()

for generacion in range(NUM_GENERACIONES):
    # Evaluar el fitness de la población actual
    fitness_values = np.array([calcular_fitness(cromosoma) for cromosoma in poblacion])
    mejor_fitness = np.min(fitness_values)
    mejor_fitness_generacion.append(mejor_fitness)

    # Graficar el mejor fitness de cada generación
    plt.plot(generacion, mejor_fitness, 'bo')
    plt.pause(0.01)

    # Selección y cruce de cromosomas
    padres = seleccionar_cromosomas(poblacion, fitness_values)
    hijos = cruzar_cromosomas(padres)

    # Mutación de los hijos
    hijos_mutados = np.array([mutar(cromosoma) for cromosoma in hijos])

    # Llenar la población con el mejor cromosoma de la generación anterior
    poblacion = llenar_poblacion(hijos_mutados, poblacion[np.argmin(fitness_values)])

# Mostrar el mejor cromosoma de cada generación
for generacion, fitness_generacion in enumerate(mejor_fitness_generacion):
    print(f"Generación {generacion}: Mejor fitness = {fitness_generacion}")

plt.xlabel('Generación')
plt.ylabel('Mejor Fitness')
plt.title('Evolución del Mejor Fitness')
plt.ioff()
plt.show()