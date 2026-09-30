
import random
import tkinter as tk
from tkinter import messagebox

from conexion import database, collection
from bson import ObjectId


ventana = tk.Tk()
ventana.title("SISTEMA DE DIAGNOSTICO")
ventana.geometry("850x550")
ventana.config(bg="#e8f0f2")


tk.Label(
    ventana,
    text="SISTEMA DE DIAGNOSTICO",
    font=("Arial", 14, "bold"),
    bg="#2c7a7b",
    fg="white",
    pady=10
).pack(fill="x")


izquierda = tk.Frame(ventana, bg="#e8f0f2")
izquierda.pack(side="left", padx=20, pady=10, fill="y")


derecha = tk.Frame(ventana, bg="#e8f0f2")
derecha.pack(side="right", padx=20, pady=10, fill="both", expand=True)


# Variable para saber qué registro se está editando
registro_editando = None


# =========================
# CAMPOS DEL PACIENTE
# =========================

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


# =========================
# FUNCIÓN PARA DIAGNOSTICAR
# =========================

def diagnosticar():

    try:
        P = int(oxigenacion.get()) < 90
        Q = int(frecuencia.get()) < 60 or int(frecuencia.get()) > 100
        R = int(presion.get()) > 140

        imc = float(peso.get()) / (float(talla.get()) / 100) ** 2
        S = imc >= 25

    except ValueError:
        messagebox.showerror(
            "Error",
            "Por favor, introduce valores numéricos válidos."
        )
        return

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
        nivel_riesgo = "bajo"
        texto += "Nivel de riesgo: bajo\n"
    elif cantidad <= 2:
        nivel_riesgo = "medio"
        texto += "Nivel de riesgo: medio\n"
    else:
        nivel_riesgo = "alto"
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

    datos = {
        "nombre": nombre.get(),
        "edad": edad.get(),
        "oxigenacion": oxigenacion.get(),
        "frecuencia_cardiaca": frecuencia.get(),
        "presion_arterial": presion.get(),
        "peso": peso.get(),
        "talla": talla.get(),
        "imc": imc,
        "oxigenacion_baja": P,
        "frecuencia_fuera_rango": Q,
        "presion_alta": R,
        "sobrepeso": S,
        "sintomas_detectados": cantidad,
        "nivel_riesgo": nivel_riesgo,
        "numero_cita": numero_cita,
        "fecha_cita": str(numero_cita) + "/10/2026",
        "hora_cita": "10:00"
    }

    try:
        collection.insert_one(datos)

        resultado.config(text=texto)

        actualizar_lista()

        messagebox.showinfo(
            "Registro guardado",
            "El diagnóstico se guardó correctamente en MongoDB."
        )

    except Exception as e:
        messagebox.showerror(
            "Error de MongoDB",
            "No se pudo guardar el registro:\n" + str(e)
        )


# =========================
# LIMPIAR CAMPOS
# =========================

def limpiar():

    global registro_editando

    nombre.delete(0, "end")
    edad.delete(0, "end")
    oxigenacion.delete(0, "end")
    frecuencia.delete(0, "end")
    presion.delete(0, "end")
    peso.delete(0, "end")
    talla.delete(0, "end")

    resultado.config(text="", fg="black")

    registro_editando = None

    boton_editar.config(text="Editar")


# =========================
# ACTUALIZAR LISTA
# =========================

def actualizar_lista():

    lista.delete(0, tk.END)

    try:

        registros = collection.find().sort("_id", -1)

        for registro in registros:

            texto_registro = (
                str(registro.get("nombre", "Sin nombre"))
                + " | Edad: "
                + str(registro.get("edad", ""))
                + " | Riesgo: "
                + str(registro.get("nivel_riesgo", ""))
            )

            lista.insert(tk.END, texto_registro)

            # Guardamos el ID del registro
            lista_ids.append(str(registro["_id"]))

    except Exception as e:

        messagebox.showerror(
            "Error",
            "No se pudieron cargar los registros:\n" + str(e)
        )


# =========================
# CARGAR REGISTRO PARA EDITAR
# =========================

