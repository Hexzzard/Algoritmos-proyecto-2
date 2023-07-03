import numpy as np
import matplotlib.pyplot as plt
import random
import asyncio
# Variables globales, definen TODO
largo = 20
alto = 20
porcentaje_area_de_aparicion = 20
habitantes_primera_generacion = 20
numero_de_movimientos = 40
tiempo_entre_movimientos = 0.1
agresividad = 1

class Terreno:
    def __init__(self, largo, alto): #constructor
        self.largo = largo
        self.alto = alto
        self.inicializarTerreno()
        self.fig, self.ax = plt.subplots()
        self.im = None

    def inicializarTerreno(self): #define los atributos que necesitan resetearse
        self.matriz = np.zeros((self.largo, self.alto))
        self.diccionario_coordenadas = {} #registro de las ubicaciones de los habitantes

    def MostrarGrafica(self, generacion, movimiento): #muestra la grafica del entorno
        if self.im is None: #si no hay una imagen, se crea 
            self.im = self.ax.imshow(self.matriz, cmap='Blues', interpolation='nearest', extent=[0, self.largo, 0, self.alto])
            self.ax.set_xlim(0, self.largo)
            self.ax.set_ylim(0, self.alto)
            self.ax.set_xlabel('Eje X')
            self.ax.set_ylabel('Eje Y')
            plt.title(f'Generacion {generacion}, Movimiento {movimiento}')

        else: #y si existe la actualizamos
            self.im.set_data(self.matriz)  
            self.ax.set_xlim(0, self.largo)
            self.ax.set_ylim(0, self.alto)
            plt.title(f'Generacion {generacion}, Movimiento {movimiento}')

class Habitante:
    def __init__(self, numero): #constructor
        self.numero = numero #el numero que ocupa dentro del arreglo de poblacion
        self.inicializarHabitante()
        
    def inicializarHabitante(self): #define los atributos que no dependen del constructor
        self.cromosoma  = Crear_Cromosoma_Movimiento()
        self.clase = np.argmax(self.cromosoma) #la clase es la direccion donde tiene mas probabilidad de moverse
        
        self.combate = agresividad*random.random()/2 #probabilidad de cada individuo de ganar una pelea
        self.posicionar_habitante(largo, alto, porcentaje_area_de_aparicion)

    def posicionar_habitante(self, largo, alto, porcentaje_area_de_aparicion): #ubica al habitante en el mapa
        limite_largo = round(largo * (porcentaje_area_de_aparicion / 100)) #se define el area de aparicion
        while True: #iteramos hasta encontrar una posicion que este disponible
            posible_posicion_x = np.random.randint(0, limite_largo) 
            posible_posicion_y = np.random.randint(0, alto)
            if terreno.matriz[posible_posicion_y, posible_posicion_x] == 0:
                break

        self.coordenada_x = posible_posicion_x #asignamos las coordenadas al habitante
        self.coordenada_y = posible_posicion_y
        terreno.matriz[self.coordenada_y, self.coordenada_x] = self.clase #registramos al habitante en el terreno

        coordenada = f'({self.coordenada_x},{self.coordenada_y})' #string que indica la posicion en la que se encuentra
        terreno.diccionario_coordenadas[coordenada] = self.numero #guardamos la posicion en el registro

    def moverse(self): #logica de movimiento del habitante
        direccion_movimiento = seleccionar_posicion_aleatoria(self.cromosoma) #tomamos una posicion aleatoria para moverse
        vector_movimiento = diccionario_vector_movimientos[direccion_movimiento] #traducimos la direccion a un vector con ayuda de un diccionario
        
        if (self.coordenada_x != largo-1): #se mueve siempre cuando el movimiento sea valido, y si es que no ha llegado a la zona segura
            if 0 <= self.coordenada_y + vector_movimiento[0] < alto and 0 <= self.coordenada_x + vector_movimiento[1] < largo:
                if terreno.matriz[self.coordenada_y + vector_movimiento[0]][self.coordenada_x + vector_movimiento[1]] == 0:
        
                    terreno.matriz[self.coordenada_y][self.coordenada_x] = 0 #borramos la posicion anterior y registramos la nueva
                    self.coordenada_x = self.coordenada_x + vector_movimiento[1]
                    self.coordenada_y = self.coordenada_y + vector_movimiento[0]
                    terreno.matriz[self.coordenada_y][self.coordenada_x] = self.clase

                    coordenada = f'({self.coordenada_x},{self.coordenada_y})' #string que indica la posicion en la que se encuentra
                    terreno.diccionario_coordenadas[coordenada] = self.numero #registramos la posicion en los registros

diccionario_vector_movimientos = { #traduce la posicion a moverse en un vector
    0: [1, 0],   # Norte
    1: [1, 1],   # Noreste
    2: [0, 1],   # Este
    3: [-1, 1],  # Sureste
    4: [-1, 0],  # Sur
    5: [-1, -1], # Suroeste
    6: [0, -1],  # Oeste
    7: [1, -1],  # Noroeste
    8: [0, 0]    # No movimiento
}

diccionario_movimientos = { #traduce la posicion a moverse en un string con la posicion
    0: 'Norte',
    1: 'Noreste',
    2: 'Este',
    3: 'Sureste',
    4: 'Sur',
    5: 'Suroeste',
    6: 'Oeste',
    7: 'Noroeste',
    8: 'No movimiento'
}

