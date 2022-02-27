from flask import Blueprint, render_template, flash, redirect, url_for
from lib.comprobar_sesion import comprobar_sesion
from lib.db_cursor import db_cursor
import os

delete = Blueprint('bp_eliminar', __name__, static_folder="static", template_folder="templates")


@delete.route('/<string:db>/<string:table>/<string:id>')
def delete_contact(db, table, id):
    login = comprobar_sesion()[0]
    if login:
        datab, cur = db_cursor(db)
        try:
            cur.execute('SELECT `imagen` FROM `{0}` WHERE id = {1}'.format(table, id))
            image = cur.fetchone()
            filename = image[0]
            os.remove('static/uploads/' + filename)
        except Exception as E:
            pass
        cur.execute('DELETE FROM `{0}` WHERE id = {1}'.format(table, id))
        datab.commit()
        flash('Item de la tabla "{0}" eliminado correctamente'.format(table))
        return redirect(url_for('bp_index.index', db=db))
    else:
        return render_template('ingresar.html')
