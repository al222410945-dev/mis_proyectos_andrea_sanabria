from itertools import permutations
from math import factorial, hypot
import tkinter as tk
from tkinter import ttk

# ---------------- CONFIGURACIÓN (edita aquí) ----------------
NOMBRE, INICIO = "Almacén", (0, 0)
CLIENTES = {"A": (2, 1), "B": (4, 4), "C": (5, 2), "D": (6, 6), "E": (8, 1)}
FONDO, AZUL, VERDE, ROJO, TENUE, NARANJA = "#f3f8fb", "#1677a8", "#159477", "#d1495b", "#b7ddd5", "#f4a261"
VELOCIDAD_MS = 700          # tiempo entre tramos en la animación
# ------------------------------------------------------------

PUNTOS = {NOMBRE: INICIO, **CLIENTES}
LIM = max(max(p) for p in PUNTOS.values()) + 1


def tramos(orden):
    """(desde, hasta, distancia euclidiana) de cada tramo, ida y regreso."""
    n = [NOMBRE, *orden, NOMBRE]
    return [(a, b, hypot(PUNTOS[b][0] - PUNTOS[a][0], PUNTOS[b][1] - PUNTOS[a][1]))
            for a, b in zip(n, n[1:])]


def generar_rutas():
    rutas = [(o, sum(t[2] for t in tramos(o))) for o in permutations(CLIENTES)]
    return sorted(rutas, key=lambda r: r[1])


