from flask import Blueprint, render_template, flash, redirect, url_for
from lib.comprobar_sesión import comprobar_sesion
from lib.db_cursor import db_cursor

delete = Blueprint('bp_eliminar', __name__, static_folder="static", template_folder="templates")


@delete.route('/<string:db>/<string:table>/<string:id>')
def delete_contact(db, table, id):
    login = comprobar_sesion()
    if login:
        datab, cur = db_cursor(db)
        cur.execute('DELETE FROM `{0}` WHERE id = {1}'.format(table, id))
        datab.commit()
        flash('Item de la tabla "{0}" eliminado correctamente'.format(table))
        return redirect(url_for('index', db=db))
    else:
        return render_template('ingresar.html')
