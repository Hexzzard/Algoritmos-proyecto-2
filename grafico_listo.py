import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap

# Definir los colores en formato RGBA
colors = [(255, 255, 255, 255),      #Terreno
          (255, 0, 0, 128),          #Rojo
          (255, 165, 0, 128),        
          (255, 255, 0, 128),        #Amarillo 
          (46, 204, 113, 128),
          (0, 255, 0, 128),          #Verde
          (72, 201, 176, 128),
          (41, 128, 185, 128),       #Azul
          (142, 68, 173, 128),
          (127, 140, 141, 128)       #No moverse
          ]  

#Matplotlib trabaja con valores entre 0 y 1
colors = [(r/255, g/255, b/255, a/255) for r, g, b, a in colors]

# Crear el cmap personalizado
cmap = ListedColormap(colors)

# Variables globales, definen TODO
largo = 20
alto = 20
porcentaje_area_de_aparicion = 20
habitantes_primera_generacion = 20
numero_de_movimientos = 40
tiempo_entre_movimientos = 0.0001
agresividad = 1
seed = 42     #seeds probadas 322

#constantes globales
random.seed(seed)
np.random.seed(seed)
cantidad_de_clases = 9
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
            self.im = self.ax.imshow(self.matriz, cmap=cmap, interpolation='nearest', extent=[0, self.largo, 0, self.alto])
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
    def __init__(self, numero, cromosoma=None): #constructor
        self.numero = numero #el numero que ocupa dentro del arreglo de poblacion
        self.inicializarHabitante(cromosoma)
        self.movimientos = 0

    def inicializarHabitante(self, cromosoma=None): #inicializa los valores del habitante
        if cromosoma is None: #si no se ingresa un cromosoma, genera uno
            self.cromosoma = Crear_Cromosoma_Movimiento()
        else:
            self.cromosoma = cromosoma

        self.clase = np.argmax(self.cromosoma)+1 #la clase es la direccion donde tiene mas probabilidad de moverse
        
        self.combate = agresividad*random.random()/2 #probabilidad de cada individuo de ganar una pelea
        self.posicionar_habitante(alto, largo, porcentaje_area_de_aparicion)

    def posicionar_habitante(self, largo, alto, porcentaje_area_de_aparicion): #ubica al habitante en el mapa
        limite_largo = round(largo * (porcentaje_area_de_aparicion / 100)) #se define el area de aparicion
        while True: #iteramos hasta encontrar una posicion que este disponible
            posible_posicion_x = np.random.randint(0, limite_largo) 
            posible_posicion_y = np.random.randint(0, alto)
            if terreno.matriz[posible_posicion_y, posible_posicion_x] == 0:
                break
        self.coordenada_x = posible_posicion_x #asignamos las coordenadas al habitante
        self.coordenada_y = posible_posicion_y
        terreno.matriz[self.coordenada_y, self.coordenada_x] = self.clase #registramos al habitante en el terreno<----revisar

        coordenada = f'({self.coordenada_x},{self.coordenada_y})' #string que indica la posicion en la que se encuentra
        terreno.diccionario_coordenadas[coordenada] = self.numero #guardamos la posicion en el registro


    def moverse(self): #logica de movimiento del habitante
        vector_movimiento = seleccionar_posicion_aleatoria(self.cromosoma) #tomamos una posicion aleatoria para moverse
       
        
        if (self.coordenada_x != largo-1): #se mueve siempre cuando el movimiento sea valido, y si es que no ha llegado a la zona segura
            self.movimientos += 1
            if 0 <= self.coordenada_y + vector_movimiento[0] < alto and 0 <= self.coordenada_x + vector_movimiento[1] < largo:
                if terreno.matriz[self.coordenada_y + vector_movimiento[0]][self.coordenada_x + vector_movimiento[1]] == 0:
                    
                    terreno.matriz[self.coordenada_y][self.coordenada_x] = 0 #borramos la posicion anterior y registramos la nueva
                    
                    self.coordenada_x = self.coordenada_x + vector_movimiento[1]
                    self.coordenada_y = self.coordenada_y + vector_movimiento[0]
                    terreno.matriz[self.coordenada_y][self.coordenada_x] = self.clase

                    coordenada = f'({self.coordenada_x},{self.coordenada_y})' #string que indica la posicion en la que se encuentra
                    terreno.diccionario_coordenadas[coordenada] = self.numero #registramos la posicion en los registros
                #else:
                    #print("choco contra un habitante")
                    #funcion_matar()

def fitness(habitante):
    fit = (numero_de_movimientos)/(habitante.movimientos)# otra forma seria abs(habitante.movimientos-numero_de_movimientos)
    return fit

