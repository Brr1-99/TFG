from flask import render_template, Blueprint, request, flash, redirect, url_for
from lib.comprobar_sesión import comprobar_sesion
from lib.table_for_joints import table_joints

joint = Blueprint('bp_join', __name__, static_folder="static", template_folder="templates_join")
val_join = []


@joint.route('/<string:db>/<string:table>/<string:id>', methods=['GET'])
def join(db, table, id):
    login = comprobar_sesion()
    if login:
        if request.method == 'GET':
            val_join.append([db, table, id])
            if len(val_join) > 1:
                message = table_joints(val_join)
                flash(f"{message}")
                return redirect(url_for('bp_index.index', db=db))
            else:
                flash('Seleccione el valor con el que desea relacionarlo.')
                return redirect(url_for('bp_index.index', db=db))
    else:
        return render_template('ingresar.html')
