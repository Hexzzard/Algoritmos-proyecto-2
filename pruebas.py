import numpy as np
import matplotlib.pyplot as plt

# Matriz de ejemplo
matriz = np.array([[0, 0], [3, 4]])
print(matriz)
# Crear figura y ejes
fig, ax = plt.subplots()

# Mostrar la matriz en el primer cuadrante
ax.imshow(matriz, cmap='Blues', interpolation='nearest', extent=[0, matriz.shape[1], 0, matriz.shape[0]])

# Ajustar límites de los ejes
ax.set_xlim(0, matriz.shape[1])
ax.set_ylim(0, matriz.shape[0])

# Añadir etiquetas a los ejes
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')

# Mostrar la gráfica
plt.show()
