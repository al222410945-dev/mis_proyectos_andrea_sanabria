# SafeGuardIA: recorrido del proceso de análisis usando DFS y BFS
# El grafo representa pasos posibles del sistema, no una detección real.
# DFS explora una rama antes de regresar; BFS busca primero el camino con menos pasos.

from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

flujo = {
    "Inicio": ["Revisar texto", "Revisar imagen"],
    "Revisar texto": ["Analizar mensaje (NLP)"],
    "Analizar mensaje (NLP)": ["Revisar enlace", "Mostrar mensaje"],
    "Revisar enlace": ["Advertir posible phishing", "Mostrar mensaje"],
    "Advertir posible phishing": ["Mostrar advertencia"],
    "Mostrar mensaje": ["Fin"],
    "Revisar imagen": ["Analizar imagen (visión artificial)"],
    "Analizar imagen (visión artificial)": [
        "Difuminar contenido", "Mostrar imagen"
    ],
    "Difuminar contenido": ["Mostrar advertencia"],
    "Mostrar imagen": ["Fin"],
    "Mostrar advertencia": ["Fin"],
    "Fin": []
}

inicio = "Inicio"
objetivo = "Fin"


def dfs_primera_ruta(grafo, inicio, objetivo):
    visitados = set()
    orden = []

    def explorar(nodo):
        visitados.add(nodo)
        orden.append(nodo)
        if nodo == objetivo:
            return [nodo]
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                resultado = explorar(vecino)
                if resultado:
                    return [nodo] + resultado
        return None

    ruta = explorar(inicio)
    return ruta, orden


def bfs_ruta_corta(grafo, inicio, objetivo):
    cola = deque([[inicio]])
    visitados = {inicio}
    orden = []

    while cola:
        ruta = cola.popleft()
        actual = ruta[-1]
        orden.append(actual)
        if actual == objetivo:
            return ruta, orden
        for vecino in grafo[actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(ruta + [vecino])
    return None, orden


def mostrar_ruta(ruta):
    return " -> ".join(ruta) if ruta else "No se encontró una ruta."


ruta_dfs, orden_dfs = dfs_primera_ruta(flujo, inicio, objetivo)
ruta_bfs, orden_bfs = bfs_ruta_corta(flujo, inicio, objetivo)

print("=" * 58)
print("SAFEGUARDIA: RECORRIDO DEL PROCESO DE ANÁLISIS")
print("=" * 58)
print("\nDFS, primera ruta encontrada:")
print(mostrar_ruta(ruta_dfs))
print("Pasos:", len(ruta_dfs) - 1 if ruta_dfs else 0)
print("\nBFS, ruta con menos pasos:")
print(mostrar_ruta(ruta_bfs))
print("Pasos:", len(ruta_bfs) - 1 if ruta_bfs else 0)
print("\nDFS revisó:", " -> ".join(orden_dfs))
print("BFS revisó:", " -> ".join(orden_bfs))
print("\nNota: este ejemplo recorre el flujo lógico de la aplicación.")
print("No intercepta notificaciones ni analiza imágenes por sí mismo.")

# Dibujo sencillo del flujo y resaltado de la ruta BFS.
grafo_nx = nx.DiGraph()
for origen, destinos in flujo.items():
    for destino in destinos:
        grafo_nx.add_edge(origen, destino)

posiciones = {
    "Inicio": (0, 2),
    "Revisar texto": (2, 3),
    "Revisar imagen": (2, 1),
    "Analizar mensaje (NLP)": (4, 3),
    "Analizar imagen (visión artificial)": (4, 1),
    "Revisar enlace": (6, 3.7),
    "Mostrar mensaje": (6, 2.5),
    "Difuminar contenido": (6, 1.4),
    "Mostrar imagen": (6, 0.5),
    "Advertir posible phishing": (8, 3.7),
    "Mostrar advertencia": (8, 1.8),
    "Fin": (10, 2)
}

plt.figure(figsize=(16, 8))
nx.draw_networkx_nodes(grafo_nx, posiciones, node_size=2500,
                       node_color="#DCE3EA", edgecolors="#264653")
nx.draw_networkx_labels(grafo_nx, posiciones, font_size=8)
nx.draw_networkx_edges(grafo_nx, posiciones, arrows=True,
                       arrowsize=18, edge_color="#AAB4BE", width=1.5)

aristas_ruta = list(zip(ruta_bfs, ruta_bfs[1:])) if ruta_bfs else []
nx.draw_networkx_edges(grafo_nx, posiciones, edgelist=aristas_ruta,
                       arrows=True, arrowsize=20, edge_color="#E76F51", width=3)

plt.title("Flujo de análisis preventivo de SafeGuardIA", fontsize=16,
          fontweight="bold", color="#264653")
plt.axis("off")
plt.tight_layout()
plt.savefig("Flujo_Analisis_SafeGuardIA.png", dpi=250, bbox_inches="tight")
plt.show()
print("\nGráfica creada: Flujo_Analisis_SafeGuardIA.png")
