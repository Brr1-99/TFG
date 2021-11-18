from flask import Flask, render_template, redirect, url_for, flash, session

from inicio.intro import iniciar
from adjuntar.add import adjuntar
from buscar.buscar import buscar
from administrar.admin import admin
from editar.editar import edit
from config.mydb1 import db1, db2
from lib.db_for_index import db_for_index
from lib.db_cursor import db_cursor

# Conexión a todas las bases de datos

mydb1, cursor1 = db1()

mydb2, cursor2 = db2()

# Creación API y conexión Blueprints
app = Flask(__name__)
app.register_blueprint(iniciar, url_prefix="/inicio")
app.register_blueprint(adjuntar, url_prefix="/add")
app.register_blueprint(buscar, url_prefix="/search")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(edit, url_prefix="/edit")

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


@app.route('/delete/<string:db>/<string:table>/<string:id>')
def delete_contact(db, table, id):
    login = comprobar_sesion()
    if login:
        datab,cur = db_cursor(db)
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


if __name__ == '__main__':
    app.run(port=3000, debug=True)
