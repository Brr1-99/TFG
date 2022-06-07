from config.mydb1 import db1, db2, db3

def db_cursor(db):
    """
    Devuelve la conexión a la base de datos y su correspondiente cursor
    Así se pueden realizar las operaciones 
    """
    if db == 'inventario':
        mydb, cursor = db1()
    elif db == 'manten_correctivo':
        mydb, cursor = db2()
    else:
        mydb, cursor = db3()
    return mydb, cursor
