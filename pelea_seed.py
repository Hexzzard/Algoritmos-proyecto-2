import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap

# Variables globales, definen TODO
largo = 15
alto = 15
porcentaje_area_de_aparicion = 20
habitantes_primera_generacion = 10
numero_de_movimientos = 40
tiempo_entre_movimientos = 0.1
agresividad = 1
seed = 23122342
random.seed(seed)
np.random.seed(seed)

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

class Terreno:
    def __init__(self, largo, alto): #constructor
        self.largo = largo
        self.alto = alto
        self.inicializarTerreno()
        self.fig, self.ax = plt.subplots()
        self.im = None

    def inicializarTerreno(self): #define los atributos que necesitan resetearse
        self.matriz = (np.zeros((self.largo, self.alto)))
        self.diccionario_coordenadas = {} #registro de las ubicaciones de los habitantes
       
    def MostrarGrafica(self, generacion, movimiento): #muestra la grafica del entorno
           
        if self.im is None: #si no hay una imagen, se crea 
            self.im = self.ax.imshow(np.flipud(np.transpose(self.matriz)), cmap=cmap, interpolation='nearest', extent=[0, self.largo, 0, self.alto])
            self.ax.set_xlim(0, self.largo)
            self.ax.set_ylim(0, self.alto)
            self.ax.set_xlabel('Eje X')
            self.ax.set_ylabel('Eje Y')
            plt.title(f'Generacion {generacion}, Movimiento {movimiento}')

        else: #y si existe la actualizamos
            self.im.set_data(np.flipud(np.transpose(self.matriz)))
            self.ax.set_xlim(0, self.largo)
            self.ax.set_ylim(0, self.alto)
            plt.title(f'Generacion {generacion}, Movimiento {movimiento}')

class Habitante:
    def __init__(self, numero): #constructor
        self.numero = numero #el numero que ocupa dentro del arreglo de poblacion
        self.inicializarHabitante()
        self.movimientos = 0
        self.evasion = random.random() #genera un numero al azar en el rango [0, 1).
        self.agresividad = random.random()# azar rango [0, 1).

    def inicializarHabitante(self): #define los atributos que no dependen del constructor
        self.cromosoma = Crear_Cromosoma_Movimiento()
        self.clase = np.argmax(self.cromosoma) #la clase es la direccion donde tiene mas probabilidad de moverse
        if self.clase==0:
            self.clase = 1
        self.combate = agresividad*random.random()/2 #probabilidad de cada individuo de ganar una pelea
        self.posicionar_habitante(alto, largo, porcentaje_area_de_aparicion)

    def posicionar_habitante(self, largo, alto, porcentaje_area_de_aparicion): #ubica al habitante en el mapa
        limite_largo = round(largo * (porcentaje_area_de_aparicion / 100)) #se define el area de aparicion

        while True: #iteramos hasta encontrar una posicion que este disponible
            posible_posicion_x = np.random.randint(0, limite_largo) 
            posible_posicion_y = np.random.randint(0, alto-1)
            if terreno.matriz[posible_posicion_x, posible_posicion_y] == 0:
                break
        self.coordenada_x = posible_posicion_x #asignamos las coordenadas al habitante
        self.coordenada_y = posible_posicion_y
        terreno.matriz[self.coordenada_x, self.coordenada_y] = self.clase #registramos al habitante en el terreno<----revisar
        coordenada = f'({self.coordenada_x},{self.coordenada_y})' #string que indica la posicion en la que se encuentra
        terreno.diccionario_coordenadas[coordenada] = self.numero #guardamos la posicion en el registro


    def moverse(self): #logica de movimiento del habitante
        vector_movimiento = seleccionar_posicion_aleatoria(self.cromosoma) #tomamos una posicion aleatoria para moverse
        proximo_x = self.coordenada_x + vector_movimiento[0]
        proximo_y = self.coordenada_y + vector_movimiento[1]
        if (self.coordenada_x != largo-1): #se mueve siempre cuando el movimiento sea valido, y si es que no ha llegado a la zona segura
            self.movimientos += 1
            if 0 <= proximo_y < alto and 0 <= proximo_x < largo:
                if terreno.matriz[proximo_x][proximo_y] == 0:
                    terreno.matriz[self.coordenada_x][self.coordenada_y] = 0 #borramos la posicion anterior y registramos la nueva
                    #print("Clase de los habitantes: ",self.clase) <------------ numeros enteros del 0-7??
                    self.coordenada_x = proximo_x
                    self.coordenada_y = proximo_y
                    terreno.matriz[self.coordenada_x][self.coordenada_y] = self.clase
                    
                    coordenada = f'({self.coordenada_x},{self.coordenada_y})' #string que indica la posicion en la que se encuentra
                    terreno.diccionario_coordenadas[coordenada] = self.numero #registramos la posicion en los registros
                else:

                    if self.coordenada_x != proximo_x and self.coordenada_y != proximo_y:
                        
                        pelear((self.coordenada_x, self.coordenada_y) , (proximo_x, proximo_y), self)

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

