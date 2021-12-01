from flask import request
from flask_paginate import Pagination, get_page_parameter
from config.mydb1 import db1, db2, db3


def db_for_index(db):
    datos = []
    pages = []
    tables = []
    if db == 'inventario':

        cursor1 = db1()[1]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page * limit - limit

        cursor1.execute('Select * FROM componente ORDER BY `Fecha Modificación` DESC LIMIT %s OFFSET %s', (limit, offset))
        d1 = cursor1.fetchall()
        t1 = len(d1)

        cursor1.execute('Show Columns FROM componente')
        c1 = cursor1.fetchall()
        datos.append([d1, c1, 'componente'])

        cursor1.execute('Select * FROM maquina ORDER BY `Fecha Modificación` DESC LIMIT %s OFFSET %s', (limit, offset))
        d2 = cursor1.fetchall()
        t2 = len(d2)

        cursor1.execute('Show Columns FROM maquina')
        c2 = cursor1.fetchall()
        datos.append([d2, c2, 'maquina'])

        pagination = Pagination(page=page, per_page=limit, total=t1, record_name='index')
        pagination2 = Pagination(page=page, per_page=limit, total=t2, record_name='index')
        pages.append(pagination)
        pages.append(pagination2)

        cursor1.execute("""SELECT TABLE_NAME from information_schema.tables where table_schema = '{0}'""".format(db))
        ctable = list(cursor1.fetchall())
        for table in ctable:
            tables.append(table[0])
        tables.remove('componente_maquina')
        cursor1.close()

    elif db == 'manten_correctivo':

        cursor2 = db2()[1]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page * limit - limit

        cursor2.execute('Select * FROM actuacion ORDER BY `id` DESC LIMIT %s OFFSET %s', (limit, offset))
        d1 = cursor2.fetchall()
        t1 = len(d1)

        cursor2.execute('Show Columns FROM actuacion')
        c1 = cursor2.fetchall()
        datos.append([d1, c1, 'actuacion'])

        cursor2.execute('Select * FROM incidencia ORDER BY `id` DESC LIMIT %s OFFSET %s', (limit, offset))
        d2 = cursor2.fetchall()
        t2 = len(d2)

        cursor2.execute('Show Columns FROM incidencia')
        c2 = cursor2.fetchall()
        datos.append([d2, c2, 'incidencia'])

        pagination = Pagination(page=page, per_page=limit, total=t1, record_name='index')
        pagination2 = Pagination(page=page, per_page=limit, total=t2, record_name='index')
        pages.append(pagination)
        pages.append(pagination2)

        cursor2.execute("""SELECT TABLE_NAME from information_schema.tables where table_schema = '{0}'""".format(db))
        ctable = list(cursor2.fetchall())
        for table in ctable:
            tables.append(table[0])

        cursor2.close()
    else:

        cursor3 = db3()[1]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page * limit - limit

        cursor3.execute('Select * FROM actuacion_preventiva ORDER BY `id` DESC LIMIT %s OFFSET %s', (limit, offset))
        d1 = cursor3.fetchall()
        t1 = len(d1)

        cursor3.execute('Show Columns FROM actuacion_preventiva')
        c1 = cursor3.fetchall()
        datos.append([d1, c1, 'incidencia'])

        pagination = Pagination(page=page, per_page=limit, total=t1, record_name='index')
        pages.append(pagination)

        cursor3.execute("""SELECT TABLE_NAME from information_schema.tables where table_schema = '{0}'""".format(db))
        ctable = list(cursor3.fetchall())
        for table in ctable:
            tables.append(table[0])

        cursor3.close()

    return datos, db, pages, tables
