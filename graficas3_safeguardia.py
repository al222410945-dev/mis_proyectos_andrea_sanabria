# ==============================================================
#   PALETAS DE COLOR APLICADAS A SAFEGUARDIA
# ==============================================================
#
# Basada en graficas3.py. En lugar de solo mostrar paletas con
# datos al azar, aquí se USAN con datos del proyecto, eligiendo
# la paleta según el tipo de información:
#
#   - Total de incidentes por zona (categorías sin orden)
#         -> paleta "colorblind" (colores distintos, también
#            legibles para personas con daltonismo)
#
#   - Incidentes por zona y mes (de menos a más)
#         -> paleta "Reds" (más oscuro = más incidentes,
#            es decir, más riesgo)
#
# NOTA: los datos son SIMULADOS. Cámbialos por los de tu
# colección "incidentes" cuando los tengas.
# ==============================================================

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Para que los números simulados sean siempre los mismos
np.random.seed(7)

COLOR_TEXTO = "#264653"
COLOR_GRIS = "#6C757D"

# ==========================================================
# DATOS (simulados)
# ==========================================================

zonas = ["Parque", "Mercado", "Avenida", "Callejón",
         "Puente", "Plaza", "Escuela"]

meses = ["Abr", "May", "Jun", "Jul", "Ago", "Sep"]

# Tabla: cada fila es una zona y cada columna un mes
incidentes = np.random.randint(1, 12, size=(len(zonas), len(meses)))

# Total por zona, ordenado de mayor a menor
totales = incidentes.sum(axis=1)
orden = np.argsort(totales)[::-1]

zonas_ordenadas = [zonas[i] for i in orden]
totales_ordenados = totales[orden]

# ==========================================================
# FIGURA CON DOS GRÁFICAS
# ==========================================================

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(17, 8), gridspec_kw={"width_ratios": [1, 1.3]}
)

fig.suptitle("Incidentes reportados en SafeGuardIA por zona",
             fontsize=24, fontweight="bold", color=COLOR_TEXTO)

# ----------------------------------------------------------
# IZQUIERDA: barras horizontales (categorías -> "colorblind")
# ----------------------------------------------------------

colores = sns.color_palette("colorblind", len(zonas))

barras = ax1.barh(zonas_ordenadas, totales_ordenados, color=colores,
                  edgecolor=COLOR_TEXTO)

ax1.bar_label(barras, fontsize=12, fontweight="bold", padding=4)
ax1.invert_yaxis()    # la zona con más incidentes queda arriba

ax1.set_title("Total de incidentes (abril - septiembre)",
              fontsize=15, fontweight="bold", pad=12)
ax1.set_xlabel("Incidentes reportados", fontsize=13)
ax1.set_xlim(0, totales_ordenados.max() * 1.15)
ax1.tick_params(axis="y", labelsize=12)
ax1.grid(axis="x", linestyle="--", alpha=0.4)
ax1.set_axisbelow(True)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.text(0, -0.13,
         "Paleta 'colorblind': cada color es una zona distinta, sin orden.",
         transform=ax1.transAxes, fontsize=10, color=COLOR_GRIS)

# ----------------------------------------------------------
# DERECHA: mapa de calor (de menos a más -> "Reds")
# ----------------------------------------------------------

sns.heatmap(
    incidentes[orden],
    ax=ax2,
    cmap="Reds",
    annot=True,
    fmt="d",
    annot_kws={"fontsize": 11},
    linewidths=1,
    linecolor="white",
    xticklabels=meses,
    yticklabels=zonas_ordenadas,
    cbar_kws={"label": "Incidentes en el mes"},
)

ax2.set_title("Incidentes por mes y zona", fontsize=15,
              fontweight="bold", pad=12)
ax2.set_xlabel("Mes", fontsize=13)
ax2.set_ylabel("")
ax2.tick_params(axis="y", labelsize=12, rotation=0)
ax2.tick_params(axis="x", labelsize=12)

ax2.text(0, -0.13,
         "Paleta 'Reds': mientras más oscuro, más incidentes (más riesgo).",
         transform=ax2.transAxes, fontsize=10, color=COLOR_GRIS)

# ----------------------------------------------------------
# Pie de figura
# ----------------------------------------------------------

fig.text(0.01, 0.01,
         "Fuente: datos simulados | SafeGuardIA | UTVT",
         fontsize=10, color=COLOR_GRIS)

plt.tight_layout(rect=(0, 0.03, 1, 0.95))

plt.savefig("Grafica_Incidentes_Zonas.png", dpi=300, bbox_inches="tight")

plt.show()

print("=" * 60)
print("Gráfica generada correctamente.")
print("Archivo guardado como: Grafica_Incidentes_Zonas.png")
print("=" * 60)
