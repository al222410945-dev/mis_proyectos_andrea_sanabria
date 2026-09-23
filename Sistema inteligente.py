
print("=" * 55)
print("       SISTEMA DE AUTODIAGNÓSTICO DE EQUIPO")
print("=" * 55)

respuesta = input("¿Tiene electricidad? (si/no): ").lower()
P = respuesta == "si"
if not P:
    print("Verifica si hay luz en casa y si el equipo está conectado")

respuesta = input("¿Enciende? (si/no): ").lower()
Q = respuesta == "si"
if not Q:
    print("Presiona el botón de encendido y verifica si hay luces o sonido")

respuesta = input("¿El monitor muestra imagen? (si/no): ").lower()
R = respuesta == "si"
if not R:
    print("Verifica si el monitor está encendido y conectado correctamente")

respuesta = input("¿Hay sonido? (si/no): ").lower()
S = respuesta == "si"
if not S:
    print("Verifica si los altavoces están conectados y el volumen no está en mute")

respuesta = input("¿Conecta a internet? (si/no): ").lower()
T = respuesta == "si"
if not T:
    print("Verifica si el cable de red está conectado o si el WiFi está activo")


resultado = P and Q and R and S and T


if (not P) or (not Q) or (not R) or (not S) or (not T):
    
    
    if not P:
        print("Diagnostico: Revisar la alimentación o verifica cable de corriente y toma eléctrica")
    
    elif not Q:
        print("Diagnostico: Revisar fuente de poder o tarjeta grafica - verifica luces del equipo")
    
    elif not R:
        print("Diagnostico: Revisar monitor o memoria o verifica cable VGA/HDMI y monitor")
    
    elif not S:
        print("Diagnostico: Revisar audio o verifica altavoces, conexiones y volumen")
    
    elif not T:
        print("Diagnostico: Revisar red o verifica cable de red, router o configuración WiFi")

else:
    print("Diagnostico: El equipo funciona correctamente y sin problemas detectados")