from flask import render_template, Blueprint
from lib.list import get_list
from lib.comprobar_sesion import comprobar_sesion


listar = Blueprint('bp_listar', __name__, static_folder="static", template_folder="templates")
mensaje_error = False


@listar.route('/<string:db>/<string:table>/<string:id>')
def lista(db, table, id):
    """
    Se listan los valores relacionados entre varias tablas de una base de datos
    @db, @table y @id
    """
    login = comprobar_sesion()[0]
    if login:
        datos_db, pages, tabla = get_list(db, id)
        return render_template('listar.html', pagination=pages, mensaje=mensaje_error, datos=datos_db, base=db, table=tabla)
    else:
        return render_template('ingresar.html')
