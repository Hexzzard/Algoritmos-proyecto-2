import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Definir los colores en formato RGBA
colors = [(255, 255, 255, 255),      # Blanco con transparencia completa
          (255, 0, 0, 128),          # Rojo con transparencia completa
          (255, 165, 0, 128),        # Naranja con transparencia completa
          (255, 255, 0, 128),        # Amarillo con transparencia media
          (46, 204, 113, 128),
          (0, 255, 0, 128),          #Verde
          (72, 201, 176, 128),
          (41, 128, 185, 128),            #Azul
          (142, 68, 173, 128),
          (127, 140, 141, 128)       #No moverse
          ]  

#Matplotlib trabaja con valores entre 0 y 1
colors = [(r/255, g/255, b/255, a/255) for r, g, b, a in colors]

# Crear el cmap personalizado
cmap = ListedColormap(colors)

# Ejemplo de uso del cmap
data =  np.zeros((20, 20))
j =0
for i in range (19):
    data[19,i] = j
    i +=1
    j+=1
    if j == 10:
        j=0

plt.imshow(data, cmap=cmap)
plt.colorbar()
plt.show()