def Crear_Cromosoma_Movimiento(): #crea una lista con la probabilidad de moverse a cada posicion
    cromosoma_Movimiento = []
    for i in range(9): #creamos una lista con valores aleatorios del 0 al 100
        valor = np.random.randint(0, 100)
        cromosoma_Movimiento.append(valor)
    cromosoma_Movimiento = normalizar(cromosoma_Movimiento) #normalizamos el vector
    return cromosoma_Movimiento

indices_para_movimiento = np.arange(len(diccionario_vector_movimientos))
def seleccionar_posicion_aleatoria(vector): #selecciona una posicion aleatoria de un vector normalizado
    vector_normalizado = normalizar(vector)
    #print("normalizacion de vecto de probabilidad: ", vector_normalizado)
    #print("selecionado al azar por probabilidad: ", np.random.choice(vector , size=1, replace=False, p=vector_normalizado))
    #print("vector de probabilidad de movimiento: ", vector)
    indice_seleccionado = np.random.choice(indices_para_movimiento, size=1, replace=False, p=vector_normalizado)
    #print(indice_seleccionado)
    #print(diccionario_vector_movimientos[indice_seleccionado[0]])
    return diccionario_vector_movimientos[indice_seleccionado[0]]


def crear_primera_poblacion(): #crea la primera poblacion de habitantes
    poblacion = [] #arreglo que contiene a la poblacion
    for i in range(habitantes_primera_generacion):
        habitante = Habitante(i)
        poblacion.append(habitante)
    return poblacion 

def crear_siguiente_poblacion(sobrevivientes): #crea la siguiente poblacion
    poblacion = []  # arreglo que contiene a la poblacion
    fittest = 999
    if(len(sobrevivientes) == 1):#######crea poblacion de 21 habitantes <-------------
        for i in range(habitantes_primera_generacion):
            if i==generacion%habitantes_primera_generacion:
                cromosoma = sobrevivientes[0].cromosoma
                habitante = Habitante(i, cromosoma)
                poblacion.append(habitante)
                #print("el unico habitante tiene el numero: ", i)
            else:
                habitante = Habitante(i)
                poblacion.append(habitante)
    
        return poblacion
    
    #print("segunda gen:",sobrevivientes)
    for i in range(len(sobrevivientes)):
        if (sobrevivientes[i].movimientos < fittest):
            fittest = sobrevivientes[i].movimientos
    nueva_poblacion = []

    for i in range(len(sobrevivientes)):
        if i<10:
            dos_sobrevivientes = seleccionar_habitantes(sobrevivientes)
            nueva_poblacion.append(cruzar_cromosomas(dos_sobrevivientes)[0])
            nueva_poblacion.append(cruzar_cromosomas(dos_sobrevivientes)[1])
    
    for i in range(len(nueva_poblacion)):
        cromosoma = nueva_poblacion[i]
        habitante = Habitante(i, cromosoma)
        poblacion.append(habitante)
    if len(nueva_poblacion)!=habitantes_primera_generacion:
        for i in range(habitantes_primera_generacion-len(nueva_poblacion)):
            habitante = Habitante(len(nueva_poblacion)+i)
            poblacion.append(habitante)
    
    return poblacion
def cruzar_cromosomas(dos_sobrevivientes):
    dna_index = np.random.randint(1, 9)
    cromosoma_hijo1 = []
    cromosoma_hijo2 = []
    
    for i in range(dna_index):
        cromosoma_hijo1.append(dos_sobrevivientes[0].cromosoma[i])
        cromosoma_hijo2.append(dos_sobrevivientes[1].cromosoma[i])
    for i in range(dna_index, 9):
        cromosoma_hijo1.append(dos_sobrevivientes[0].cromosoma[i])
        cromosoma_hijo2.append(dos_sobrevivientes[1].cromosoma[i])
    return normalizar(mutacion(cromosoma_hijo1)), normalizar(mutacion(cromosoma_hijo2))

def mutacion(hijo):
    if np.random.randint(1, 20) == 20:
        index_modificado = np.random.randint(0, 8)
        valor_modificado = np.random.uniform(-1.0, 1.0)
        if valor_modificado < 0 and valor_modificado * -1 >= hijo[index_modificado]:
            hijo[index_modificado] = 0
            return hijo
        hijo[index_modificado] += valor_modificado
        return hijo
    return hijo
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
def normalizar(vector): #normaliza un vector / suma total de sus componentes = 1
    return vector / np.sum(vector)


def probabilidad(sobrevivientes):
    probabilidad = []
    for i in range(len(sobrevivientes)):
        probabilidad.append(fitness(sobrevivientes[i]))
    return normalizar(probabilidad)

def seleccionar_habitantes(sobrevivientes):
    return np.random.choice(sobrevivientes, size=2, replace=False, p=probabilidad(sobrevivientes))


