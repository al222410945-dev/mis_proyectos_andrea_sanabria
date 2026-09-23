import random
import tkinter as tk

ventana = tk.Tk()
ventana.title("SISTEMA DE DIAGNOSTICO")
ventana.geometry("750x480")
ventana.config(bg="#e8f0f2")

tk.Label(ventana, text="SISTEMA DE DIAGNOSTICO", font=("Arial", 14, "bold"), bg="#2c7a7b", fg="white", pady=10).pack(fill="x")

izquierda = tk.Frame(ventana, bg="#e8f0f2")
izquierda.pack(side="left", padx=20, pady=10, fill="y")

derecha = tk.Frame(ventana, bg="#e8f0f2")
derecha.pack(side="right", padx=20, pady=10, fill="both", expand=True)

tk.Label(izquierda, text="Nombre:", bg="#e8f0f2", font=("Arial", 10)).pack()
nombre = tk.Entry(izquierda, font=("Arial", 10))
nombre.pack()

tk.Label(izquierda, text="Edad:", bg="#e8f0f2", font=("Arial", 10)).pack()
edad = tk.Entry(izquierda, font=("Arial", 10))
edad.pack()

tk.Label(izquierda, text="Oxigenacion:", bg="#e8f0f2", font=("Arial", 10)).pack()
oxigenacion = tk.Entry(izquierda, font=("Arial", 10))
oxigenacion.pack()

tk.Label(izquierda, text="Frecuencia cardiaca:", bg="#e8f0f2", font=("Arial", 10)).pack()
frecuencia = tk.Entry(izquierda, font=("Arial", 10))
frecuencia.pack()

tk.Label(izquierda, text="Presion arterial:", bg="#e8f0f2", font=("Arial", 10)).pack()
presion = tk.Entry(izquierda, font=("Arial", 10))
presion.pack()

tk.Label(izquierda, text="Peso:", bg="#e8f0f2", font=("Arial", 10)).pack()
peso = tk.Entry(izquierda, font=("Arial", 10))
peso.pack()

tk.Label(izquierda, text="Talla:", bg="#e8f0f2", font=("Arial", 10)).pack()
talla = tk.Entry(izquierda, font=("Arial", 10))
talla.pack()

def diagnosticar():
    P = int(oxigenacion.get()) < 90
    Q = int(frecuencia.get()) < 60 or int(frecuencia.get()) > 100
    R = int(presion.get()) > 140

    imc = float(peso.get()) / (float(talla.get()) / 100) ** 2
    S = imc >= 25

    texto = "Diagnostico:\n"

    if P:
        texto += "Sintoma: oxigenacion baja\nRecomendacion: acudir al medico\n"
    if Q:
        texto += "Sintoma: frecuencia cardiaca fuera de rango\nRecomendacion: descansar\n"
    if R:
        texto += "Sintoma: presion arterial alta\nRecomendacion: reducir sal\n"
    if S:
        texto += "Sintoma: sobrepeso (IMC alto)\nRecomendacion: mejorar la dieta y hacer ejercicio\n"

    riesgo = P or Q or R or S
    cantidad = P + Q + R + S

    if not riesgo:
        texto += "\nEl paciente esta bien\n"
        resultado.config(fg="green")
    else:
        texto += "\nEl paciente necesita atencion\n"
        resultado.config(fg="red")

    if cantidad == 0:
        texto += "Nivel de riesgo: bajo\n"
    elif cantidad <= 2:
        texto += "Nivel de riesgo: medio\n"
    else:
        texto += "Nivel de riesgo: alto\n"

    numero_cita = random.randint(1, 20)

    texto += "\nCita generada:\n"
    texto += "Numero de cita: " + str(numero_cita) + "\n"
    texto += "Fecha: " + str(numero_cita) + "/10/2026\n"
    texto += "Hora: 10:00\n"
    texto += "\nResumen del paciente:\n"
    texto += "Nombre: " + nombre.get() + "\n"
    texto += "Edad: " + edad.get() + "\n"
    texto += "Sintomas detectados: " + str(cantidad)

    resultado.config(text=texto)

def limpiar():
    nombre.delete(0, "end")
    edad.delete(0, "end")
    oxigenacion.delete(0, "end")
    frecuencia.delete(0, "end")
    presion.delete(0, "end")
    peso.delete(0, "end")
    talla.delete(0, "end")
    resultado.config(text="", fg="black")

boton = tk.Button(izquierda, text="Diagnosticar", command=diagnosticar, bg="#2c7a7b", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5)
boton.pack(pady=(15, 5))

boton_limpiar = tk.Button(izquierda, text="Limpiar", command=limpiar, bg="#888888", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5)
boton_limpiar.pack()

resultado = tk.Label(derecha, text="", justify="left", anchor="nw", bg="white", font=("Arial", 9), relief="solid", bd=1, padx=10, pady=10)
resultado.pack(fill="both", expand=True)

ventana.mainloop()