def pelear(posicion_habitante1, posicion_habitante2, habitante1): #funcion del felipe /matar habitantes
    #terreno.matriz[posicion_habitante1[0]][posicion_habitante1[1]] = 0.5
    coordenada = f'({posicion_habitante2[0]},{posicion_habitante2[1]})'
    numero = terreno.diccionario_coordenadas[coordenada]
    #print(habitante1.numero, " choco con :", numero)
    habitante_objetivo = poblacion[numero]
    if habitante1.agresividad >0.8:#si la agresividad es mayor al 80% entonces intentara matar al otro habitante
        if habitante_objetivo.evasion >0.5:
            print("el habitante ", habitante1.numero, " intento asesinar al habitante ", habitante_objetivo.numero, " pero falló")
        else:
            #eliminar, se setea a 0 el valor que tiene en la matriz del terreno
            #se quita de la lista de poblacion y tambien se borra del diccionado de posicion
            terreno.matriz[posicion_habitante2[0]][posicion_habitante2[1]] = 0
            poblacion.pop(numero)
            del terreno.diccionario_coordenadas[coordenada]
            for i in range(len(poblacion)):
                poblacion[i].numero = i
                coord = f'({poblacion[i].coordenada_x},{poblacion[i].coordenada_y})'
                terreno.diccionario_coordenadas[coord] = i
            print("el habitante ", habitante1.numero, " asesinó al habitante ", habitante_objetivo.numero)

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
    indice_seleccionado = np.random.choice(indices_para_movimiento, size=1, replace=False, p=vector_normalizado)
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
                habitante = Habitante(i)
                habitante.cromosoma = sobrevivientes[0].cromosoma
                poblacion.append(habitante)
            else:
                habitante = Habitante(i)
                poblacion.append(habitante)
        return poblacion
   
    for i in range(len(sobrevivientes)):
        if (sobrevivientes[i].movimientos < fittest):
            fittest = sobrevivientes[i].movimientos
    nueva_poblacion = []

    for i in range(len(sobrevivientes)):
        if i<10:
            dos_sobrevivientes = seleccionar_habitantes(sobrevivientes)
            cruce_cromo = cruzar_cromosomas(dos_sobrevivientes)
            nueva_poblacion.append(cruce_cromo[0])
            nueva_poblacion.append(cruce_cromo[1])
    
    for i in range(len(nueva_poblacion)):
        habitante = Habitante(i)
        habitante.cromosoma = nueva_poblacion[i]
        poblacion.append(habitante)
    if len(nueva_poblacion)!=habitantes_primera_generacion:
        for i in range(habitantes_primera_generacion-len(nueva_poblacion)):
            habitante = Habitante(len(nueva_poblacion)+i)
            poblacion.append(habitante)
    return poblacion

#selecciona 2 sobrevivientes para cruzar sus cromosomas segun un index random, obteniendo de 2 padres, 2 hijos
def cruzar_cromosomas(dos_sobrevivientes):
    dna_index = np.random.randint(0, 9)
    cromosoma_hijo1 = []
    cromosoma_hijo2 = []

    #si dna_index es 0 o 9, los hijos seran igual a los padres, si no, se cortan los cromosomas de los padres en ese indice,
    #el hijo 1 será el cromosoma del padre 1 hasta el dna_index + el cromosoma del padre 2 desde el dna index hasta el final
    for i in range(dna_index):
        cromosoma_hijo1.append(dos_sobrevivientes[0].cromosoma[i])
        cromosoma_hijo2.append(dos_sobrevivientes[1].cromosoma[i])
    for i in range(dna_index, 9):
        cromosoma_hijo1.append(dos_sobrevivientes[0].cromosoma[i])
        cromosoma_hijo2.append(dos_sobrevivientes[1].cromosoma[i])
    return normalizar(mutacion(cromosoma_hijo1)), normalizar(mutacion(cromosoma_hijo2))

#un 5% de probabilidad de mutar cuando se gestan los 2 hijos en cruzar cromosomas
def mutacion(hijo):
    if np.random.randint(1, 20) == 20:
        index_modificado = np.random.randint(0, 8)          #cromosoma cualquiera del hijo
        valor_modificado = np.random.uniform(-1.0, 1.0)     #valor en que se añadirá a ese cromosoma
        if valor_modificado < 0 and valor_modificado * -1 >= hijo[index_modificado]: #si al sumar el valor ese cromosoma da menor a 0, que se quede en 0
            hijo[index_modificado] = 0
            return hijo
        hijo[index_modificado] += valor_modificado #se suma el valor al cromosoma index_modificado del hijo y se retorna
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

def seleccionar_habitantes(sobrevivientes): #selecciona 2 habitantes distintos con probabilidad p de ser escogidos para cruzarlos
    return np.random.choice(sobrevivientes, size=2, replace=False, p=probabilidad(sobrevivientes))

def graficar_supervivientes_por_generacion(x, y):
    plt.plot(x, y)
    plt.xlabel('N° Generacion')
    plt.ylabel('Cantidad de sobrevivientes')
    plt.show()

#variables utilizadas dentro del ciclo
generacion = 1
juego_activo = True
terreno = Terreno(largo, alto)
poblacion = []
poblacion_sobrevivientes = []

lista_x = []
lista_y = []

#ciclo del juego
while True:
    terreno.inicializarTerreno() #regeneramos el terreno
    if (len(poblacion_sobrevivientes) == 0): #si no hay supervivientes se crea una generacion por azar
        poblacion = crear_primera_poblacion()
        lista_y.append(len(poblacion_sobrevivientes))    
        lista_x.append(generacion)
        if (generacion != 1):
            print('no hubo supervivientes')
            
    else:
        print(f'sobrevivientes: {poblacion_sobrevivientes}')
        #poblacion_sobrevivientes son indices de los sobrevivientes, asi que se saca la verdadera población en enviar_pobla
        #para enviarla a la generación de la nueva población
        enviar_pobla = [poblacion[i] for i in poblacion_sobrevivientes] 
        poblacion = crear_siguiente_poblacion(enviar_pobla)
        lista_y.append(len(poblacion_sobrevivientes))    
        lista_x.append(generacion)

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
        graficar_supervivientes_por_generacion(lista_x, lista_y)
        break
    poblacion_sobrevivientes = sobrevivientes()
    generacion +=1