def pelear(habitante1, habitante2): #funcion del felipe /matar habitantes
    #te añadi un parametro a los habitantes 'combate'
    #es como la probabilidad de que tiene ganar cada individuo una pelea
    #arreglo de 3 valores, % de ganar habitante 1, % de ganar habitante 2, % de empate
    cromosoma = [habitante1.combate, habitante2.combate, 1-habitante1.combate-habitante2.combate]
    accion = seleccionar_posicion_aleatoria(cromosoma)  # Seleccionar al azar el índice del gen perdedor
    if accion == 0:
        poblacion.remove(habitante1)  # Eliminar al gen perdedor 1
        print("se elimino 1 habitante")
    if accion == 1:
        print("se elimino 1 habitante")
        poblacion.remove(habitante2)  # Eliminar al gen perdedor 2
    #si es 2 es empate y no hace nada

    #ahi lo terminas, fijate lo de terreno.diccionario_coordenadas, ese es el seleccionador
    #le das una coordenada y te devuelve el individuo
    #modifica el movimiento, ahora si pilla a alguien mandalo a pelear
def graficar_supervivientes_por_generacion(generaciones, numero_supervivientes_por_generacion, lista_de_supervivientes_por_clase_y_generacion):
    grafico_eje_x = list(range(1, generaciones)) #generamos el eje x del grafico
    
    for i in range(cantidad_de_clases): #graficamos los supervivientes de cada clase
        grafico_eje_y = lista_de_supervivientes_por_clase_y_generacion[i] 
        plt.plot(grafico_eje_x, grafico_eje_y, color=colors[i+1], alpha=1, label=f'Preferencia {diccionario_movimientos[i]}')
        
    plt.plot(grafico_eje_x, numero_supervivientes_por_generacion, color='black', alpha=1, label='Sobrevivientes totales')
    #los colores de la clase de los individuos se mantendran, y el total sera de color negro
    plt.xlabel('N° Generacion')
    plt.ylabel('Cantidad de sobrevivientes')
    plt.legend(fontsize='small')
    plt.title(f'Resumen de supervivientes, seed: {seed}')
    plt.show()


#variables utilizadas dentro del ciclo
generacion = 1
juego_activo = True
terreno = Terreno(largo, alto)
poblacion = []
poblacion_sobrevivientes = []

lista_numero_supervivientes_por_generacion = []
lista_supervivientes_por_clases_y_generacion = [[],[],[],[],[],[],[],[],[]]

#ciclo del juego
while True:
    terreno.inicializarTerreno() #regeneramos el terreno
    if (len(poblacion_sobrevivientes) == 0): #si no hay supervivientes se crea una generacion por azar
        if (generacion != 1):
            print('No hubo supervivientes')
            print('Fin del juego, cierra le ventana para ver las estadisticas')
            plt.pause(999999)
            lista_numero_supervivientes_por_generacion.append(len(poblacion_sobrevivientes)) #guardamos las estadisticas
            for i in range(cantidad_de_clases): #guardamos los sobrevivientes en base a cada clase
                lista_supervivientes_por_clases_y_generacion[i].append(0) #inicializamos todos con 0
            graficar_supervivientes_por_generacion(generacion, lista_numero_supervivientes_por_generacion, lista_supervivientes_por_clases_y_generacion)
            break
        else:
            poblacion = crear_primera_poblacion()
            
    else:
        print(f'sobrevivientes numeros: {poblacion_sobrevivientes}')
        habitantes_sobrevivientes = [poblacion[i] for i in poblacion_sobrevivientes] #convertimos las id en los objetos
        poblacion = crear_siguiente_poblacion(habitantes_sobrevivientes) #creamos la siguiente poblacion con la poblacion de sobrevivientes
        lista_numero_supervivientes_por_generacion.append(len(poblacion_sobrevivientes)) #guardamos las estadisticas
        for i in range(cantidad_de_clases): #guardamos los sobrevivientes en base a cada clase
            lista_supervivientes_por_clases_y_generacion[i].append(0) #inicializamos todos con 0
        if len(habitantes_sobrevivientes)>0:
            for superviviente in habitantes_sobrevivientes: #y incrementamos el valor en base a las clases de los supervivientes
                lista_supervivientes_por_clases_y_generacion[superviviente.clase-1][generacion-2] +=1
        
    for i in range (numero_de_movimientos): 
        for habitante in poblacion: #en cada turno movemos a todos los habitantes de la poblacion
            habitante.moverse()
        terreno.MostrarGrafica(generacion, i+1) #creamos/actualizamos la grafica
        plt.pause(tiempo_entre_movimientos)   
        if len(plt.get_fignums()) == 0: #si es que no hay figuras activas finaliza el ciclo
            print('Fin de la muestra')
            juego_activo = False
            break

    if(not juego_activo): #para salir del ciclo definitivamente

        graficar_supervivientes_por_generacion(generacion, lista_numero_supervivientes_por_generacion, lista_supervivientes_por_clases_y_generacion)
        break
    poblacion_sobrevivientes = sobrevivientes()
    generacion +=1
