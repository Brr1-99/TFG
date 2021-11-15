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


@app.route('/index/<string:db>')
def index(db):
    login = comprobar_sesion()
    if login:
        global fecha_hoy
        datos_db, base, pages = db_for_index(db)
        return render_template('index.html', pagination=pages, mensaje=mensaje_error, fecha=fecha_hoy, datos=datos_db, base=base)
    else:
        return render_template('ingresar.html')


@app.route('/add/<string:db>/<string:table>')
def add(db, table):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        mensaje_error = False
        col = db_for_add(db, table)
        flash('Conexión con la tabla {0} realizada con éxito.'.format(table))
        return render_template('add.html', mensaje=mensaje_error, columns=col)
    else:
        return render_template('ingresar.html')


@app.route('/add', methods=['POST'])
def add_table():
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False

            last_url = str(request.referrer)
            table = last_url.split('/')[-1]
            db = last_url.split('/')[-2]

            cur, datab = db_cursor(db)
            col_name = []
            cur.execute('Show Columns FROM {0}'.format(table))
            columns = cur.fetchall()
            for column in columns[1:-1]:
                col_name.append(column[0])

            datas = []
            for i in range(len(col_name)):
                datas.append(request.form['col.{0}'.format(i+1)])

            names = to_mysql(col_name)

            cur.execute('INSERT INTO `{0}` {1} VALUES {2}'.format(table, names, tuple(datas)))
            datab.commit()
            flash('Pieza añadida a la tabla "{0}" correctamente'.format(table))

            return redirect(url_for('index', db=db))
    else:
        return render_template('ingresar.html')


@app.route('/edit/<string:db>/<string:table>/<string:id>')
def edit_contact(db, table, id):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        mensaje_error = False
        cur, datab = db_cursor(db)
        cur.execute('Select * FROM {0} WHERE id = {1}'.format(table, id))
        datos = cur.fetchall()
        flash('Por favor especifíque los nuevo valores')
        return render_template('edit.html', contact=datos[0])
    else:
        return render_template('ingresar.html')


@app.route('/update', methods=['POST'])
def update_contact():
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False

            last_url = str(request.referrer)
            id = last_url.split('/')[-1]
            table = last_url.split('/')[-2]
            db = last_url.split('/')[-3]

            cur, datab = db_cursor(db)
            col_name = []
            cur.execute('Show Columns FROM {0}'.format(table))
            columns = cur.fetchall()
            for column in columns[1:-1]:
                col_name.append(column[0])

            datas = []
            for i in range(len(col_name)):
                datas.append(request.form['contact.{0}'.format(i + 1)])

            text = extractCols(col_name)
            cur.execute("""
                UPDATE `{0}`
                SET {1}
                WHERE id = {2} """.format(table, text, id), datas)

            datab.commit()
            flash('Pieza actualizada correctamente')
            return redirect(url_for('index', db=db))
    else:
        return render_template('ingresar.html')


@app.route('/delete/<string:db>/<string:table>/<string:id>')
def delete_contact(db, table, id):
    login = comprobar_sesion()
    if login:
        cur, datab = db_cursor(db)
        cur.execute('DELETE FROM `{0}` WHERE id = {1}'.format(table, id))
        datab.commit()
        flash('Item de la tabla "{0}" eliminado correctamente'.format(table))
        return redirect(url_for('index', db=db))
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


def db_for_index(db):
    datos = []
    pages = []
    if db == 'inventario':

        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page * limit - limit

        cursor1.execute('Select * FROM componente ORDER BY `Fecha Modificación` DESC LIMIT %s OFFSET %s', (limit, offset))
        d1 = cursor1.fetchall()
        t1 = len(d1)

        cursor1.execute('Show Columns FROM componente')
        c1 = cursor1.fetchall()
        datos.append([d1, c1, 'componente'])

        cursor1.execute('Select * FROM maquina_herramienta ORDER BY `Fecha Modificación` DESC LIMIT %s OFFSET %s', (limit, offset))
        d2 = cursor1.fetchall()
        t2 = len(d2)

        cursor1.execute('Show Columns FROM maquina_herramienta')
        c2 = cursor1.fetchall()
        datos.append([d2, c2, 'maquina_herramienta'])

        pagination = Pagination(page=page, per_page=limit, total=t1, record_name='index')
        pagination2 = Pagination(page=page, per_page=limit, total=t2, record_name='index')
        pages.append(pagination)
        pages.append(pagination2)
    else:
        base = 2
    return datos, db, pages


def db_for_add(db, table):
    col = []
    if db == 'inventario':
        cursor1.execute('Show Columns FROM {0}'.format(table))
        col = cursor1.fetchall()
    return col


def db_cursor(db):
    cursor = cursor1
    mydb = mydb1
    if db == 'inventario':
        cursor = cursor1
        mydb = mydb1
    return cursor, mydb


def to_mysql(data):
    mysql_data = str(tuple(data)).replace("'", "`")
    return mysql_data


def extractCols(arr_cols):
    text = ''
    for col in arr_cols[:-1]:
        text += "`" + str(col) + "` = %s ,"
    text += "`" + str(arr_cols[-1]) + "` = %s "
    return text


if __name__ == '__main__':
    app.run(port=3000, debug=True)
