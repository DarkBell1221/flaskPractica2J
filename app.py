from flask import Flask, render_template, request
from markupsafe import escape
import pusher
import mysql.connector
import pytz

# Definir función para manejar la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    pusher_client = pusher.Pusher(
        app_id='1868490',
        key='e1d8c501f1496bf4614e',
        secret='7f77d21d3627c15b058c',
        cluster='us2',
        ssl=True
    )

    con = get_db_connection()
    cursor = con.cursor()

    sql = "INSERT INTO tst0_cursos (Nombre, Asunto) VALUES (%s, %s)"
    val = (args["Nombre"], args["Asunto"])
    cursor.execute(sql, val)

    con.commit()
    cursor.close()
    con.close()

    pusher_client.trigger("registrosNombre", "registroAsunto", args)
    return args

@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos ORDER BY Id_Cursos DESC")
    registros = cursor.fetchall()
    
    cursor.close()
    con.close()

    # Procesar registros y devolver una lista de resultados
    return {"registros": registros}

if __name__ == "__main__":
    app.run(debug=True)
