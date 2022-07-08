from lib.insert_tables import insert_tables
relaciones = {'componente': ['maquina', 'protocolo'],
              'actuacion': ['incidencia', 'usuario'],
              'incidencia': ['maquina', 'protocolo', 'actuacion', 'usuario'],
              'maquina': ['componente', 'incidencia', 'actuacion_preventivo'],
              'protocolo': ['incidencia', 'componente'],
              'actuacion_preventivo': ['maquina', 'usuario']
              }

join1 = []
join2 = []
data1 = []
data2 = []
step = 1


def relaciones1(vector: list[str]) -> tuple[str, str]:
    message = 'Dirígete a una de las siguientes tablas para crear relación:'
    return message, relaciones[vector]


def relaciones2(vector: list[str]) -> tuple[str, list[str]]:
    global step
    vec = None
    message = 'No has elegido una tabla correcta.Prueba una de estas:'
    for i in join1:
        if i == vector:
            message = 'Relación creada con la tabla:'
            vec = vector
            break
    return message, vec


def table_joints(db: str, table: str, id: int) -> tuple[str, list[list[str]]]:
    """
    Se realiza la unión de dos tablas en 2 pasos
    En el primero se muestran las tablas a poder relacionar con la primera escogida
    En el segundo si se ha elegido una segunda tabla de forma correcta, se realiza la unón en la base de datos
    """
    global join1
    global step
    global join2
    if step == 1:
        mensaje1, join1 = relaciones1(table)
        data2.clear()
        data1.clear()
        join2 = []
        data1.append([db, table, id])
        print(data1)
        step = 2
        return mensaje1, join1
    else:
        mensaje2, join2 = relaciones2(table)
        if join2:
            data2.append([db, table, id])
            insert_tables(data1, data2)
            step = 1
            join1 = []
            return mensaje2, join2
        else:
            step = 2
            return mensaje2, join1
