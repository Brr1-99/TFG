from flask import render_template, Blueprint, request
from lib.db_cursor import db_cursor
from lib.comprobar_sesión import comprobar_sesion
from lib.table_for_joints import table_for_joints

joint = Blueprint('bp_join', __name__, static_folder="static", template_folder="templates_join")
mensaje_error = False


@joint.route('/<string:db>/', methods=['GET', 'POST'])
def join(db):
    login = comprobar_sesion()
    if login:
        if request.method == 'GET':
            datab, cur = db_cursor(db)
            tables, row, table_mid = table_for_joints(db)
            if len(tables) > 1:
                return render_template('join.html', tables_join=tables)
            else:
                cur.execute()
                return render_template('join.html', tables_join=tables)
    else:
        return render_template('ingresar.html')
