from flask import Flask, render_template, session
from inicio.intro import iniciar
from adjuntar.add import adjuntar
from buscar.buscar import buscar
from administrar.admin import admin
from editar.editar import edit
from config.mydb1 import db1, db2, db3
from eliminar.eliminar import delete
from mostrar.mostrar import indx
from relacionar.join import joint
from listar.listar import listar
from subir.subir import uploads

# Conexión a todas las bases de datos

mydb1, cursor1 = db1()

mydb2, cursor2 = db2()

mydb3, cursor3 = db3()

# Creación API y conexión Blueprints
app = Flask(__name__)
app.register_blueprint(iniciar, url_prefix="/inicio")
app.register_blueprint(adjuntar, url_prefix="/add")
app.register_blueprint(buscar, url_prefix="/search")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(edit, url_prefix="/edit")
app.register_blueprint(delete, url_prefix="/delete")
app.register_blueprint(indx, url_prefix="/index")
app.register_blueprint(joint, url_prefix="/join")
app.register_blueprint(listar, url_prefix="/list")
app.register_blueprint(uploads, url_prefix="/upload")

# Ajustes
app.secret_key = "sE+gcUVWsU491sJ"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# Rutas Web
@app.route('/')
def main():
    return render_template('portada.html')


@app.route('/salir')
def salir():
    session.clear()
    return render_template('portada.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
