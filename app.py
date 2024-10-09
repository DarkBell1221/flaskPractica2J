from flask import Flask, render_template, request, jsonify, redirect
import mysql.connector
import pusher
from mysql.connector import Error

# Conexión a la base de datos
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )
    except Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id='1868490',
    key='e1d8c501f1496bf4614e',
    secret='7f77d21d3627c15b058c',
    cluster='us2',
    ssl=True
)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Registrar un nuevo curso y emitir evento con Pusher
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form.get("nombre_curso")
    telefono = request.form.get("telefono")
    con = get_db_connection()

    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor()
        sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
        val = (nombre, telefono)
        cursor.execute(sql, val)
        con.commit()

        # Disparar evento con Pusher al agregar un nuevo registro
        pusher_client.trigger("registros", "nuevo", {
            "nombre_curso": nombre,
            "telefono": telefono
        })

        return redirect("/registros")

    except Error as e:
        print(f"Error al insertar en la base de datos: {e}")
        return "Error al registrar datos", 500

    finally:
        cursor.close()
        con.close()

# Mostrar registros
@app.route("/registros")
def mostrar_registros():
    con = get_db_connection()

    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT Id_Curso, Nombre_Curso, Telefono FROM tst0_cursos")
        registros = cursor.fetchall()

        # Debug: Ver los registros en la consola
        print(f"Registros recuperados: {registros}")

        return render_template("inscripcion.html", registros=registros)

    except Error as e:
        print(f"Error al recuperar registros: {e}")
        return "Error al mostrar registros", 500

    finally:
        cursor.close()
        con.close()

# Editar un registro existente y emitir evento con Pusher
@app.route("/editar_registro/<int:id>", methods=["POST"])
def editar_registro(id):
    nuevo_nombre = request.form["nombre_curso"]
    nuevo_telefono = request.form["telefono"]

    con = get_db_connection()
    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE tst0_cursos
            SET Nombre_Curso = %s, Telefono = %s
            WHERE Id_Curso = %s
        """, (nuevo_nombre, nuevo_telefono, id))
        con.commit()

        # Emitimos el evento con Pusher para notificar la edición
        pusher_client.trigger("registros", "editar", {
            "id": id,
            "nombre_curso": nuevo_nombre,
            "telefono": nuevo_telefono
        })

        return redirect("/registros")

    except Error as e:
        print(f"Error al editar el registro: {e}")
        return "Error al editar el registro", 500

    finally:
        cursor.close()
        con.close()


# Eliminar un registro por Id y emitir evento con Pusher
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    con = get_db_connection()

    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor()
        sql = "DELETE FROM tst0_cursos WHERE Id_Curso = %s"
        cursor.execute(sql, (id,))
        con.commit()

        # Emitimos el evento con Pusher para notificar la eliminación
        pusher_client.trigger("registros", "eliminar", {"id": id})

        return redirect("/registros")

    except Error as e:
        print(f"Error al eliminar registro: {e}")
        return "Error al eliminar registro", 500

    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    app.run(debug=True)