class App(tk.Tk):
    TAM = 560                      # tamaño del mapa
    GW, GH, ML, MR, MT, MB = 480, 380, 50, 15, 20, 35   # gráfica de línea

    def __init__(self):
        super().__init__()
        self.title("Robot repartidor | Ruta óptima")
        self.configure(bg=FONDO)
        self.rutas, self.i = generar_rutas(), 0
        self.paso, self.anim = 0, None          # tramos mostrados / id de animación
        self.todas = tk.BooleanVar(value=True)
        d, n = [r[1] for r in self.rutas], len(CLIENTES)

        tk.Label(self, bg=FONDO, font=("Segoe UI", 12, "bold"),
                 text=f"Rutas posibles: {n}! = {factorial(n)}   |   Mínima: {min(d):.2f}   |   "
                      f"Máxima: {max(d):.2f}   |   Promedio: {sum(d) / len(d):.2f}").pack(pady=8)
        cuerpo = tk.Frame(self, bg=FONDO)
        cuerpo.pack(padx=10, pady=(0, 10))
        izq = tk.Frame(cuerpo, bg=FONDO)
        izq.pack(side="left")
        self.info = tk.Label(izq, bg=FONDO, font=("Segoe UI", 11, "bold"))
        self.info.pack(anchor="w")
        self.mapa = tk.Canvas(izq, width=self.TAM, height=self.TAM, bg="white")
        self.mapa.pack()
        barra = tk.Frame(izq, bg=FONDO)
        barra.pack(fill="x", pady=6)
        for txt, f in [("Ruta óptima", lambda: self.ir(0)),
                       ("Ruta más larga", lambda: self.ir(len(self.rutas) - 1)),
                       ("◀", lambda: self.ir(self.i - 1)), ("▶", lambda: self.ir(self.i + 1))]:
            tk.Button(barra, text=txt, command=f).pack(side="left", padx=2)
        barra2 = tk.Frame(izq, bg=FONDO)
        barra2.pack(fill="x")
        for txt, f in [("◀ Tramo", lambda: self.mover(-1)),
                       ("Tramo ▶", lambda: self.mover(1)),
                       ("↻ Animar", lambda: self.ir(self.i)),
                       ("Ver completa", lambda: self.mover(99))]:
            tk.Button(barra2, text=txt, command=f).pack(side="left", padx=2)
        tk.Checkbutton(barra2, text="Mostrar todas las rutas", bg=FONDO, variable=self.todas,
                       command=self.dibujar_mapa).pack(side="left", padx=8)

        tabs = ttk.Notebook(cuerpo)
        tabs.pack(side="left", padx=(10, 0), anchor="n")
        self.tabla = ttk.Treeview(tabs, columns=("n", "ruta", "dist"), show="headings", height=24)
        for c, t, w in [("n", "#", 40), ("ruta", "Recorrido", 270), ("dist", "Distancia", 80)]:
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=w)
        for k, (o, dist) in enumerate(self.rutas):
            self.tabla.insert("", "end", iid=str(k),
                              values=(k + 1, " → ".join(("Alm", *o, "Alm")), f"{dist:.2f}"))
        self.tabla.bind("<<TreeviewSelect>>", self.al_elegir)
        self.detalle = tk.Text(tabs, width=52, height=26, font=("Consolas", 10))
        self.grafica = tk.Canvas(tabs, width=self.GW, height=self.GH, bg="white")
        self.grafica.bind("<Button-1>", self.clic_grafica)
        tabs.add(self.tabla, text="Rutas (120)")
        tabs.add(self.detalle, text="Cálculo")
        tabs.add(self.grafica, text="Gráfica de línea")
        self.ir(0)

    # ---------- control de la animación tramo por tramo ----------
    def pausar(self):
        if self.anim:
            self.after_cancel(self.anim)
            self.anim = None

    def mover(self, delta):
        """Avanza/retrocede tramos manualmente (pausa la animación)."""
        self.pausar()
        total = len(tramos(self.rutas[self.i][0]))
        self.paso = max(0, min(total, self.paso + delta))
        self.refrescar()

    def avanzar(self):
        self.anim = None
        total = len(tramos(self.rutas[self.i][0]))
        if self.paso < total:
            self.paso += 1
            self.refrescar()
            if self.paso < total:
                self.anim = self.after(VELOCIDAD_MS, self.avanzar)

    def refrescar(self):
        self.dibujar_mapa()
        self.dibujar_detalle()

    # ---------- selección de ruta ----------
    def ir(self, i):
        self.pausar()
        self.i = max(0, min(len(self.rutas) - 1, i))
        self.paso = 0
        orden, dist = self.rutas[self.i]
        self.info.config(text=f"{'★ Óptima' if self.i == 0 else f'Ruta #{self.i + 1}'}: "
                              f"{' → '.join([NOMBRE, *orden, NOMBRE])}  =  {dist:.2f}")
        self.tabla.selection_set(str(self.i))
        self.tabla.see(str(self.i))
        self.refrescar()
        self.dibujar_grafica()
        self.anim = self.after(VELOCIDAD_MS, self.avanzar)   # inicia el recorrido

    def dibujar_detalle(self):
        orden, dist = self.rutas[self.i]
        self.detalle.delete("1.0", "end")
        self.detalle.insert("end", "d = raíz((x2-x1)² + (y2-y1)²)\n\n")
        acum = 0
        for k, (a, b, d) in enumerate(tramos(orden)[:self.paso], 1):
            acum += d
            self.detalle.insert("end", f"Tramo {k}: {a} {PUNTOS[a]} → {b} {PUNTOS[b]}\n"
                                       f"   d = {d:.2f}   (acumulado = {acum:.2f})\n")
        if self.paso == len(tramos(orden)):
            self.detalle.insert("end", f"\nDISTANCIA TOTAL = {dist:.2f}")

    def al_elegir(self, _e):
        sel = self.tabla.selection()
        if sel and int(sel[0]) != self.i:
            self.ir(int(sel[0]))

    def dibujar_mapa(self):
        c, m = self.mapa, 40
        u = (self.TAM - 2 * m) / LIM
        p = lambda pt: (m + pt[0] * u, self.TAM - m - pt[1] * u)
        c.delete("all")
        for v in range(LIM + 1):
            x, y = p((v, v))
            c.create_line(m, y, self.TAM - m, y, fill="#e7eff3")
            c.create_line(x, m, x, self.TAM - m, fill="#e7eff3")
            c.create_text(x, self.TAM - m + 14, text=str(v))
            c.create_text(m - 14, y, text=str(v))
        if self.todas.get():
            for o, _ in self.rutas:
                c.create_line(*[v for n in (NOMBRE, *o, NOMBRE) for v in p(PUNTOS[n])], fill=TENUE)
        orden = self.rutas[self.i][0]
        base = AZUL if self.i == 0 else VERDE
        # solo se dibujan los tramos ya recorridos
        for k, (a, b, d) in enumerate(tramos(orden)[:self.paso], 1):
            (x1, y1), (x2, y2) = p(PUNTOS[a]), p(PUNTOS[b])
            actual = (k == self.paso)
            c.create_line(x1, y1, x2, y2, fill=NARANJA if actual else base,
                          width=5 if actual else 3, arrow="last")
            c.create_text((x1 + x2) / 2 + 4, (y1 + y2) / 2 - 9, text=f"{d:.2f}", fill=ROJO,
                          font=("Segoe UI", 8, "bold"))
        for nombre, pt in PUNTOS.items():
            x, y = p(pt)
            c.create_oval(x - 11, y - 11, x + 11, y + 11, fill=VERDE if nombre == NOMBRE else AZUL,
                          outline="white", width=2)
            c.create_text(x, y, text="Al" if nombre == NOMBRE else nombre, fill="white",
                          font=("Segoe UI", 8, "bold"))
            c.create_text(x, y + 22, text=f"({pt[0]},{pt[1]})", font=("Segoe UI", 8))

    def xy_grafica(self, k, d):
        dist = [r[1] for r in self.rutas]
        lo, hi = min(dist), max(dist)
        x = self.ML + k * (self.GW - self.ML - self.MR) / (len(dist) - 1)
        y = self.GH - self.MB - (d - lo) / (hi - lo) * (self.GH - self.MT - self.MB)
        return x, y

    def dibujar_grafica(self):
        g, dist = self.grafica, [r[1] for r in self.rutas]
        g.delete("all")
        g.create_line(self.ML, self.MT, self.ML, self.GH - self.MB)
        g.create_line(self.ML, self.GH - self.MB, self.GW - self.MR, self.GH - self.MB)
        for k in range(6):
            d = min(dist) + (max(dist) - min(dist)) * k / 5
            y = self.xy_grafica(0, d)[1]
            g.create_line(self.ML, y, self.GW - self.MR, y, fill="#e7eff3")
            g.create_text(self.ML - 6, y, text=f"{d:.1f}", anchor="e", font=("Segoe UI", 8))
        for k in (0, 19, 39, 59, 79, 99, len(dist) - 1):
            g.create_text(self.xy_grafica(k, min(dist))[0], self.GH - self.MB + 12, text=str(k + 1),
                          font=("Segoe UI", 8))
        g.create_text(self.GW / 2, self.GH - 8, text="Ruta (de menor a mayor distancia)")
        g.create_line(*[v for k, d in enumerate(dist) for v in self.xy_grafica(k, d)], fill=AZUL, width=2)
        for k, color in ((0, VERDE), (self.i, ROJO)):
            x, y = self.xy_grafica(k, dist[k])
            g.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="white")
        x, y = self.xy_grafica(self.i, dist[self.i])
        g.create_text(x + 8, y - 12, text=f"#{self.i + 1}: {dist[self.i]:.2f}", fill=ROJO, anchor="w")

    def clic_grafica(self, e):
        k = round((e.x - self.ML) / (self.GW - self.ML - self.MR) * (len(self.rutas) - 1))
        self.ir(k)


if __name__ == "__main__":
    App().mainloop()