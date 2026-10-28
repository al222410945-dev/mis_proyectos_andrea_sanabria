# ============================================================
# BÚSQUEDA DFS Y BFS APLICADA A SAFEGUARDIA
# ============================================================
#
# IDEA DEL PROYECTO
# SafeGuardIA guarda los incidentes que reportan los usuarios.
# Aquí usamos esa información para buscar RUTAS entre zonas:
#
#   - Cada zona (Casa, Parque, Mercado...) es un "estado".
#   - Cada calle que conecta dos zonas es una conexión.
#   - Cada zona tiene un número de incidentes reportados.
#
# Como las calles se pueden recorrer en los dos sentidos
# (de Casa a Parque y de Parque a Casa), el mapa tiene CICLOS.
# Por eso es importante evitar que el algoritmo se quede
# dando vueltas.
#
# Con DFS y BFS respondemos:
#   - ¿Qué rutas existen de Casa a la Escuela?
#   - ¿Cuál es la más corta?
#   - ¿Cuál es la MÁS SEGURA (menos incidentes)?
#   - ¿Qué pasa si limito cuántos pasos puede dar la ruta?
#
# NOTA: el mapa y los incidentes son SIMULADOS. En la app
# real los números saldrían de la colección "incidentes"
# en MongoDB.
#
# SALIDAS DEL PROGRAMA
#   - Texto en pantalla con todo lo que pide la práctica.
#   - Grafica_Mapa_Rutas.png         (mapa y ruta encontrada)
#   - Grafica_Limite_Profundidad.png (efecto del límite)
#   - Grafica_Riesgo_Rutas.png       (incidentes por ruta)
# ============================================================

import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Para que las flechas (→) se vean bien en la consola de Windows
sys.stdout.reconfigure(encoding="utf-8")


# ============================================================
# 1. EL MAPA (grafo con ciclos)
# ============================================================
# Cada zona indica a cuáles puede pasar.
# Las calles van en ambos sentidos, por eso cada conexión
# aparece dos veces (ida y vuelta) y eso forma ciclos, por ejemplo:
#   Casa → Parque → Avenida → Mercado → Casa
# "Callejón" es una zona sin salida (solo se puede regresar).

grafo = {
    "Casa":     ["Mercado", "Parque"],
    "Mercado":  ["Callejón", "Avenida", "Puente", "Casa"],
    "Parque":   ["Casa", "Avenida"],
    "Avenida":  ["Parque", "Escuela", "Plaza", "Mercado"],
    "Callejón": ["Mercado"],
    "Puente":   ["Mercado", "Plaza"],
    "Plaza":    ["Avenida", "Puente", "Escuela"],
    "Escuela":  ["Avenida", "Plaza"],
}

# Incidentes reportados en cada zona (simulados)
incidentes = {
    "Casa": 1, "Mercado": 14, "Parque": 9, "Avenida": 6,
    "Callejón": 17, "Puente": 11, "Plaza": 5, "Escuela": 2,
}

estado_inicial = "Casa"
estado_objetivo = "Escuela"


def flecha(lista):
    """Convierte una lista en texto: A → B → C"""
    return " → ".join(lista)


def linea(titulo):
    print("\n" + "=" * 62)
    print(titulo)
    print("=" * 62)


def riesgo(ruta):
    """Suma los incidentes de las zonas por las que pasa la ruta
    (sin contar la zona de salida)."""
    return sum(incidentes[zona] for zona in ruta[1:])


# ============================================================
# 2. DFS: ORDEN DE EXPLORACIÓN + CONTROL DE CICLOS
# ============================================================
# Esta versión se detiene en la PRIMERA ruta que encuentra.
#
# Usa dos estructuras:
#   visitados -> todas las zonas que ya se revisaron
#   camino    -> la ruta que se está siguiendo en este momento
#
# Antes de entrar a una zona se pregunta:
#   ¿ya la visité?  -> si sí, NO entro (así no hay ciclo infinito)

def dfs_primera_ruta(actual, objetivo, visitados, camino, orden, avisos):

    visitados.add(actual)       # la marco como visitada
    camino.append(actual)       # la agrego a la ruta actual
    orden.append(actual)        # la anoto en el orden de exploración

    if actual == objetivo:      # ¿llegué?
        return camino.copy()

    for vecino in grafo[actual]:

        if vecino in visitados:
            # Aquí se evita el ciclo
            if vecino in camino:
                avisos.append(f"CICLO detectado: {actual} → {vecino} "
                              f"({vecino} ya está en la ruta actual)")
            else:
                avisos.append(f"Omitido: {actual} → {vecino} "
                              f"({vecino} ya fue explorado antes)")
            continue

        resultado = dfs_primera_ruta(vecino, objetivo, visitados,
                                     camino, orden, avisos)
        if resultado:
            return resultado

    # BACKTRACKING: desde aquí no se llegó al objetivo,
    # así que regreso un paso.
    camino.pop()
    return None


