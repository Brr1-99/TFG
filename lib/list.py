from flask import request
from flask_paginate import Pagination, get_page_parameter
from lib.db_cursor import db_cursor
from config.mydb1 import db1


def get_list(db: str, id: int) -> tuple[list, Pagination, str]:
    """
    Obtiene los datos de las tablas entrelazadas para crearse luego una tabla en el html 
    """
    datos = []

    cursor_comp = db1()[1]
    cursor_comp.execute('Show Columns FROM componente')
    comp = cursor_comp.fetchall()

    cursor = db_cursor(db)[1]

    if db == 'inventario':
        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page * limit - limit

        cursor.execute(""" SELECT * FROM `componente_maquina` 
                        RIGHT JOIN `componente` ON componente_maquina.id_componente = componente.id 
                        WHERE `id_maquina` = {0} LIMIT {1} OFFSET {2} """.format(id, limit, offset))

        d1 = cursor.fetchall()
        t1 = len(d1)

        datos.append([d1, comp, id])

        pagination = Pagination(page=page, per_page=limit, total=t1, record_name='list')

        return datos, pagination, 'componente'
    else:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 5
        offset = page * limit - limit

        cursor.execute(""" SELECT * FROM `componente_protocolo` 
                                RIGHT JOIN `componente` ON componente_protocolo.id_componente = componente.id 
                                WHERE `id_protocolo` = {0} LIMIT {1} OFFSET {2} """.format(id, limit, offset))

        d1 = cursor.fetchall()
        t1 = len(d1)

        datos.append([d1, comp, id])
        pagination = Pagination(page=page, per_page=limit, total=t1, record_name='list')
        return datos, pagination, 'componente'
