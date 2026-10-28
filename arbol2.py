# ============================================================
# PROBLEMA DE BÚSQUEDA
# ============================================================

# Definición formal de un problema de búsqueda

# En Inteligencia Artificial, 
# un problema de búsqueda consiste en determinar 
# una secuencia de acciones que permita a un agente 
# pasar de un estado inicial a un estado objetivo, 
# utilizando las acciones disponibles y respetando las restricciones del problema.

# Formalmente, un problema de búsqueda puede representarse como una tupla de cinco elementos:

# P=(S,A,s0,G,C)

# donde:

# Elemento	Significado
# (S)	    Conjunto de todos los estados posibles
# (A)	    Conjunto de acciones que el agente puede realizar
# (s0)	    Estado inicial
# (G)	    Conjunto de estados objetivo
# (C)	    Costo asociado a las acciones o caminos

# 1. CONJUNTO DE ESTADOS (S)
# ------------------------------------------------------------
# Cada letra representa una posición posible del agente. Estados 
# Representan todas las situaciones en las que puede encontrarse el agente.
# Por ejemplo, para un robot que se mueve en un mapa:
# Cada letra representa una posición posible.

estados = {"A", "B", "C", "D", "E", "F" "G", "H", "I", "J"}


# 2. ACCIONES / CONEXIONES (A)
# ------------------------------------------------------------
# Diccionario que indica a qué estados puede desplazarse
# el agente desde cada estado izquierda o derecha

acciones = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["F", "G"],
    "D": ["A", "H"],
    "E": ["D"],
    "F": ["C", "I"],
    "G": ["C"],
    "J": ["I"],
}


# 3. ESTADO INICIAL (s0)
# ------------------------------------------------------------
# El agente comienza en A.

estado_inicial = "A"


# 4. ESTADO OBJETIVO (G)
# ------------------------------------------------------------
# El objetivo consiste en llegar a J.

estado_objetivo = "J"


# ============================================================
# ALGORITMO DE BÚSQUEDA EN ANCHURA (BFS)
# ============================================================

def busqueda_anchura(inicio, objetivo):
    """
    Busca un camino desde el estado inicial
    hasta el estado objetivo utilizando BFS.
    """

    # Cola de estados pendientes por explorar.
    cola = [[inicio]]

    # Estados que ya fueron visitados.
    visitados = set()

    # Mientras existan caminos pendientes...
    while cola:

        # Extraemos el primer camino de la cola.
        camino = cola.pop(0)

        # El último estado del camino es el estado actual.
        estado_actual = camino[-1]

        # Si ya visitamos este estado, lo ignoramos.
        if estado_actual in visitados:
            continue

        # Registramos el estado como visitado.
        visitados.add(estado_actual)

        # Mostramos el estado que estamos explorando.
        print("Explorando:", estado_actual)

        # Comprobamos si encontramos el objetivo.
        if estado_actual == objetivo:
            return camino

        # Obtenemos los estados vecinos.
        for vecino in acciones[estado_actual]:

            # Si todavía no hemos visitado el vecino...
            if vecino not in visitados:

                # Creamos un nuevo camino.
                nuevo_camino = camino + [vecino]

                # Lo agregamos a la cola.
                cola.append(nuevo_camino)

    # Si no existe una solución...
    return None


# ============================================================
# EJECUTAR LA BÚSQUEDA
# ============================================================

solucion = busqueda_anchura(
    estado_inicial,
    estado_objetivo
)


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

if solucion:

    print("\n¡Objetivo encontrado!")

    print("Ruta encontrada:")

    print(" -> ".join(solucion))

    print("\nNúmero de movimientos:", len(solucion) - 1)

else:

    print("\nNo se encontró una solución.")


# ---------------- Interfaz sencilla (Tkinter) ----------------
import io, threading, ollama, tkinter as tk
from tkinter import ttk
from contextlib import redirect_stdout

POS = {"A": (80, 60), "B": (210, 60), "C": (340, 60),
       "D": (80, 160), "E": (210, 160), "F": (340, 160), "G":(340,160)}

ultimo = {}   # guarda la última búsqueda para pasársela a la IA

def buscar(*_):
    salida = io.StringIO()
    with redirect_stdout(salida):
        ruta = busqueda_anchura(inicio.get(), objetivo.get()) or []
    orden = [l.split(": ")[1] for l in salida.getvalue().splitlines()
             if l.startswith("Explorando")]
    ultimo.update(orden=orden, ruta=ruta)
    pares = set(zip(ruta, ruta[1:])) | set(zip(ruta[1:], ruta))
    lienzo.delete("all")
    for a, vecinos in acciones.items():
        for b in vecinos:
            en_ruta = (a, b) in pares
            lienzo.create_line(*POS[a], *POS[b], width=6 if en_ruta else 3,
                               fill="#f97316" if en_ruta else "#cbd5e1")
    for n, (x, y) in POS.items():
        lienzo.create_oval(x-24, y-24, x+24, y+24, width=2, outline="#334155",
                           fill="#f97316" if n in ruta else "#e2e8f0")
        lienzo.create_text(x, y, text=n, font=("Segoe UI", 14, "bold"))
    resultado.config(text=" → ".join(ruta) + f"\n{len(ruta)-1} movimientos"
                     if ruta else "No se encontró una solución")
    dibujar_arbol(orden, ruta)

