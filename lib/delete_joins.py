from config.mydb1 import db1


def delete_joins(id_maquina, id_comp):
    """
    Se elimina la unión entre las tablas a través de los ids
    """
    db, cursor1 = db1()
    cursor1.execute("DELETE FROM `componente_maquina` WHERE `id_componente`= '{0}' AND `id_maquina` = '{1}'".format(id_comp, id_maquina))
    message = f'Relación eliminada entre la máquina {id_maquina} y la pieza con id {id_comp}'
    db.commit()
    cursor1.close()
    return message
