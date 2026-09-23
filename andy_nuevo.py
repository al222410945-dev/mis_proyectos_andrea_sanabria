# Sistema de autodiagnóstico de equipo (versión con diccionario y resumen de fallas)

# pregunta si/no y repite si la respuesta no es valida
def pedir_si_no(pregunta):
    while True:
        r = input(pregunta + " (si/no): ").strip().lower()
        if r in ("si", "no"):
            return r == "si"
        print("Respuesta no valida, escribe 'si' o 'no'.")

def main():
    print("=" * 55)
    print("       SISTEMA DE AUTODIAGNÓSTICO DE EQUIPO")
    print("=" * 55)

    # cada prueba tiene su pregunta y su solucion
    pruebas = {
        "P": ("¿Tiene electricidad?", "Revisar cable de corriente y toma eléctrica"),
        "Q": ("¿Enciende?", "Revisar fuente de poder o tarjeta gráfica"),
        "R": ("¿El monitor muestra imagen?", "Revisar cable VGA/HDMI y monitor"),
        "S": ("¿Hay sonido?", "Revisar altavoces, conexiones y volumen"),
        "T": ("¿Conecta a internet?", "Revisar cable de red, router o WiFi"),
    }

    # hacemos todas las preguntas y guardamos respuestas
    resultados = {}
    for clave, (pregunta, _) in pruebas.items():
        resultados[clave] = pedir_si_no(pregunta)

    # lista con las soluciones de lo que fallo
    fallas = [pruebas[c][1] for c, ok in resultados.items() if not ok]

    print("\n" + "=" * 55)
    print("                  DIAGNÓSTICO")
    print("=" * 55)

    # si no hay fallas todo esta bien, si no mostramos la lista
    if not fallas:
        print("El equipo funciona correctamente, sin problemas detectados.")
    else:
        print(f"Se detectaron {len(fallas)} problema(s):")
        for i, solucion in enumerate(fallas, 1):
            print(f"  {i}. {solucion}")

main()
