from flask import Flask
from markupsafe import escape

from flask import render_template
from flask import request

import pusher

import mysql.connector

import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
  
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()
  
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
  
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

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_cursos (Nombre, Asunto) VALUES (%s, %s, %)"
    val = (args["Nombre"], args["Asunto"])
    cursor.execute(sql, val)

    con.commit()
    con.close()
 
    pusher_client.trigger("registrosNombre", "registroAsunto", args)
    return args

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos ORDER BY Id_Cursos DESC")
    registros = cursor.fetchall()

    con.close()

    return registros
