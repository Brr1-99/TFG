from _datetime import date
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_paginate import Pagination, get_page_parameter
import bcrypt

# Conexión a bases de datos
mydb1 = MySQLdb.connect(host='localhost',
                        user='root',
                        password='',
                        db='inventario')

cursor1 = mydb1.cursor()

mydb2 = MySQLdb.connect(host='localhost',
                        user='root',
                        password='',
                        db='manten_correctivo')

cursor2 = mydb2.cursor()

# Creación API
app = Flask(__name__)

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
        return render_template('inicio.html')
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

        cursor2.execute("""INSERT INTO `Usuarios`(`Nombre`,`Correo registro`, `Contraseña`)
                        VALUES ( %s, %s, %s )""", (nombre, correo, encriptado))
        mydb2.commit()

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

        cursor2.execute("""SELECT  `Correo registro` , `Contraseña`, `Nombre`
        FROM `Usuarios`
        WHERE `Correo registro` = %s """, [correo])

        mydb2.commit()

        usuario = cursor2.fetchone()

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
        cursor1.execute('Select * FROM componente')
        inventario = cursor1.fetchall()

        return render_template('index.html', mensaje=mensaje_error, fecha=fecha_hoy, inventario=inventario)
    else:
        return render_template('ingresar.html')


@app.route('/add_contact', methods=['POST'])
def add_contact():
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False
            pieza = request.form['pieza']
            tipo = request.form['tipos']
            coste = request.form['coste']
            lugar = request.form['lugar']

            cursor1.execute("""INSERT INTO `componente`(`nombre componente`, `tipo`, `coste`, `localización`)
             VALUES ( %s, %s, %s, %s )""", (pieza, tipo, coste, lugar))

            mydb1.commit()
            flash('Item añadido correctamente')
            return redirect(url_for('index'))
    else:
        return render_template('ingresar.html')


@app.route('/edit/componente=<string:id>')
def edit_contact(id):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        mensaje_error = False
        cursor1.execute('Select * FROM componente WHERE id = {0}'.format(id))
        datos = cursor1.fetchall()
        return render_template('edit.html', contact=datos[0])
    else:
        return render_template('ingresar.html')


@app.route('/update/componente=<string:id>', methods=['POST'])
def update_contact(id):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False
            pieza = request.form['pieza']
            tipo = request.form['tipos']
            coste = request.form['coste']
            lugar = request.form['lugar']

            cursor1.execute("""
                UPDATE `componente`
                SET `Nombre Componente` = %s,
                `tipo` = %s,
                `coste` = %s,
                `localización`= %s
                WHERE id = %s """, (pieza, tipo, coste, lugar, id))

            mydb1.commit()
            flash('Pieza actualizada correctamente')
            return redirect(url_for('index'))
    else:
        return render_template('ingresar.html')


@app.route('/delete/componente=<string:id>')
def delete_contact(id):
    login = comprobar_sesion()
    if login:
        cursor1.execute('DELETE FROM `componente` WHERE id = {0}'.format(id))
        mydb1.commit()
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

            cursor1.execute(""" SELECT *
            FROM `vigo`
            WHERE `{0}`= '{1}'""".format(opcion, valor))
            mydb1.commit()
            datos = cursor1.fetchall()

            cursor1.execute(""" SELECT SUM(`cantidad`) FROM `vigo` WHERE `{0}` = '{1}'""".format(opcion, valor))
            datoscuenta = cursor1.fetchall()

            page = request.args.get(get_page_parameter(), type=int, default=1)
            limit = 5
            offset = page * limit - limit

            total = len(datos)

            if total > 0:
                cursor1.execute("""Select *
                FROM `vigo`
                WHERE `{0}`= '{1}'ORDER BY `Fecha Modificación`
                DESC LIMIT {2} OFFSET {3}""".format(opcion, valor, limit, offset))

                valores = cursor1.fetchall()

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
