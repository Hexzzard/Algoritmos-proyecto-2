import matplotlib.pyplot as plt
import numpy as np

# Ejemplo de 10 arreglos de datos
datos = []
for i in range(10):
    datos.append(np.random.rand(100))  # Generar datos aleatorios

# Crear el gráfico compuesto por 10 líneas
for i in range(10):
    plt.plot(datos[i])

# Mostrar el gráfico
plt.show()