def Crear_Cromosoma_Movimiento(): #crea una lista con la probabilidad de moverse a cada posicion
    cromosoma_Movimiento = []
    for i in range(9): #creamos una lista con valores aleatorios del 0 al 100
        valor = np.random.randint(0, 100)
        cromosoma_Movimiento.append(valor)
    cromosoma_Movimiento = normalizar(cromosoma_Movimiento) #normalizamos el vector

    return cromosoma_Movimiento

def normalizar(vector): #normaliza un vector / suma total de sus componentes = 1
    return vector / np.sum(vector)

def seleccionar_posicion_aleatoria(vector): #selecciona una posicion aleatoria de un vector normalizado
    rnd = np.random.random() #se toma el primer elemento, tal que su frecuencia acumulada sea mayor al valor generado
    acumulado = 0
    posicion = 0
    for elemento in vector: 
        acumulado += elemento
        if acumulado > rnd:
            return posicion
        posicion += 1
    return posicion - 1 #si todos son menores se retorna el ultimo elemento de la lista

def crear_primera_poblacion(): #crea la primera poblacion de habitantes
    poblacion = [] #arreglo que contiene a la poblacion
    for i in range(habitantes_primera_generacion):
        habitante = Habitante(i)
        poblacion.append(habitante)
    return poblacion 

def crear_siguiente_poblacion(): #crea la primera poblacion de habitantes
    poblacion = [] #arreglo que contiene a la poblacion
    for i in range(habitantes_primera_generacion):
        habitante = Habitante(i)
        poblacion.append(habitante)
    return poblacion 

def sobrevivientes (): #busca los sobrevivientes
    sobrevivientes = [] 
    for i in range(alto): 
        try: #puede retornar error al no existir un registro para una determinada coordenada
            clave = f'({largo-1},{i})' #busca las coincidencias de la ultima fila
            valor = terreno.diccionario_coordenadas[clave]
            sobrevivientes.append(valor)

        except KeyError: #ignoramos los errores
            continue
    return sobrevivientes

def pelear(habitante1, habitante2): #funcion del felipe /matar habitantes
    #te añadi un parametro a los habitantes 'combate'
    #es como la probabilidad de que tiene ganar cada individuo una pelea
    #arreglo de 3 valores, % de ganar habitante 1, % de ganar habitante 2, % de empate
    cromosoma = [habitante1.combate, habitante2.combate, 1-habitante1.combate-habitante2.combate]
    accion = seleccionar_posicion_aleatoria(cromosoma)  # Seleccionar al azar el índice del gen perdedor
    if accion == 0:
        poblacion.remove(habitante1)  # Eliminar al gen perdedor 1
    if accion == 1:
        poblacion.remove(habitante2)  # Eliminar al gen perdedor 2
    #si es 2 es empate y no hace nada

    #ahi lo terminas, fijate lo de terreno.diccionario_coordenadas, ese es el seleccionador
    #le das una coordenada y te devuelve el individuo
    #modifica el movimiento, ahora si pilla a alguien mandalo a pelear

#variables utilizadas dentro del ciclo
generacion = 1
juego_activo = True
terreno = Terreno(largo, alto)
poblacion = []
poblacion_sobrevivientes = []

async def pasos(habitante):
        habitante.moverse()
        if (habitante.coordenada_x==19):
            print("Habitante en (",habitante.coordenada_x,",", habitante.coordenada_y,") Sobrevivio")

async def asincrono():      
    for i in range(numero_de_movimientos):
        for habitante in poblacion: #en cada turno movemos a todos los habitantes de la poblacion
            await asyncio.ensure_future(pasos(habitante))
        terreno.MostrarGrafica(generacion, i+1)
        plt.pause(tiempo_entre_movimientos)
        if len(plt.get_fignums()) == 0: #si es que no hay figuras activas finaliza el ciclo
            print('Fin de la muestra')
            return False
        
    return True   

while True:
    terreno.inicializarTerreno() #regeneramos el terreno
    if (len(poblacion_sobrevivientes) == 0): #si no hay supervivientes se crea una generacion por azar
        poblacion = crear_primera_poblacion()
        print()
        if (generacion != 1):
            print('no hubo supervivientes')
    else:
        print(f'sobrevivientes: {poblacion_sobrevivientes}') 
        poblacion = crear_siguiente_poblacion() #por implementar
    
    loop = asyncio.get_event_loop() #inicializa el loop para hacer los pasos
   
    juego_activo =  loop.run_until_complete(asincrono())#comienza a hacer las tareas que se dejan para el loop en ensure_future
    if(not juego_activo): #para salir del ciclo definitivamente
        break
    poblacion_sobrevivientes = sobrevivientes()
    generacion +=1

#loop.close()


#Falta:
#terminar el gameloop cuando se llege a la zona segura
#mostrar un solo grafico, se puede hacer pero hay que convertirlo en asyncronico, hice un par de intentos pero no me salio
#logica de segundas generaciones
#lo que sea que halla que hacer con el fitness


#Opcionales:
#pintar a los cuadrados segun cual sea la direccion con mayor probabilidad
#matar
#vision

#PD: si añaden parametros opcionales, tiene que ser con genetica, la wea es demostrar si ganan los que tienen o no el gen
#o por ejemplo los que tienen mayor o menor vision.
#y estudien la logica de objetos clases en python.

#version lo que hice en 3 horas