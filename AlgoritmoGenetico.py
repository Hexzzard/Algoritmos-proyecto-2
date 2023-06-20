import numpy as np
import matplotlib.pyplot as plt

# Parámetros del algoritmo genético
tamano_poblacion = 100
tamano_cromosoma = 10
probabilidad_mutacion = 0.1
numero_generaciones = 100

# Función objetivo
def fitness(cromosoma):
    return abs(np.sum(cromosoma) - 1.0)

# Crear un cromosoma aleatorio
def crear_cromosoma():
    return np.random.random(tamano_cromosoma)

# Crear una población inicial
def crear_poblacion():
    return np.array([crear_cromosoma() for _ in range(tamano_poblacion)])

# Selección de cromosomas utilizando probabilidad acumulada
def seleccionar_cromosomas(poblacion):
    fitness_values = np.array([fitness(cromosoma) for cromosoma in poblacion])
    probabilidad_acumulada = np.cumsum(1.0 / (fitness_values + 1e-10))
    return poblacion[np.searchsorted(probabilidad_acumulada, np.random.random(tamano_poblacion))]

# Generar un número aleatorio
def generador_random():
    return np.random.random()

# Seleccionar el último cromosoma menor que un número aleatorio
def ultimo_cromosoma_menor_random(poblacion, numero_aleatorio):
    fitness_values = np.array([fitness(cromosoma) for cromosoma in poblacion])
    indices_ordenados = np.argsort(fitness_values)
    return poblacion[indices_ordenados[np.searchsorted(fitness_values[indices_ordenados], numero_aleatorio, side='right') - 1]]

# Extraer los padres de la población
def sacar_padres(poblacion):
    padres = []
    for _ in range(tamano_poblacion):
        padre1 = ultimo_cromosoma_menor_random(poblacion, generador_random())
        padre2 = ultimo_cromosoma_menor_random(poblacion, generador_random())
        padres.append((padre1, padre2))
    return padres

# Cruce de cromosomas
def cruzar_cromosomas(padres):
    hijos = []
    for padre1, padre2 in padres:
        punto_cruce = np.random.randint(1, tamano_cromosoma - 1)
        hijo = np.concatenate((padre1[:punto_cruce], padre2[punto_cruce:]))
        hijos.append(hijo)
    return np.array(hijos)

# Mutación de cromosomas
def mutar(cromosoma):
    for i in range(tamano_cromosoma):
        if np.random.random() < probabilidad_mutacion:
            cromosoma[i] = np.random.random()
    return cromosoma

# Llenar la población con el mejor individuo anterior
def llenar_poblacion(poblacion, mejor_anterior):
    poblacion[0] = mejor_anterior
    return poblacion

# Algoritmo genético
poblacion = crear_poblacion()
mejor_fitness_generacion = []

for generacion in range(numero_generaciones):
    # Evaluar el fitness de la población actual
    fitness_values = np.array([fitness(cromosoma) for cromosoma in poblacion])
    mejor_fitness = np.min(fitness_values)
    mejor_fitness_generacion.append(mejor_fitness)
    indice_mejor = np.argmin(fitness_values)
    mejor_individuo = poblacion[indice_mejor]

    # Selección y cruce de cromosomas
    padres = sacar_padres(poblacion)
    hijos = cruzar_cromosomas(padres)

    # Mutación de los hijos
    hijos_mutados = np.array([mutar(cromosoma) for cromosoma in hijos])

    # Llenar la población con el mejor individuo anterior
    poblacion = llenar_poblacion(hijos_mutados, mejor_individuo)

# Mostrar el mejor individuo de cada generación
for generacion, fitness_generacion in enumerate(mejor_fitness_generacion):
    print(f"Generación {generacion}: Mejor fitness = {fitness_generacion}")

# Graficar el mejor fitness de cada generación
plt.plot(range(numero_generaciones), mejor_fitness_generacion)
plt.xlabel('Generación')
plt.ylabel('Mejor Fitness')
plt.title('Evolución del Mejor Fitness')
plt.show()