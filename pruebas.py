diccionario = {
    1: "valor1",
    3: "valor3",
    5: "valor5",
    7: "valor7",
    9: "valor9"
}

for i in range(1, 11):
    try:
        valor = diccionario[i]
        print(valor)
    except KeyError:
        continue