Hexzzard
hexzzard
Recuperando las Malvinas

pipeeav3 — 19/10/2022 22:41
O es a partir de las 15.00 nomas
Hexzzard — 19/10/2022 22:41
antes de las 10
pipeeav3 — 19/10/2022 22:41
Ah dale
Hexzzard — 19/10/2022 22:41
pero teni que tener suerte de que no halla alguien presentando a esa hora
pipeeav3 — 19/10/2022 22:41
Osea de 8 a 10
Y dps de 3 a 5
Hexzzard — 19/10/2022 22:41
sip
pipeeav3 — 19/10/2022 22:41
Esos son los plazos
Dale
Gracias
pipeeav3 — 24/11/2022 20:07
Buena hexzzard cómo estás?
Oye te quería hacer una consulta 😅
Hexzzard — 24/11/2022 20:11
en lo de interfaces?
pipeeav3 — 24/11/2022 20:11
si era para consultarte en que formato enviaste los graficos al telegram
Hexzzard — 24/11/2022 20:11
blob
pipeeav3 — 24/11/2022 20:17
lo estudiare😅
gracias
pipeeav3 — 11/04/2023 20:06
Hola bro
Oye sabes cuándo el profe le pondrá nota a los programas?
Hexzzard — 11/04/2023 20:57
La otra semana se supone
pipeeav3 — 11/04/2023 21:00
Ah vale será junto con la prueba entonces
pipeeav3 — 12/04/2023 13:33
Fuiste a clases hoy?😅
Hexzzard — 12/04/2023 14:38
Si fui
La prueba es la semana del 26
pipeeav3 — 12/04/2023 14:39
Ah vale
Y la otra semana que hay?
Talleres?
Hexzzard — 12/04/2023 14:39
Repaso
Y eso
pipeeav3 — 12/04/2023 14:39
Ah buenísima
Gracias
pipeeav3 — 17/04/2023 18:24
Hola bro
Una consulta pudiste hacer el taller  7 y 8?
pipeeav3 — 18/04/2023 3:57
Tipo de archivo adjunto: spreadsheet
Taller_Formativo_7_Problemas_de_minimizacion_y_restricciones_de_tipo_mayor_o_igual_que.xlsx
11.64 KB
Hexzzard — 18/04/2023 3:57
Tipo de archivo adjunto: spreadsheet
xdxd3.xlsx
14.73 KB
pipeeav3 — 19/04/2023 17:10
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

#Definir restricciones
A = np.array([[1,3],[1,2],[0.5,1]])
Expandir
Metodo_Grafico.py
2 KB
ese metodo grafico me pasaron
pipeeav3 — 19/04/2023 17:21
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

# Definimos el problema de programación lineal
# Maximizar: 2x + 3y
Expandir
Prueba_metodo_grafico.py
2 KB
y ese  me quedo utilizando chatgpt como base
pipeeav3 — 29/05/2023 17:11
Tipo de archivo adjunto: acrobat
Taller_2_5_1.pdf
79.83 KB
ese metodo habia usado
y esa era la otra forma que tampoco llego
Imagen
pipeeav3 — 29/05/2023 22:22
creo que lo hice
0,4116 = 0,4116
eso me dio
pipeeav3 — 13/06/2023 19:09
me ayudas con lo del mellado estoy pa la caga y eso que le di mas espacio al disco:(
pipeeav3 — ayer a las 21:40
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del algoritmo genético
tamano_poblacion = 100
tamano_cromosoma = 10
Expandir
aaaa.txt
4 KB
eso es mi pequeño avance de hoy intentando aplicar los conceptos y intentando pedir a chatgpt le faltan hartas cosas si sjjjsjs
lo tengo dinamico pero no tengo el cambio de datos xd
pipeeav3 — hoy a las 0:52
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del algoritmo genético
NUM_GENES = 10
NUM_POBLACION = 100
Expandir
algo.txt
4 KB
﻿
pipeeav3
pipeeav3#0920
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