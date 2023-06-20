import numpy as np
import matplotlib.pyplot as plt
import time

#variables globales, definen TODO 
largo = 20
alto = 20
porcentaje_area_de_aparicion = 20
habitantes_primera_generacion = 20

class Terreno:
    def __init__(self, largo, alto): #constructor
        self.largo = largo
        self.alto = alto

    def inicializarTerreno (self):
        self.matriz = np.zeros((self.largo, self.alto))

    def MostrarGrafica (self): #grafica la matriz
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.matriz, cmap='Blues', interpolation='nearest', extent=[0, self.matriz.shape[1], 0, self.matriz.shape[0]])
        self.ax.set_xlim(0, self.matriz.shape[1])
        self.ax.set_ylim(0, self.matriz.shape[0])
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        plt.show()
    
    def ActualizarGrafica (self): #asincronico, no me funciono :c
        print(self.matriz)
        self.im.set_data(self.matriz)  # Actualizar los datos de la imagen
        self.ax.set_xlim(0, self.matriz.shape[1])  # Actualizar los límites del eje x
        self.ax.set_ylim(0, self.matriz.shape[0])  # Actualizar los límites del eje y
        plt.show()
        #plt.draw()  # Volver a dibujar el gráfico con los cambios

terreno = Terreno(largo,alto) #creamos el terreno
terreno.inicializarTerreno()

#Nota: Los habitantes necesitan el terreno para generarse

class Habitante:
    def inicializarHabitante (self): #llama a las funciones para crear los atributos del habitante
        movimiento = Crear_Cromosoma_Movimiento()
        cromosoma = normalizar(movimiento)
        self.cromosoma = cromosoma
        self.coordenada_x, self.coordenada_y = posicionar_habitante(largo, alto, porcentaje_area_de_aparicion)
    
    def moverse(self): #movimiento
        direccion_movimiento = direccion(self.cromosoma)
        vector_movimiento = diccionario_vector_movimientos[direccion_movimiento]
        print(self.coordenada_y, vector_movimiento[0])
        if(self.coordenada_y+vector_movimiento[0] < alto and self.coordenada_y+vector_movimiento[0] > 0):
            if(self.coordenada_x+vector_movimiento[1] < largo and self.coordenada_x+vector_movimiento[1] > 0):
                if (terreno.matriz[self.coordenada_y+vector_movimiento[0]][self.coordenada_x+vector_movimiento[1]]==0): #se mueve siempre que este vacio la posicion destino
                    terreno.matriz[self.coordenada_y][self.coordenada_x]= 0
                    self.coordenada_x = self.coordenada_x+vector_movimiento[1]
                    self.coordenada_y = self.coordenada_y+vector_movimiento[0]
                    terreno.matriz[self.coordenada_y][self.coordenada_x]= 1                    


diccionario_vector_movimientos = {
    0: [ 1, 0], #Norte
    1: [ 1, 1], #Noreste
    2: [ 0, 1], #Este
    3: [-1, 1], #Sureste
    4: [-1, 0], #Sur
    5: [-1,-1], #Suroeste
    6: [ 0,-1], #Oeste
    7: [ 1,-1], #Noroeste
    8: [ 0, 0]  #No movimiento
}

diccionario_movimientos = { #es de bonito
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
def Crear_Cromosoma_Movimiento (): #crea un array con valores aleatorios indicando la % de moverse a un lado
    cromosoma_Movimiento = [] #las direcciones estan en base a diccionario_Movimientos
    for i in range(9):
        valor = np.random.randint(0, 100)
        cromosoma_Movimiento.append(valor)
    return cromosoma_Movimiento
    
def normalizar(vector): #devuelve un vector, tal que la suma de sus componentes de 1
    return vector / np.sum(vector)

def direccion(vector): #retorna la posicion del arreglo que se usara
    rnd = np.random.random()
    acumulado = 0
    posicion = 0
    for elemento in vector:
        acumulado += elemento
        if acumulado > rnd:
            return posicion
        posicion +=1
    return posicion-1

def posicionar_habitante(largo, alto, porcentaje_area_de_aparicion): #ubica a los habitantes en el terreno
    limite_largo = round(largo * (porcentaje_area_de_aparicion / 100))
    posicion_x = np.random.randint(0, limite_largo)
    posicion_y = np.random.randint(0, alto)

    while (terreno.matriz[posicion_y,posicion_x]!= 0): #si hay un habitante en la posicion buscara otra
        posicion_x = np.random.randint(0, limite_largo)
        posicion_y = np.random.randint(0, alto)

    terreno.matriz[posicion_y,posicion_x]= 1

    return posicion_x,posicion_y

poblacion = []
for i in range(habitantes_primera_generacion):
    nombre_habitante = f"Habitante {i+1}"  # Nombre del habitante
    habitante = Habitante()  # Crear una instancia de la clase Habitante
    habitante.inicializarHabitante()
    poblacion.append(habitante)

#game loop
while True:
    for habitante in poblacion:
        habitante.moverse()
    terreno.MostrarGrafica()
    time.sleep(1) #tiempo entre graficos

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