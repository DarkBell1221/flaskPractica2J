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

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/registrar", methods=["POST"])  # Cambia el método a POST
def registrar():
    nombre = request.form.get("Nombre")
    telefono = request.form.get("Telefono")
    
    con = get_db_connection()

    if con is None:
        return jsonify({"error": "Error en la conexión a la base de datos"}), 500

    try:
        cursor = con.cursor()
        sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
        val = (nombre, telefono)
        cursor.execute(sql, val)
        con.commit()

        # Trigger en Pusher para actualizar en tiempo real
        data = {"Nombre_Curso": nombre, "Telefono": telefono}
        pusher_client.trigger("cursos-channel", "curso-registrado", data)

        return jsonify({"success": "Curso registrado con éxito"}), 200

    except Error as e:
        print(f"Error al insertar en la base de datos: {e}")
        return jsonify({"error": "Error al registrar datos"}), 500

    finally:
        cursor.close()
        con.close()

@app.route("/buscar")
def buscar():
    con = get_db_connection()

    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tst0_cursos ORDER BY Id_Cursos DESC")
        registros = cursor.fetchall()

        return jsonify({"registros": registros}), 200

    except Error as e:
        print(f"Error al buscar datos: {e}")
        return "Error al buscar registros", 500

    finally:
        cursor.close()
        con.close()

@app.route("/registros")
def mostrar_registros():
    con = get_db_connection()

    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT Nombre_Curso, Telefono FROM tst0_cursos")
        registros = cursor.fetchall()

        return render_template("inscripcion.html", registros=registros)

    except Error as e:
        print(f"Error al recuperar registros: {e}")
        return "Error al mostrar registros", 500

    finally:
        cursor.close()
        con.close()

# Eliminar por número de teléfono
@app.route("/eliminar/<string:telefono>", methods=["POST"])
def eliminar(telefono):
    con = get_db_connection()

    if con is None:
        return "Error en la conexión a la base de datos", 500

    try:
        cursor = con.cursor()
        sql = "DELETE FROM tst0_cursos WHERE Telefono = %s"
        cursor.execute(sql, (telefono,))
        con.commit()
        return redirect("/registros")  # Redirige a la lista de registros

    except Error as e:
        print(f"Error al eliminar registro: {e}")
        return "Error al eliminar registro", 500

    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    app.run(debug=True)
