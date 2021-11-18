from flask import Blueprint, render_template, flash, request, redirect, url_for
from lib.comprobar_sesión import comprobar_sesion
from lib.to_mysql import to_mysql
from lib.db_for_columns import db_for_columns
from lib.db_cursor import db_cursor

adjuntar = Blueprint('bp_añadir', __name__, static_folder="static", template_folder="templates_add")

mensaje_error = False


@adjuntar.route('/<string:db>/<string:table>')
def add(db, table):
    global mensaje_error
    login = comprobar_sesion()
    if login:
        mensaje_error = False
        col = db_for_columns(db, table)
        flash('Conexión con la tabla {0} realizada con éxito.'.format(table))
        return render_template('add.html', mensaje=mensaje_error, columns=col)
    else:
        return render_template('ingresar.html')


@adjuntar.route('', methods=['GET', 'POST'])
def add_table():
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'POST':
            mensaje_error = False

            last_url = str(request.referrer)
            table = last_url.split('/')[-1]
            db = last_url.split('/')[-2]

            datab, cur = db_cursor(db)
            col_name = []
            cur.execute('Show Columns FROM {0}'.format(table))
            columns = cur.fetchall()
            for column in columns[1:-1]:
                col_name.append(column[0])

            datas = []
            for i in range(len(col_name)):
                datas.append(request.form['col.{0}'.format(i+1)])

            names = to_mysql(col_name)

            cur.execute('INSERT INTO `{0}` {1} VALUES {2}'.format(table, names, tuple(datas)))
            datab.commit()
            flash('Pieza añadida a la tabla "{0}" correctamente'.format(table))

            return redirect(url_for('bp_index.index', db=db))
        else:
            flash('Selecciona el botón de añadir en una tabla para acceder a la página que buscas.')
            return redirect(url_for('bp_inicio.inicio'))
    else:
        return render_template('ingresar.html')