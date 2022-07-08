from config.mydb1 import db1, db2, db3

cursor1 = db1()[1]
cursor2 = db2()[1]
cursor3 = db3()[1]


def db_for_columns(db: str, table: str) -> list[str]:
    """
    Devuelve los valores de las columnas de una determinada tabla
    """
    col = []
    if db == 'inventario':
        cursor1.execute('Show Columns FROM {0}'.format(table))
        col = cursor1.fetchall()
    elif db == 'manten_correctivo':
        cursor2.execute('Show Columns FROM {0}'.format(table))
        col = cursor2.fetchall()
    else:
        cursor3.execute('Show Columns FROM {0}'.format(table))
        col = cursor3.fetchall()
    return col