# ============================================================
# 3. DFS: TODAS LAS RUTAS + LÍMITE DE PROFUNDIDAD
# ============================================================
# Ahora NO nos detenemos en la primera ruta.
#
# Para encontrar todas las rutas, una zona puede aparecer en
# varias rutas distintas. Por eso aquí solo evitamos repetir
# zonas DENTRO de la misma ruta (conjunto "en_esta_ruta").
# Al hacer backtracking, la zona sale de ese conjunto.
#
# LÍMITE DE PROFUNDIDAD:
# profundidad = cuántos pasos llevo desde el inicio.
# Si llego al límite y aún no estoy en el objetivo,
# corto esa rama y regreso.

def dfs_todas_las_rutas(actual, objetivo, limite, camino, en_esta_ruta,
                        rutas, orden, avisos, cortes):

    camino.append(actual)
    en_esta_ruta.add(actual)
    orden.append(actual)

    profundidad = len(camino) - 1

    if actual == objetivo:
        # Encontré una ruta: la guardo y sigo buscando otras
        rutas.append(camino.copy())

    elif profundidad >= limite:
        # Llegué al límite: no sigo por esta rama
        cortes.append(f"{actual} (profundidad {profundidad})")

    else:
        for vecino in grafo[actual]:
            if vecino in en_esta_ruta:
                avisos.append(f"CICLO evitado: {actual} → {vecino}")
            else:
                dfs_todas_las_rutas(vecino, objetivo, limite, camino,
                                    en_esta_ruta, rutas, orden,
                                    avisos, cortes)

    # BACKTRACKING: quito la zona para probar otro camino
    camino.pop()
    en_esta_ruta.remove(actual)


def buscar_todas(limite):
    """Ejecuta la búsqueda de todas las rutas y regresa los resultados."""
    rutas, orden, avisos, cortes = [], [], [], []
    dfs_todas_las_rutas(estado_inicial, estado_objetivo, limite,
                        [], set(), rutas, orden, avisos, cortes)
    return {"rutas": rutas, "orden": orden,
            "avisos": avisos, "cortes": cortes}


# ============================================================
# 4. BFS (BÚSQUEDA EN ANCHURA)
# ============================================================
# BFS revisa primero todas las zonas cercanas y luego las
# más lejanas, por eso siempre encuentra la ruta con MENOS PASOS.

def bfs(inicio, objetivo, limite):

    cola = [[inicio]]
    visitados = {inicio}
    orden, avisos, cortes = [], [], []

    while cola:
        camino = cola.pop(0)
        actual = camino[-1]
        orden.append(actual)

        if actual == objetivo:
            return camino, orden, avisos, cortes

        if len(camino) - 1 >= limite:
            cortes.append(f"{actual} (profundidad {len(camino) - 1})")
            continue

        for vecino in grafo[actual]:
            if vecino in visitados:
                avisos.append(f"Omitido: {actual} → {vecino} (ya visitado)")
            else:
                visitados.add(vecino)
                cola.append(camino + [vecino])

    return None, orden, avisos, cortes


# ============================================================
# 5. GRÁFICAS
# ============================================================

# Paleta coherente (misma en todas las gráficas)
COLOR_INICIO = "#2A9D8F"     # verde azulado
COLOR_OBJETIVO = "#E9C46A"   # amarillo
COLOR_RECHAZO = "#E76F51"    # rojo anaranjado
COLOR_NORMAL = "#DCE3EA"     # gris claro
COLOR_RUTA = "#264653"       # azul oscuro
COLOR_LINEA = "#B0B8C1"      # gris
COLOR_GRIS = "#6C757D"

# Posición de cada zona en el dibujo
posiciones = {
    "Casa":     (0, 0),
    "Mercado":  (3.2, -2),
    "Parque":   (3.2, 2),
    "Avenida":  (6.8, 0),
    "Callejón": (0, -3.6),
    "Puente":   (6.8, -3.4),
    "Plaza":    (10.2, -1.8),
    "Escuela":  (13.2, 0),
}


