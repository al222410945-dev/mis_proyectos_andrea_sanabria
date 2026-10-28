"""
==============================================================
Primer Gráfico con Matplotlib
==============================================================
Materia: Extracción de Conocimiento en Bases de Datos
Objetivo: Aprender a construir una gráfica utilizando Matplotlib.
==============================================================
"""

# ============================================================
# IMPORTACIÓN DE LIBRERÍAS
# ============================================================
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# DATOS
# ============================================================
# Meses del año
meses = [
    "Ene", "Feb", "Mar", "Abr",
    "May", "Jun", "Jul", "Ago",
    "Sep", "Oct", "Nov", "Dic"
]

# Ventas simuladas (miles de pesos)
ventas = [85, 90, 96, 105, 120, 135, 150, 148, 160, 172, 181, 195]

# ============================================================
# CONFIGURACIÓN GENERAL ESTABLECE EL TAMAÑO DE LA FIGURA
# ============================================================
fig, ax = plt.subplots(figsize=(14, 8))

# ============================================================
# GRÁFICA PRINCIPAL (LÍNEA CON COLOR Y MARCADORES)
# ============================================================
ax.plot(
    meses,
    ventas,
    color="#1f77b4",
    linewidth=3,
    marker="o",
    markersize=8,
    markerfacecolor="white",
    markeredgewidth=2,
    label="Ventas mensuales"
)

# ============================================================
# LÍNEA DE PROMEDIO
# ============================================================
promedio = np.mean(ventas)
ax.axhline(
    promedio,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Promedio"
)

# Texto descriptivo del promedio dentro del área
ax.text(
    10.5,
    promedio + 3,
    f"Promedio = {promedio:.1f} mil pesos",
    color="red",
    fontsize=11,
    fontweight="bold"
)

# ============================================================
# DESTACAR EL MÁXIMO
# ============================================================
indice_max = np.argmax(ventas)
ax.scatter(
    meses[indice_max],
    ventas[indice_max],
    color="green",
    s=180,
    zorder=5,
    label="Máximo"
)

# Anotación destacada del máximo
ax.annotate(
    "Mayor venta del año\n(195 mil pesos)",
    xy=(meses[indice_max], ventas[indice_max]),
    xytext=(7.5, 202),
    arrowprops=dict(
        arrowstyle="->",
        color="green",
        lw=2,
        connectionstyle="arc3,rad=-0.1"
    ),
    fontsize=11,
    fontweight="bold",
    color="green",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f8f5", edgecolor="green", alpha=0.9)
)

# ============================================================
# ANOTACIONES EN CADA PUNTO (NÚMEROS VISIBLES SIN EMPALMARSE)
# ============================================================
for x, y in zip(meses, ventas):
    ax.text(
        x,
        y + 3.5,
        f"${y}k",
        fontsize=10,
        ha="center",
        va="bottom",
        fontweight="bold"
    )

# ============================================================
# ENCABEZADOS (TÍTULO PRINCIPAL ARRIBA, SUBTÍTULO ABAJO)
# ============================================================
# 1. Título principal (arriba)
fig.suptitle(
    "Ventas mensuales de la empresa EcoMart",
    fontsize=20,
    fontweight="bold",
    y=0.98
)

# 2. Subtítulo con contexto (debajo del título principal)
ax.set_title(
    "Periodo Enero - Diciembre 2026",
    fontsize=13,
    color="gray",
    pad=15
)

# ============================================================
# ETIQUETAS Y UNIDADES DE EJES
# ============================================================
ax.set_xlabel("Mes", fontsize=14, fontweight="bold", labelpad=10)
ax.set_ylabel("Ventas (Miles de pesos)", fontsize=14, fontweight="bold", labelpad=10)

# Margen superior en el eje Y para evitar cortes
ax.set_ylim(75, 220)

# ============================================================
# CUADRÍCULA Y ESTILO DE MARCO
# ============================================================
ax.grid(linestyle="--", linewidth=0.7, alpha=0.6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ============================================================
# LEYENDA
# ============================================================
ax.legend(fontsize=11, loc="upper left", frameon=True)

# ============================================================
# PIE DE FIGURA DEBAJO DE LA GRÁFICA Y CENTRADO
# ============================================================
fig.text(
    0.5,
    0.01,
    "Conclusión: Estimado de las ventas | Elaboración propia | UTVT",
    fontsize=10,
    color="gray",
    ha="center"
)

# ============================================================
# AJUSTAR ESPACIOS, GUARDAR Y MOSTRAR
# ============================================================
plt.tight_layout(rect=[0, 0.04, 1, 0.96])

plt.savefig(
    "Grafica_Profesional_01.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("=" * 60)
print("Gráfica generada correctamente.")
print("Archivo guardado como: Grafica_Profesional_01.png")
print("=" * 60)