def editar_registro():

    global registro_editando

    seleccion = lista.curselection()

    if not seleccion:

        messagebox.showwarning(
            "Seleccionar registro",
            "Selecciona un registro de la lista para editar."
        )
        return

    indice = seleccion[0]

    # Si no estamos editando, cargar el registro
    if registro_editando is None:

        id_registro = lista_ids[indice]

        registro = collection.find_one({
            "_id": ObjectId(id_registro)
        })

        if registro:

            nombre.delete(0, "end")
            nombre.insert(0, registro.get("nombre", ""))

            edad.delete(0, "end")
            edad.insert(0, registro.get("edad", ""))

            oxigenacion.delete(0, "end")
            oxigenacion.insert(0, registro.get("oxigenacion", ""))

            frecuencia.delete(0, "end")
            frecuencia.insert(0, registro.get("frecuencia_cardiaca", ""))

            presion.delete(0, "end")
            presion.insert(0, registro.get("presion_arterial", ""))

            peso.delete(0, "end")
            peso.insert(0, registro.get("peso", ""))

            talla.delete(0, "end")
            talla.insert(0, registro.get("talla", ""))

            registro_editando = id_registro

            boton_editar.config(text="Guardar edición")

            resultado.config(
                text="Registro cargado.\nModifica los datos y pulsa 'Guardar edición'.",
                fg="black"
            )


    # Si ya estamos editando, guardar los cambios
    else:

        try:

            P = int(oxigenacion.get()) < 90
            Q = int(frecuencia.get()) < 60 or int(frecuencia.get()) > 100
            R = int(presion.get()) > 140

            imc = float(peso.get()) / (float(talla.get()) / 100) ** 2
            S = imc >= 25

            cantidad = P + Q + R + S

            if cantidad == 0:
                nivel_riesgo = "bajo"
            elif cantidad <= 2:
                nivel_riesgo = "medio"
            else:
                nivel_riesgo = "alto"

            datos_actualizados = {
                "nombre": nombre.get(),
                "edad": edad.get(),
                "oxigenacion": oxigenacion.get(),
                "frecuencia_cardiaca": frecuencia.get(),
                "presion_arterial": presion.get(),
                "peso": peso.get(),
                "talla": talla.get(),
                "imc": imc,
                "oxigenacion_baja": P,
                "frecuencia_fuera_rango": Q,
                "presion_alta": R,
                "sobrepeso": S,
                "sintomas_detectados": cantidad,
                "nivel_riesgo": nivel_riesgo
            }

            collection.update_one(
                {"_id": ObjectId(registro_editando)},
                {"$set": datos_actualizados}
            )

            messagebox.showinfo(
                "Registro actualizado",
                "El registro se actualizó correctamente."
            )

            registro_editando = None

            boton_editar.config(text="Editar")

            actualizar_lista()

            resultado.config(
                text="Registro actualizado correctamente.",
                fg="green"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Verifica que los campos numéricos sean correctos."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                "No se pudo actualizar el registro:\n" + str(e)
            )


# =========================
# ELIMINAR REGISTRO
# =========================

def eliminar_registro():

    seleccion = lista.curselection()

    if not seleccion:

        messagebox.showwarning(
            "Seleccionar registro",
            "Selecciona un registro de la lista para eliminar."
        )
        return

    indice = seleccion[0]
    id_registro = lista_ids[indice]

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Seguro que deseas eliminar este registro?"
    )

    if confirmar:

        try:

            collection.delete_one({
                "_id": ObjectId(id_registro)
            })

            messagebox.showinfo(
                "Registro eliminado",
                "El registro se eliminó correctamente."
            )

            actualizar_lista()
            limpiar()

        except Exception as e:

            messagebox.showerror(
                "Error",
                "No se pudo eliminar el registro:\n" + str(e)
            )


# =========================
# BOTONES
# =========================

boton = tk.Button(
    izquierda,
    text="Diagnosticar",
    command=diagnosticar,
    bg="#2c7a7b",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=20,
    pady=5
)

boton.pack(pady=(15, 5))


boton_limpiar = tk.Button(
    izquierda,
    text="Limpiar",
    command=limpiar,
    bg="#888888",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=20,
    pady=5
)

boton_limpiar.pack(pady=3)


boton_editar = tk.Button(
    izquierda,
    text="Editar",
    command=editar_registro,
    bg="#d69e2e",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=20,
    pady=5
)

boton_editar.pack(pady=3)


boton_eliminar = tk.Button(
    izquierda,
    text="Eliminar",
    command=eliminar_registro,
    bg="#c53030",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=20,
    pady=5
)

boton_eliminar.pack(pady=3)


# =========================
# RESULTADO
# =========================

resultado = tk.Label(
    derecha,
    text="",
    justify="left",
    anchor="nw",
    bg="white",
    font=("Arial", 9),
    relief="solid",
    bd=1,
    padx=10,
    pady=10
)

resultado.pack(fill="both", expand=True)


# =========================
# LISTA DE REGISTROS
# =========================

tk.Label(
    derecha,
    text="Registros guardados:",
    bg="#e8f0f2",
    font=("Arial", 10, "bold")
).pack(pady=(10, 3))


lista_ids = []

lista = tk.Listbox(
    derecha,
    height=7,
    font=("Arial", 9)
)

lista.pack(fill="x", padx=5, pady=5)


# Cargar registros existentes al iniciar
actualizar_lista()


ventana.mainloop()
