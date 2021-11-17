from config.mydb1 import db1, db2

cursor1 = db1()[1]
cursor2 = db2()[1]


def db_for_columns(db, table):
    col = []
    if db == 'inventario':
        cursor1.execute('Show Columns FROM {0}'.format(table))
        col = cursor1.fetchall()
    elif db == 'manten_correctivo':
        cursor2.execute('Show Columns FROM {0}'.format(table))
        col = cursor2.fetchall()
    return col
