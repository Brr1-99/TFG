from flask import request
from flask_paginate import Pagination, get_page_parameter
from config.mydb1 import db1


def get_list(id):
    datos = []

    cursor1 = db1()[1]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 5
    offset = page * limit - limit

    cursor1.execute(""" SELECT * FROM `componente_maquina` 
                    RIGHT JOIN `componente` ON componente_maquina.id_componente = componente.id 
                    WHERE `id_maquina` = {0} LIMIT {1} OFFSET {2} """.format(id, limit, offset))

    d1 = cursor1.fetchall()
    t1 = len(d1)

    cursor1.execute('Show Columns FROM componente')
    c1 = cursor1.fetchall()
    datos.append([d1, c1, f'Lista de Componentes de la Maquina de id : {id}'])

    pagination = Pagination(page=page, per_page=limit, total=t1, record_name='list')
    return datos, pagination
