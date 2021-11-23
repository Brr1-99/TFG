from flask import render_template, Blueprint, flash, redirect, url_for
from lib.comprobar_sesión import comprobar_sesion
from lib.table_for_joints import table_joints

joint = Blueprint('bp_join', __name__, static_folder="static", template_folder="templates_join")


@joint.route('/<string:db>/<string:table>/<string:id>')
def join(db, table, id):
    login = comprobar_sesion()[0]
    if login:
        message, join1 = table_joints(db, table, id)
        flash(f"{message} {join1}")
        return redirect(url_for('bp_index.index', db=db))
    else:
        return render_template('ingresar.html')
