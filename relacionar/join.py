from flask import render_template, Blueprint, request
from lib.db_cursor import db_cursor
from lib.comprobar_sesión import comprobar_sesion
from lib.table_for_joints import table_for_joints

joint = Blueprint('bp_join', __name__, static_folder="static", template_folder="templates_join")
mensaje_error = False


@joint.route('/<string:db>/<string:table>/<string:id>', methods=['GET', 'POST'])
def join(db, table, id):
    login = comprobar_sesion()
    if login:
        if request.method == 'GET':

            datab, cur = db_cursor(db)
            tables, rows, table_mid = table_for_joints(db, table)

            return render_template('join.html', tables_join=tables)
    else:
        return render_template('ingresar.html')