def dibujar_arbol(orden, ruta):
    # Árbol de búsqueda: cada estado cuelga del estado que lo descubrió
    padre, hijos = {}, {n: [] for n in estados}
    for n in orden:
        if n == objetivo.get():
            break
        for v in acciones[n]:
            if v != orden[0] and v not in padre:
                padre[v] = n
                hijos[n].append(v)
    pos, hojas = {}, [0]
    def colocar(n, nivel):
        if hijos[n]:
            xs = [colocar(h, nivel + 1) for h in hijos[n]]
            x = sum(xs) / len(xs)
        else:
            x = hojas[0]
            hojas[0] += 1
        pos[n] = (x, nivel)
        return x
    colocar(orden[0], 0)
    paso = 300 / max(1, hojas[0] - 1)
    xy = {n: (210 if hojas[0] == 1 else 60 + x * paso, 35 + nivel * 55)
          for n, (x, nivel) in pos.items()}
    pares = set(zip(ruta, ruta[1:]))
    arbol.delete("all")
    for h, p in padre.items():
        if p in xy and h in xy:
            en_ruta = (p, h) in pares
            arbol.create_line(*xy[p], *xy[h], width=6 if en_ruta else 3,
                              fill="#f97316" if en_ruta else "#cbd5e1")
    for n, (x, y) in xy.items():
        arbol.create_oval(x-20, y-20, x+20, y+20, width=2, outline="#334155",
                          fill="#f97316" if n in ruta else "#e2e8f0")
        arbol.create_text(x, y, text=n, font=("Segoe UI", 13, "bold"))

vista = {}   # ventana emergente donde se muestra la respuesta de la IA

def mostrar_ia(texto):
    if "win" not in vista or not vista["win"].winfo_exists():
        w = tk.Toplevel(ventana)
        w.title("Explicación de la IA")
        w.geometry("540x340")
        w.configure(bg="#f8fafc", padx=15, pady=15)
        tk.Label(w, text="Explicación de la IA", bg="#f8fafc", fg="#0f172a",
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 8))
        marco = tk.Frame(w, bg="#f8fafc")
        marco.pack(fill="both", expand=True)
        cuadro = tk.Text(marco, wrap="word", font=("Segoe UI", 12), bg="white",
                         fg="#334155", relief="flat", padx=12, pady=10,
                         highlightthickness=1, highlightbackground="#e2e8f0")
        barra_scroll = ttk.Scrollbar(marco, command=cuadro.yview)
        cuadro.config(yscrollcommand=barra_scroll.set)
        barra_scroll.pack(side="right", fill="y")
        cuadro.pack(side="left", fill="both", expand=True)
        vista.update(win=w, txt=cuadro)
    cuadro = vista["txt"]
    cuadro.config(state="normal")
    cuadro.delete("1.0", "end")
    cuadro.insert("end", texto)
    cuadro.config(state="disabled")
    vista["win"].lift()

def explicar():
    if not ultimo.get("ruta"):
        return
    pregunta = (f"Explica en español, de forma sencilla y en máximo 4 líneas, cómo la "
                f"búsqueda en anchura (BFS) llegó de {inicio.get()} a {objetivo.get()}. "
                f"Orden de exploración: {', '.join(ultimo['orden'])}. "
                f"Ruta final: {' -> '.join(ultimo['ruta'])}.")
    mostrar_ia("Pensando...")
    def tarea():   # se ejecuta en un hilo para que la ventana no se congele
        try:
            r = ollama.chat(model="llama3.2",
                            messages=[{"role": "user", "content": pregunta}])
            texto = r["message"]["content"]
        except Exception:
            texto = "No se pudo conectar con Ollama. Revisa que esté abierto."
        ventana.after(0, lambda: mostrar_ia(texto))
    threading.Thread(target=tarea, daemon=True).start()

ventana = tk.Tk()
ventana.title("Búsqueda en Anchura (BFS)")
ventana.configure(bg="#f8fafc", padx=20, pady=15)

tk.Label(ventana, text="Búsqueda en Anchura", bg="#f8fafc", fg="#0f172a",
         font=("Segoe UI", 18, "bold")).pack()

barra = tk.Frame(ventana, bg="#f8fafc")
barra.pack(pady=10)
inicio, objetivo = tk.StringVar(value=estado_inicial), tk.StringVar(value=estado_objetivo)
for texto, var in (("Inicio:", inicio), ("Objetivo:", objetivo)):
    tk.Label(barra, text=texto, bg="#f8fafc").pack(side="left", padx=(8, 2))
    caja = ttk.Combobox(barra, textvariable=var, values=sorted(estados), width=4, state="readonly")
    caja.pack(side="left")
    caja.bind("<<ComboboxSelected>>", buscar)
tk.Button(barra, text="Buscar", command=buscar, bg="#22c55e", fg="white",
          relief="flat", padx=14).pack(side="left", padx=12)
tk.Button(barra, text="Explicar con IA", command=explicar, bg="#6366f1", fg="white",
          relief="flat", padx=14).pack(side="left")

lienzo = tk.Canvas(ventana, width=420, height=220, bg="white", highlightthickness=1,
                   highlightbackground="#e2e8f0")
lienzo.pack()
resultado = tk.Label(ventana, bg="#f8fafc", fg="#c2410c", font=("Segoe UI", 14, "bold"))
resultado.pack(pady=10)

tk.Label(ventana, text="Árbol de búsqueda", bg="#f8fafc", fg="#0f172a",
         font=("Segoe UI", 14, "bold")).pack()
arbol = tk.Canvas(ventana, width=420, height=200, bg="white", highlightthickness=1,
                  highlightbackground="#e2e8f0")
arbol.pack(pady=(5, 0))

buscar()
ventana.mainloop()
