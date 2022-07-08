from flask import render_template, Blueprint, flash, redirect, url_for, request
from lib.comprobar_sesion import comprobar_sesion
from lib.table_for_joints import table_joints
from lib.delete_joins import delete_joins

joint = Blueprint('bp_join', __name__, static_folder="static", template_folder="templates_join")


@joint.route('/<string:db>/<string:table>/<string:id>/<int:option>')
def join(db: str, table: str, id: int, option: int) -> any:
    """
    Dependiendo de la opción escogida se pueden unir valores de tablas diferentes 
    o eliminar uniones ya creadas
    """
    login = comprobar_sesion()[0]
    if login:
        if option == 0:
            message, join1 = table_joints(db, table, id)
            flash(f"{message} {join1}")
            return redirect(url_for('bp_index.index', db=db))
        else:
            last_id = request.referrer.split('/')[-1]
            message_disjoin = delete_joins(last_id, id)
            flash(f"{message_disjoin}")
            return redirect(url_for('bp_index.index', db=db))
    else:
        return render_template('ingresar.html')
