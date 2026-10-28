
import heapq

# Grafo con costos de las conexiones
grafo = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2), ('G', 3)],
    'D': [('H', 1)],
    'E': [('I', 1)],
    'F': [('J', 3)],
    'G': [],
    'H': [],
    'I': [],
    'J': []
}

def buscar_ruta(inicio, objetivo):
    pendientes = [(0, inicio, [inicio])]
    visitados = set()

    while pendientes:
        costo, nodo, ruta = heapq.heappop(pendientes)

        if nodo == objetivo:
            return ruta, costo

        if nodo in visitados:
            continue

        visitados.add(nodo)

        for vecino, valor in grafo[nodo]:
            if vecino not in visitados:
                heapq.heappush(
                    pendientes,
                    (costo + valor, vecino, ruta + [vecino])
                )

    return None, None


ruta, costo = buscar_ruta('A', 'J')

if ruta:
    print("Ruta encontrada:", " -> ".join(ruta))
    print("Costo total:", costo)
else:
    print("No se encontró una ruta.")