def dibujar_mapa(ruta, orden, archivo, subtitulo):
    """Dibuja el mapa, resalta la ruta y numera el orden de exploración."""

    fig, ax = plt.subplots(figsize=(14, 7.5))

    # --- Calles (una línea por conexión) ---
    dibujadas = set()
    for origen, destinos in grafo.items():
        for destino in destinos:
            par = frozenset((origen, destino))
            if par in dibujadas:
                continue
            dibujadas.add(par)

            es_ruta = (origen in ruta and destino in ruta and
                       abs(ruta.index(origen) - ruta.index(destino)) == 1)
            (x1, y1), (x2, y2) = posiciones[origen], posiciones[destino]
            ax.plot([x1, x2], [y1, y2],
                    color=COLOR_RUTA if es_ruta else COLOR_LINEA,
                    linewidth=5 if es_ruta else 1.8, zorder=1,
                    solid_capstyle="round")

    # --- Zonas (cajas) ---
    for nombre, (x, y) in posiciones.items():
        if nombre == estado_inicial:
            color = COLOR_INICIO
        elif nombre == estado_objetivo:
            color = COLOR_OBJETIVO
        elif nombre == "Callejón":
            color = COLOR_RECHAZO
        else:
            color = COLOR_NORMAL

        ax.text(x, y, nombre, ha="center", va="center", fontsize=12,
                fontweight="bold", zorder=3,
                color="white" if nombre in (estado_inicial, "Callejón")
                else "black",
                bbox=dict(boxstyle="round,pad=0.55", fc=color,
                          ec=COLOR_RUTA, lw=1.5))

        # Incidentes reportados en la zona
        ax.text(x, y - 0.75, f"Incidentes: {incidentes[nombre]}",
                ha="center", va="center", fontsize=9, color=COLOR_GRIS,
                zorder=3)

        # Número del orden en que DFS exploró la zona
        if nombre in orden:
            mitad = len(nombre) * 0.085 + 0.25   # mitad del ancho de la caja
            ax.text(x - mitad, y + 0.35, str(orden.index(nombre) + 1),
                    ha="center", va="center", fontsize=10,
                    fontweight="bold", color="white", zorder=4,
                    bbox=dict(boxstyle="circle,pad=0.3", fc=COLOR_GRIS,
                              ec="none"))

    # --- Leyenda ---
    elementos = [
        Patch(fc=COLOR_INICIO, ec=COLOR_RUTA, label="Zona de salida"),
        Patch(fc=COLOR_OBJETIVO, ec=COLOR_RUTA, label="Destino"),
        Patch(fc=COLOR_RECHAZO, ec=COLOR_RUTA, label="Zona sin salida"),
        Patch(fc=COLOR_NORMAL, ec=COLOR_RUTA, label="Otras zonas"),
        Line2D([0], [0], color=COLOR_RUTA, lw=5, label="Ruta encontrada"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_GRIS,
               markersize=11, label="Orden de exploración"),
    ]
    ax.legend(handles=elementos, loc="lower center", ncol=6, fontsize=10,
              frameon=False, bbox_to_anchor=(0.5, -0.02))

    ax.set_xlim(-1.5, 14.7)
    ax.set_ylim(-4.8, 3.4)
    ax.axis("off")

    fig.suptitle("Mapa de zonas y rutas de SafeGuardIA",
                 fontsize=20, fontweight="bold", y=0.98,
                 color=COLOR_RUTA)
    ax.set_title(subtitulo, fontsize=12, color=COLOR_GRIS, pad=4)
    fig.text(0.01, 0.01,
             "SafeGuardIA | Mapa e incidentes simulados | UTVT",
             fontsize=9, color=COLOR_GRIS)

    plt.tight_layout()
    plt.savefig(archivo, dpi=200, bbox_inches="tight")
    plt.close()


