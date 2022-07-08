from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_paginate import Pagination, get_page_parameter
from lib.comprobar_sesion import comprobar_sesion
from lib.db_cursor import db_cursor
from lib.db_for_columns import db_for_columns
from lib.db_for_index import db_for_index
from lib.table_for_joints import relaciones

buscar = Blueprint('bp_busqueda', __name__, static_folder="static", template_folder="templates")

mensaje_error = False


@buscar.route('', methods=['GET', 'POST'])
def search():
    """
    Se obtiene la última url para recoger los datos más recientes de la tabla
    Así se tiene ya una primera vista de la magnitud de los datos
    """
    global mensaje_error
    login = comprobar_sesion()[0]
    if login:
        if request.method == 'POST':
            mensaje_error = False

            table_index = str(request.form['buscar'])[-1]
            last_url = str(request.referrer)
            db = last_url.split('/')[-1]
            tables_db = db_for_index(db)[-1]

            table = tables_db[int(table_index)]

            return redirect(url_for('bp_busqueda.search_data', db=db, table=table))
        else:
            flash('Seleccione una tabla para poder iniciar la búsqueda')
            return redirect(url_for('bp_inicio.inicio'))
    else:
        return render_template('ingresar.html')


@buscar.route('/<string:db>/<string:table>', methods=["GET", "POST"])
def search_data(db: str, table: str) -> any:
    """
    Se utiliza la url para pillar las columnas de la tabla a buscar
    Se muestran los campos de búsqueda posibles a partir de las columnas
    Si el método no es 'GET' se buscan los posibles valores dados los criterios del formulario
    Si hay datos se muestran en una tabla construida dinámicamente
    De lo contrario se muestra un mensaje de error 
    """
    global mensaje_error
    login = comprobar_sesion()
    if login:
        if request.method == 'GET':
            mensaje_error = False
            current_url = str(request.url)
            datab, cur = db_cursor(db)
            col = db_for_columns(db, table)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            limit = 5
            offset = page * limit - limit

            cur.execute('SELECT * FROM {0} ORDER BY `Fecha Modificación` DESC LIMIT {1} OFFSET {2}'.format(table, limit, offset))
            datab.commit()
            data = cur.fetchall()
            length = len(data)

            pagination = Pagination(page=page, per_page=limit, total=length, record_name='search')

            return render_template('search.html', pagination=pagination, busqueda=data, url=current_url, columns=col, db=db, table=table, mensaje=mensaje_error, relate=relaciones)
        else:
            mensaje_error = True
            current_url = str(request.url)
            criterio = request.form['criterio']
            nombre = request.form['nombre']
            datab, cur = db_cursor(db)
            col = db_for_columns(db, table)

            page = request.args.get(get_page_parameter(), type=int, default=1)
            limit = 5
            offset = page * limit - limit

            cur.execute('SELECT * FROM {0}'.format(table))
            data = cur.fetchall()
            length = len(data)

            if length > 0:

                cur.execute("""SELECT * FROM {0} WHERE `{1}` LIKE '%{2}%' ORDER BY `Fecha Modificación` DESC LIMIT {3} OFFSET {4}""".format(table, criterio, nombre, limit, offset))
                datab.commit()
                data = cur.fetchall()

                pagination = Pagination(page=page, per_page=limit, total=length, record_name='search')

                return render_template('search.html', pagination=pagination, busqueda=data, url=current_url, columns=col, db=db, table=table, mensaje=mensaje_error, relate=relaciones)
            else:
                return redirect(url_for('bp_busqueda.search_data', db=db, table=table, mensaje=mensaje_error))
    else:
        return render_template('ingresar.html')
