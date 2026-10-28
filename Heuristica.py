
# Costos de cada nodo
costos = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 7,
    'E': 5,
    'F': 3,
    'G': 6,
    'H': 8,
    'I': 1,
    'J': 0
}

# Conexiones del árbol
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': ['J'],
    'J': []
}

def buscar_ruta(inicio, objetivo):
    pendientes = [(inicio, [inicio])]

    while pendientes:
        nodo, ruta = pendientes.pop()

        if nodo == objetivo:
            return ruta

        for vecino in reversed(grafo[nodo]):
            if vecino not in ruta:
                pendientes.append((vecino, ruta + [vecino]))

    return None


# Buscar la ruta de A hasta J
ruta = buscar_ruta('A', 'J')

if ruta:
    costo_total = sum(costos[nodo] for nodo in ruta)

    print("RUTA DE A HASTA J")
    print("--------------------")
    print("Ruta:", " -> ".join(ruta))
    print("Costos:", " + ".join(str(costos[n]) for n in ruta))
    print("Costo total:", costo_total)
else:
    print("No se encontró una ruta.")
