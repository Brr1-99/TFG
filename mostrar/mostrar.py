from flask import render_template, Blueprint
from lib.db_for_index import db_for_index
from lib.comprobar_sesion import comprobar_sesion
from lib.table_for_joints import relaciones

indx = Blueprint('bp_index', __name__, static_folder="static", template_folder="templates")
mensaje_error = False


@indx.route('/<string:db>')
def index(db):
    """
    Se buscan  los últimos datos modificados de la base de datos y se pasan a la vista 'index.html'
    """
    login = comprobar_sesion()[0]
    if login:
        datos_db, base, pages, tables_db = db_for_index(db)
        return render_template('index.html', pagination=pages, mensaje=mensaje_error, datos=datos_db, base=base, tables=tables_db, relate=relaciones)
    else:
        return render_template('ingresar.html')
