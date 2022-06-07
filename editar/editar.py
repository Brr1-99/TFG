from flask import Blueprint, render_template, flash, request, redirect, url_for
from lib.comprobar_sesion import comprobar_sesion
from lib.extractCols import extractCols
from lib.db_cursor import db_cursor

edit = Blueprint('bp_editar', __name__, static_folder="static", template_folder="templates")

mensaje_error = False


@edit.route('/<string:db>/<string:table>/<string:id>')
def edit_contact(db, table, id):
    """
    Se buscan los valores a través de los parámetros de la url @db, @table y @id
    Se envían para ser mostrados y que el usuario los cambie
    """
    global mensaje_error
    login = comprobar_sesion()[0]
    if login:
        mensaje_error = False
        datab, cur = db_cursor(db)
        cur.execute('Select * FROM {0} WHERE id = {1}'.format(table, id))
        datos = cur.fetchall()

        cur.execute('Show Columns FROM {0}'.format(table))
        columns = cur.fetchall()

        flash('Por favor especifíque los nuevo valores')

        return render_template('edit.html', contact=datos[0], col=columns, indice=id, tabla=table)
    else:
        return render_template('ingresar.html')


@edit.route('', methods=['GET', 'POST'])
def update_contact():
    """
    Se recogen los nuevos datos del formulario de la plantilla en la vista 'edit.html'
    Se actualizan en la base de datos correspondiente
    """
    global mensaje_error
    login = comprobar_sesion()[0]
    if login:
        if request.method == 'POST':
            mensaje_error = False

            last_url = str(request.referrer)
            index = last_url.split('/')[-1]
            table = last_url.split('/')[-2]
            db = last_url.split('/')[-3]

            datab, cur = db_cursor(db)
            col_name = []
            cur.execute('Show Columns FROM {0}'.format(table))
            columns = cur.fetchall()
            for column in columns[1:-1]:
                col_name.append(column[0])

            data = []
            for i in range(len(col_name)):
                data.append(request.form['contact.{0}'.format(i + 1)])

            cols = extractCols(col_name)
            try:
                cur.execute("""
                    UPDATE `{0}`
                    SET {1}
                    WHERE id = {2} """.format(table, cols, index), data)

                datab.commit()
                flash('Pieza actualizada correctamente.')
            except BaseException as error:
                flash(f'Se ha producido un error al actualizar los valores: {error}.')
            return redirect(url_for('bp_index.index', db=db))
        else:
            flash('Selecciona un ítem a editar para acceder a la página que buscas.')
            return redirect(url_for('bp_inicio.inicio'))
    else:
        return render_template('ingresar.html')
