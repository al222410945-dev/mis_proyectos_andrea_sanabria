# ==============================================================
#   GRÁFICA MEJORADA: ACTIVIDAD DE SAFEGUARDIA POR MES
# ==============================================================
#
# Basada en graficas1.py, pero adaptada al proyecto SafeGuardIA.
# Compara los datos de sus dos colecciones:
#   - usuarios   -> usuarios nuevos registrados cada mes
#   - incidentes -> incidentes reportados cada mes
#
# Mejoras respecto a la versión original:
#   - Dos líneas con colores distintos y coherentes con el resto
#     del proyecto.
#   - Los números de cada línea no se encimen: los de usuarios
#     van arriba y los de incidentes abajo.
#   - Línea de promedio de cada serie, con su etiqueta.
#   - Mes con más incidentes destacado y explicado.
#   - Conclusión escrita automáticamente a partir de los datos.
#
# NOTA: los datos son SIMULADOS. Para usar datos reales,
# cambia las dos listas de la sección DATOS (por ejemplo,
# con el conteo mensual de tus colecciones en MongoDB).
# ==============================================================

import matplotlib.pyplot as plt
import numpy as np

# ==========================================================
# COLORES (misma paleta en todo el proyecto)
# ==========================================================

COLOR_USUARIOS = "#2A9D8F"     # verde azulado
COLOR_INCIDENTES = "#E76F51"   # rojo anaranjado
COLOR_TEXTO = "#264653"        # azul oscuro
COLOR_GRIS = "#6C757D"

# ==========================================================
# DATOS (simulados)
# ==========================================================

meses = ["Abr", "May", "Jun", "Jul", "Ago", "Sep"]

usuarios_nuevos = [45, 62, 78, 95, 120, 150]
incidentes = [12, 18, 22, 35, 41, 58]

posiciones = np.arange(len(meses))

# ==========================================================
# CÁLCULOS PARA LA CONCLUSIÓN
# ==========================================================

promedio_usu = np.mean(usuarios_nuevos)
promedio_inc = np.mean(incidentes)

indice_max = int(np.argmax(incidentes))
mes_max = meses[indice_max]

# ==========================================================
# FIGURA
# ==========================================================

fig, ax = plt.subplots(figsize=(14, 8))

# ----------------------------------------------------------
# Líneas de datos
# ----------------------------------------------------------

ax.plot(posiciones, usuarios_nuevos, color=COLOR_USUARIOS, linewidth=3,
        marker="o", markersize=9, markerfacecolor="white",
        markeredgewidth=2.5, label="Usuarios nuevos")

ax.plot(posiciones, incidentes, color=COLOR_INCIDENTES, linewidth=3,
        marker="s", markersize=9, markerfacecolor="white",
        markeredgewidth=2.5, label="Incidentes reportados")

# ----------------------------------------------------------
# Valores sobre cada punto
# (usuarios arriba, incidentes abajo para que no se encimen)
# ----------------------------------------------------------

for x, y in zip(posiciones, usuarios_nuevos):
    ax.text(x, y + 6, str(y), ha="center", fontsize=11,
            color=COLOR_USUARIOS, fontweight="bold",
            bbox=dict(fc="white", ec="none", pad=1.5))

for x, y in zip(posiciones, incidentes):
    ax.text(x, y - 10, str(y), ha="center", fontsize=11,
            color=COLOR_INCIDENTES, fontweight="bold",
            bbox=dict(fc="white", ec="none", pad=1.5))

# ----------------------------------------------------------
# Líneas de promedio (punteadas, del mismo color de su serie)
# ----------------------------------------------------------

ax.axhline(promedio_usu, color=COLOR_USUARIOS, linestyle="--",
           linewidth=1.5, alpha=0.7)
ax.text(-0.4, promedio_usu + 3, f"Promedio usuarios: {promedio_usu:.0f}",
        color=COLOR_USUARIOS, fontsize=11, ha="left")

ax.axhline(promedio_inc, color=COLOR_INCIDENTES, linestyle="--",
           linewidth=1.5, alpha=0.7)
ax.text(-0.4, promedio_inc + 3, f"Promedio incidentes: {promedio_inc:.0f}",
        color=COLOR_INCIDENTES, fontsize=11, ha="left")

# ----------------------------------------------------------
# Destacar el mes con más incidentes
# ----------------------------------------------------------

ax.scatter(indice_max, incidentes[indice_max], s=320,
           facecolors="none", edgecolors=COLOR_TEXTO, linewidths=2.5,
           zorder=5)

ax.annotate(f"Más incidentes del periodo: {mes_max}",
            xy=(indice_max, incidentes[indice_max]),
            xytext=(indice_max - 1.5, incidentes[indice_max] + 17),
            arrowprops=dict(arrowstyle="->", color=COLOR_TEXTO, lw=2),
            fontsize=12, color=COLOR_TEXTO, fontweight="bold")

# ----------------------------------------------------------
# Títulos, etiquetas y leyenda
# ----------------------------------------------------------

fig.suptitle("Actividad de SafeGuardIA por mes",
             fontsize=22, fontweight="bold", color=COLOR_TEXTO)

ax.set_title("Usuarios nuevos e incidentes reportados  |  "
             "Abril - Septiembre 2026 (datos simulados)",
             fontsize=12, color=COLOR_GRIS, pad=12)

ax.set_xlabel("Mes", fontsize=14, fontweight="bold")
ax.set_ylabel("Cantidad de registros", fontsize=14, fontweight="bold")

ax.set_xticks(posiciones)
ax.set_xticklabels(meses, fontsize=12)
ax.set_ylim(0, max(usuarios_nuevos) + 30)
ax.set_xlim(-0.5, len(meses) - 0.5)

ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.5)
ax.set_axisbelow(True)

ax.legend(fontsize=12, loc="upper left", frameon=False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ----------------------------------------------------------
# Conclusión escrita con los datos
# ----------------------------------------------------------

fig.text(0.01, 0.01,
         f"Conclusión: los incidentes pasaron de {incidentes[0]} a "
         f"{incidentes[-1]} al mismo tiempo que los usuarios nuevos "
         f"pasaron de {usuarios_nuevos[0]} a {usuarios_nuevos[-1]}. "
         f"| SafeGuardIA | UTVT",
         fontsize=10, color=COLOR_GRIS)

plt.tight_layout(rect=(0, 0.03, 1, 1))

# ==========================================================
# GUARDAR Y MOSTRAR
# ==========================================================

plt.savefig("Grafica_Actividad_SafeGuardIA.png", dpi=300,
            bbox_inches="tight")

plt.show()

print("=" * 60)
print("Gráfica generada correctamente.")
print("Archivo guardado como: Grafica_Actividad_SafeGuardIA.png")
print("=" * 60)
