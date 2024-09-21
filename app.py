from flask import Flask, render_template, request, jsonify
import mysql.connector

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    # Inserta los datos en la tabla
    sql = "INSERT INTO tst0_cursos (Nombre, Asunto) VALUES (%s, %s)"
    val = (args["Nombre"], args["Asunto"])
    cursor.execute(sql, val)

    con.commit()
    con.close()
    
    return jsonify({"status": "ok", "Nombre": args["Nombre"], "Asunto": args["Asunto"]})

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Cursos, Nombre, Asunto FROM tst0_cursos ORDER BY Id_Cursos DESC")
    registros = cursor.fetchall()

    con.close()
    return jsonify(registros)

if __name__ == "__main__":
    app.run(debug=True)
