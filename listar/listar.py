from flask import render_template, Blueprint
from lib.list import get_list
from lib.comprobar_sesión import comprobar_sesion


listar = Blueprint('bp_listar', __name__, static_folder="static", template_folder="templates_listar")
mensaje_error = False


@listar.route('/<string:db>/<string:table>/<string:id>')
def lista(db, table, id):
    login = comprobar_sesion()[0]
    if login:
        datos_db, pages = get_list(id)
        tabla = 'componente'
        return render_template('listar.html', pagination=pages, mensaje=mensaje_error, datos=datos_db, base=db, table=tabla)
    else:
        return render_template('ingresar.html')
