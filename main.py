from flask import Flask, render_template, request, redirect, url_for, flash, session
from inicio.intro import iniciar
from adjuntar.add import adjuntar
from buscar.buscar import buscar
from administrar.admin import admin
from config.mydb1 import db1, db2
from lib.db_for_index import db_for_index

# Conexión a todas las bases de datos
mydb1, cursor1 = db1()

mydb2, cursor2 = db2()

# Creación API y conexión Blueprints
app = Flask(__name__)
app.register_blueprint(iniciar, url_prefix="/inicio")
app.register_blueprint(adjuntar, url_prefix="/add")
app.register_blueprint(buscar, url_prefix="/search")
app.register_blueprint(admin)

# Ajustes
app.secret_key = "sE+gcUVWsU491sJ"


# Variable global
mensaje_error = False


# Rutas Web
@app.route('/')
def main():
    return render_template('portada.html')


@app.route('/salir')
def salir():
    session.clear()
    return render_template('portada.html')


@app.route('/index/<string:db>')
def index(db):
    login = comprobar_sesion()
    if login:
        datos_db, base, pages, tables_db = db_for_index(db)
        return render_template('index.html', pagination=pages, mensaje=mensaje_error, datos=datos_db, base=base, tables=tables_db)
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


@app.route('/edit', methods=['GET', 'POST'])
def update_contact():
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False

            last_url = str(request.referrer)
            indice = last_url.split('/')[-1]
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
                WHERE id = {2} """.format(table, text, indice), datas)

            datab.commit()
            flash('Pieza actualizada correctamente.')
            return redirect(url_for('index', db=db))
        else:
            flash('Selecciona un ítem a editar para acceder a la página que buscas.')
            return redirect(url_for('bp_inicio.inicio'))
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


# Funciones Recurrentes
def comprobar_sesion():
    validez = False
    nombre = session.get('Nombre registro')
    if nombre:
        validez = True
    return validez


def extractCols(arr_cols):
    text = ''
    for col in arr_cols[:-1]:
        text += "`" + str(col) + "` = %s ,"
    text += "`" + str(arr_cols[-1]) + "` = %s "
    return text


if __name__ == '__main__':
    app.run(port=3000, debug=True)
