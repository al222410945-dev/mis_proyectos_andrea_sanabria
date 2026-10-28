"""
Gráfica de ventas mensuales para EcoMart.

Materia: Extracción de Conocimiento en Bases de Datos
Los valores son una estimación en miles de pesos.
"""

import matplotlib.pyplot as plt


meses = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
]
ventas = [85, 90, 96, 105, 120, 135, 150, 148, 160, 172, 181, 195]
posiciones = list(range(len(meses)))

promedio = sum(ventas) / len(ventas)
indice_maximo = max(range(len(ventas)), key=ventas.__getitem__)

fig, ax = plt.subplots(figsize=(13, 7), facecolor="#f8fafc")
ax.set_facecolor("white")

ax.fill_between(posiciones, ventas, color="#2563eb", alpha=0.08)
ax.plot(
    posiciones,
    ventas,
    color="#2563eb",
    linewidth=3.5,
    marker="o",
    markersize=8,
    markerfacecolor="white",
    markeredgecolor="#1d4ed8",
    markeredgewidth=2.2,
    label="Ventas mensuales (miles de pesos)",
    zorder=3,
)

ax.axhline(
    promedio,
    color="#16a34a",
    linestyle="--",
    linewidth=3,
    dashes=(7, 4),
    label=f"Promedio anual: {promedio:.1f} mil pesos",
    zorder=2,
)
ax.scatter(
    posiciones[indice_maximo],
    ventas[indice_maximo],
    facecolor="none",
    edgecolor="#111827",
    linewidth=2.5,
    marker="D",
    s=190,
    label="Máximo anual",
    zorder=4,
)

for x, venta in zip(posiciones, ventas):
    if x == posiciones[-2]:
        desplazamiento = (-22, 22)
    elif x == posiciones[-1]:
        desplazamiento = (24, 28)
    else:
        desplazamiento = (0, 10)
    ax.annotate(
        str(venta),
        (x, venta),
        xytext=desplazamiento,
        textcoords="offset points",
        ha="center",
        fontsize=9.5,
        fontweight="bold",
        color="#334155",
        bbox={
            "boxstyle": "round,pad=0.18",
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 0.85,
        },
    )

ax.annotate(
    "Máximo anual",
    xy=(posiciones[indice_maximo], ventas[indice_maximo]),
    xytext=(55, -45),
    textcoords="offset points",
    color="#111827",
    fontsize=10,
    fontweight="bold",
    arrowprops={"arrowstyle": "->", "color": "#111827", "lw": 1.7},
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#d1d5db"},
)

ax.annotate(
    f"Promedio: {promedio:.1f} mil pesos",
    xy=(posiciones[-1], promedio),
    xytext=(55, -100),
    textcoords="offset points",
    color="#15803d",
    fontsize=10,
    fontweight="bold",
    va="center",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#bbf7d0"},
    arrowprops={"arrowstyle": "-", "color": "#15803d", "lw": 1.2},
)

fig.suptitle(
    "Ventas mensuales de EcoMart",
    fontsize=22,
    fontweight="bold",
    color="#0f172a",
    y=0.985,
)
fig.text(
    0.5,
    0.90,
    "Estimación de enero a diciembre de 2026",
    ha="center",
    fontsize=12,
    color="#475569",
)
ax.set_xlabel("Mes", fontsize=12, labelpad=10)
ax.set_ylabel("Ventas (miles de pesos)", fontsize=12, labelpad=10)
ax.set_xticks(posiciones, meses)
ax.set_xlim(-0.35, posiciones[-1] + 4.5)
ax.set_ylim(0, 220)
ax.set_yticks(range(0, 221, 25))
ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.35)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#cbd5e1")
ax.spines["bottom"].set_color("#cbd5e1")
ax.tick_params(colors="#475569")
ax.legend(
    frameon=True,
    facecolor="white",
    edgecolor="#e2e8f0",
    framealpha=0.96,
    loc="upper left",
    fontsize=10,
)

fig.text(
    0.01,
    0.015,
    "Datos estimados | Elaboración propia | UTVT",
    fontsize=9,
    color="#64748b",
)
fig.tight_layout(rect=(0, 0.04, 1, 0.84))
fig.savefig("Grafica_Profesional_01.png", dpi=300, bbox_inches="tight")
plt.show()

print("=" * 60)
print("Gráfica generada correctamente.")
print("Archivo guardado como: Grafica_Profesional_01.png")
print("=" * 60)