def grafica_limites(resultados, archivo):
    """Muestra cómo cambia la búsqueda según el límite de profundidad."""

    limites = [r[0] for r in resultados]
    n_rutas = [r[1] for r in resultados]
    n_nodos = [r[2] for r in resultados]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # --- Izquierda: rutas encontradas ---
    barras = ax1.bar(limites, n_rutas, color=COLOR_INICIO,
                     edgecolor=COLOR_RUTA, width=0.6)
    ax1.bar_label(barras, fontsize=12, fontweight="bold", padding=3)
    ax1.set_title("Rutas encontradas", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Número de rutas", fontsize=12)
    ax1.set_ylim(0, max(n_rutas) + 1)
    ax1.set_yticks(range(0, max(n_rutas) + 2))   # solo números enteros

    # --- Derecha: zonas exploradas ---
    barras = ax2.bar(limites, n_nodos, color=COLOR_RECHAZO,
                     edgecolor=COLOR_RUTA, width=0.6)
    ax2.bar_label(barras, fontsize=12, fontweight="bold", padding=3)
    ax2.set_title("Trabajo del algoritmo (zonas exploradas)",
                  fontsize=14, fontweight="bold")
    ax2.set_ylabel("Zonas revisadas", fontsize=12)
    ax2.set_ylim(0, max(n_nodos) * 1.15)

    for ax in (ax1, ax2):
        ax.set_xlabel("Límite de profundidad (máximo de pasos)", fontsize=12)
        ax.set_xticks(limites)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("Efecto del límite de profundidad en la búsqueda DFS",
                 fontsize=20, fontweight="bold", color=COLOR_RUTA)
    fig.text(0.5, 0.90,
             "Con un límite pequeño no se llega a la Escuela; "
             "al aumentarlo aparecen más rutas",
             ha="center", fontsize=12, color=COLOR_GRIS)
    fig.text(0.01, 0.01,
             "SafeGuardIA | Mapa e incidentes simulados | UTVT",
             fontsize=9, color=COLOR_GRIS)

    plt.tight_layout(rect=(0, 0.03, 1, 0.9))
    plt.savefig(archivo, dpi=200, bbox_inches="tight")
    plt.close()


def grafica_riesgo(rutas, archivo):
    """Compara las rutas encontradas según sus incidentes acumulados."""

    # Ordenadas de la más segura a la menos segura
    ordenadas = sorted(rutas, key=riesgo)
    etiquetas = [f"{flecha(r)}  ({len(r) - 1} pasos)" for r in ordenadas]
    valores = [riesgo(r) for r in ordenadas]
    colores = [COLOR_INICIO if i == 0 else "#B8C4CE"
               for i in range(len(ordenadas))]

    fig, ax = plt.subplots(figsize=(14, 6.5))

    barras = ax.barh(etiquetas, valores, color=colores,
                     edgecolor=COLOR_RUTA)
    ax.bar_label(barras, fontsize=12, fontweight="bold", padding=4)
    ax.invert_yaxis()    # la más segura queda arriba

    ax.set_xlabel("Incidentes acumulados en la ruta", fontsize=13)
    ax.set_xlim(0, max(valores) * 1.12)
    ax.tick_params(axis="y", labelsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(handles=[
        Patch(fc=COLOR_INICIO, ec=COLOR_RUTA, label="Ruta más segura"),
        Patch(fc="#B8C4CE", ec=COLOR_RUTA, label="Otras rutas"),
    ], loc="upper right", frameon=False, fontsize=11)

    fig.suptitle("Comparación de rutas de Casa a Escuela",
                 fontsize=20, fontweight="bold", color=COLOR_RUTA)
    ax.set_title("Menos incidentes acumulados = ruta más segura",
                 fontsize=12, color=COLOR_GRIS, pad=8)
    fig.text(0.01, 0.01,
             "SafeGuardIA | Mapa e incidentes simulados | UTVT",
             fontsize=9, color=COLOR_GRIS)

    plt.tight_layout(rect=(0, 0.03, 1, 1))
    plt.savefig(archivo, dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# 6. EJECUCIÓN Y RESULTADOS
# ============================================================

# ---------- PARTE A: DFS (primera ruta, orden y ciclos) ----------

linea("PARTE A. DFS: ORDEN DE EXPLORACIÓN Y CONTROL DE CICLOS")

visitados_a, camino_a, orden_a, avisos_a = set(), [], [], []
ruta_a = dfs_primera_ruta(estado_inicial, estado_objetivo,
                          visitados_a, camino_a, orden_a, avisos_a)

print("Orden de exploración (zonas exploradas):")
print(flecha(orden_a))

print("\nRuta encontrada:")
print(flecha(ruta_a) if ruta_a else "No se encontró una ruta.")

print(f"\nZonas visitadas: {len(visitados_a)} de {len(grafo)}")
print(", ".join(sorted(visitados_a)))

print("\nMecanismo contra ciclos infinitos: el conjunto 'visitados'.")
print("Antes de entrar a una zona se revisa si ya está ahí.")
print("Avisos generados durante la búsqueda:")
for aviso in avisos_a:
    print("  -", aviso)

print("\nOjo: la ruta encontrada NO es igual a las zonas exploradas.")
extra = [n for n in orden_a if n not in ruta_a]
print("Se exploraron, pero no forman parte de la ruta:",
      ", ".join(extra) if extra else "ninguna")


# ---------- PARTE B: BFS ----------

linea("PARTE B. BFS: RUTA CON MENOS PASOS")

ruta_b, orden_b, avisos_b, cortes_b = bfs(estado_inicial,
                                          estado_objetivo, limite=10)
print("Orden de exploración:")
print(flecha(orden_b))
print("\nRuta encontrada:")
print(flecha(ruta_b))
print(f"\nPasos DFS: {len(ruta_a) - 1}  |  Pasos BFS: {len(ruta_b) - 1}")
if len(ruta_a) > len(ruta_b):
    print("DFS encontró una ruta más larga: se queda con la primera")
    print("que prueba. BFS siempre encuentra la de menos pasos.")
else:
    print("Aquí coinciden, pero solo BFS garantiza la ruta con menos")
    print("pasos; DFS se queda con la primera que prueba.")


# ---------- PARTE C: DFS todas las rutas + límite ----------

linea("PARTE C. DFS: TODAS LAS RUTAS CON LÍMITE DE PROFUNDIDAD")

LIMITE = 6
res = buscar_todas(LIMITE)

print(f"Límite de profundidad: {LIMITE}\n")
for numero, ruta in enumerate(res["rutas"], start=1):
    print(f"Ruta {numero} ({len(ruta) - 1} pasos, "
          f"{riesgo(ruta)} incidentes):")
    print(flecha(ruta), "\n")

print(f"Total de rutas encontradas: {len(res['rutas'])}")
print("\nOrden de exploración (puede repetir zonas porque se")
print("prueban rutas distintas):")
print(flecha(res["orden"]))
print(f"\nCiclos evitados: {len(res['avisos'])}")
print(f"Ramas cortadas por el límite: {len(res['cortes'])}")


# ---------- PARTE D: probar varios límites ----------

linea("PARTE D. PRUEBA CON DIFERENTES LÍMITES DE PROFUNDIDAD")

resultados = []
for lim in [2, 3, 4, 5, 6, 7]:
    r = buscar_todas(lim)
    resultados.append((lim, len(r["rutas"]), len(r["orden"])))
    print(f"\nLímite {lim}: {len(r['rutas'])} ruta(s), "
          f"{len(r['cortes'])} rama(s) cortada(s)")
    for ruta in r["rutas"]:
        print("   ", flecha(ruta))

print("\nConclusión: con límite 2 no se llega a la Escuela; al subir")
print("el límite aparecen más rutas hasta que ya están todas.")


# ---------- PARTE E: ¿la más corta es la más segura? ----------

linea("PARTE E. RUTA MÁS CORTA VS. RUTA MÁS SEGURA")

todas = res["rutas"]
mas_segura = min(todas, key=riesgo)

print(f"Ruta más corta (BFS):  {flecha(ruta_b)}")
print(f"   {len(ruta_b) - 1} pasos, {riesgo(ruta_b)} incidentes\n")
print(f"Ruta más segura:       {flecha(mas_segura)}")
print(f"   {len(mas_segura) - 1} pasos, {riesgo(mas_segura)} incidentes\n")

if riesgo(mas_segura) < riesgo(ruta_b):
    print("La ruta más corta NO es la más segura. Por eso conviene")
    print("buscar TODAS las rutas y no quedarse con la primera.")
else:
    print("En este caso la ruta más corta también es la más segura.")


# ---------- GRÁFICAS ----------

dibujar_mapa(ruta_a, orden_a, "Grafica_Mapa_Rutas.png",
             "Ruta encontrada por DFS (azul oscuro) y orden en que "
             "se exploraron las zonas (números)")
grafica_limites(resultados, "Grafica_Limite_Profundidad.png")
grafica_riesgo(todas, "Grafica_Riesgo_Rutas.png")


# ============================================================
# 7. RESUMEN PARA LA ENTREGA
# ============================================================

linea("RESUMEN")
print("Orden de exploración ......... Partes A, B y C")
print("Zonas visitadas .............. Parte A (conjunto 'visitados')")
print("Ruta o rutas encontradas ..... Partes A, B, C y E")
print("Control de ciclos ............ 'visitados' y 'en_esta_ruta'")
print(f"Límite de profundidad ........ {LIMITE} (probado de 2 a 7)")
print("Integración en el proyecto ... Rutas entre zonas con incidentes")
print("\nImágenes generadas:")
print("  - Grafica_Mapa_Rutas.png")
print("  - Grafica_Limite_Profundidad.png")
print("  - Grafica_Riesgo_Rutas.png")
