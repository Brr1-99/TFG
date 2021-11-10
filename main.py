from _datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_paginate import Pagination, get_page_parameter
import bcrypt

app = Flask(__name__)

# Conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'

mysql = MySQL(app)

app2 = Flask(__name__)

# Conexión MySQL
app2.config['MYSQL_HOST'] = 'localhost'
app2.config['MYSQL_USER'] = 'root'
app2.config['MYSQL_PASSWORD'] = ''
app2.config['MYSQL_DB'] = 'Inventario'

mysql2 = MySQL(app2)

# Encriptamiento
semilla = bcrypt.gensalt()

# Ajustes
app.secret_key = "sE+gcUVWsU491sJ"

# Variables globales
mensaje_error = False
fecha_hoy = date.today()


# Rutas Web
@app.route('/')
def main():
    return render_template('portada.html')


@app.route('/inicio')
def inicio():
    login = comprobar_sesion()
    if login:
        return render_template('index.html')
    else:
        return render_template('ingresar.html')


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "GET":
        login = comprobar_sesion()
        if login:
            return render_template('index.html')
        else:
            return render_template('registrar.html')
    else:
        nombre = request.form['Nombre registro']
        correo = request.form['Correo registro']
        password = request.form['Password registro']
        password_encode = password.encode("utf-8")
        encriptado = bcrypt.hashpw(password_encode, semilla)

        cursor = mysql.connection.cursor()
        cursor.execute("""INSERT INTO `Usuarios`(`Nombre registro`,`Correo registro`, `Contraseña`)
                VALUES ( %s, %s, %s )""", (nombre, correo, encriptado))
        mysql.connection.commit()

        session['Nombre registro'] = nombre
        session['Correo registro'] = correo

        flash("Se ha registrado correctamente. Por favor inicie sesión")

        return render_template('ingresar.html')


@app.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if request.method == "GET":
        login = comprobar_sesion()
        if login:
            return redirect(url_for('index'))
        else:
            return render_template('ingresar.html')
    else:
        correo = request.form['Correo login']
        password = request.form['Password login']
        password_encode = password.encode('utf-8')
        cursor = mysql.connection.cursor()

        cursor.execute("""SELECT  `Correo registro` , `Contraseña`, `Nombre registro` 
        FROM `Usuarios` 
        WHERE `Correo registro` = %s """, [correo])

        mysql.connection.commit()

        usuario = cursor.fetchone()

        cursor.close()

        if usuario:
            encriptado = usuario[1]
            if encriptado == bcrypt.hashpw(password_encode, encriptado.encode('utf-8')).decode('utf-8'):
                session['Nombre registro'] = usuario[2]
                session['Correo registro'] = correo

                return redirect(request.referrer)

            else:
                flash("La contraseña es incorrecta")

                return render_template('ingresar.html')

        else:
            flash("El correo no existe, por favor regístrese")

            return render_template('registrar.html')


@app.route('/salir')
def salir():
    session.clear()
    return render_template('portada.html')


@app.route('/index')
def index():
    login = comprobar_sesion()
    if login:
        global fecha_hoy
        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page*limit-limit
        cursor = mysql.connection.cursor()

        cursor.execute('Select * FROM vigo ')

        datos = cursor.fetchall()
        total = len(datos)
        cur = mysql.connection.cursor()

        cur.execute('Select * FROM vigo ORDER BY `Fecha Modificación` DESC LIMIT %s OFFSET %s', (limit, offset))

        ult_valores = cur.fetchall()
        cur.close()

        pagination = Pagination(page=page, per_page=limit, total=total, record_name='index')
        return render_template('index.html',
                               pagination=pagination, contacts=ult_valores, mensaje=mensaje_error, fecha=fecha_hoy)
    else:
        return render_template('ingresar.html')


@app.route('/add_contact', methods=['POST'])
def add_contact():
    global mensaje_error
    global fecha_hoy
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False
            pieza = request.form['pieza']
            cantidad = request.form['cantidad']
            fecha = request.form['fecha registro']
            if not fecha:
                fecha = fecha_hoy
            cursor = mysql.connection.cursor()
            cursor.execute("""INSERT INTO `vigo`(`nombre producto`,`cantidad`, `fecha registro`)
             VALUES ( %s, %s, %s )""", (pieza, cantidad, fecha))
            mysql.connection.commit()
            flash('Item añadido correctamente')
            return redirect(url_for('index'))
    else:
        return render_template('ingresar.html')


@app.route('/edit/<string:id>')
def edit_contact(id):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        mensaje_error = False
        cursor = mysql.connection.cursor()
        cursor.execute('Select * FROM vigo WHERE id = {0}'.format(id))
        datos = cursor.fetchall()
        return render_template('edit.html', contact=datos[0])
    else:
        return render_template('ingresar.html')


@app.route('/update/<string:id>', methods=['POST'])
def update_contact(id):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False
            pieza = request.form['pieza']
            cantidad = request.form['cantidad']
            fecha = request.form['fecha registro']
            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE `vigo`
                SET `nombre producto` = %s,
                `cantidad` = %s,
                `fecha registro`= %s
                WHERE id = %s """, (pieza, cantidad, fecha, id))
            mysql.connection.commit()
            flash('Pieza actualizada correctamente')
            return redirect(url_for('index'))
    else:
        return render_template('ingresar.html')


@app.route('/delete/<string:id>')
def delete_contact(id):
    login = comprobar_sesion()
    if login:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM `vigo` WHERE id = {0}'.format(id))
        mysql.connection.commit()
        flash('Item eliminado correctamente')
        return redirect(url_for('index'))
    else:
        return render_template('ingresar.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False
            valor = request.form['input2']
            opcion = request.form['opciones']
            cursor = mysql.connection.cursor()
            cursor.execute(""" SELECT * 
            FROM `vigo` 
            WHERE `{0}`= '{1}'""".format(opcion, valor))
            mysql.connection.commit()
            datos = cursor.fetchall()

            cursorcuenta = mysql.connection.cursor()
            cursorcuenta.execute(""" SELECT SUM(`cantidad`) FROM `vigo` WHERE `{0}` = '{1}'""".format(opcion, valor))
            datoscuenta = cursorcuenta.fetchall()

            page = request.args.get(get_page_parameter(), type=int, default=1)
            limit = 5
            offset = page * limit - limit

            total = len(datos)

            if total > 0:
                cur = mysql.connection.cursor()

                cur.execute("""Select * 
                FROM `vigo` 
                WHERE `{0}`= '{1}'ORDER BY `Fecha Modificación` 
                DESC LIMIT {2} OFFSET {3}""".format(opcion, valor, limit, offset))

                valores = cur.fetchall()
                cur.close()

                pagination2 = Pagination(page=page, per_page=limit, total=total, record_name='search')

                return render_template('search.html', pagination=pagination2, busqueda=valores, datos=datoscuenta)
            else:
                mensaje_error = True
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return render_template('ingresar.html')

# Funciones Recurrentes


def comprobar_sesion():
    validez = False
    nombre = session.get('Nombre registro')
    if nombre:
        validez = True
    return validez


if __name__ == '__main__':
    app.run(port=3000, debug=True)
