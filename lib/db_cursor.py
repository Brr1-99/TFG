from config.mydb1 import db1, db2


def db_cursor(db):
    cursor = 0
    mydb = 0
    if db == 'inventario':
        mydb, cursor = db1()
    elif db == 'manten_correctivo':
        mydb, cursor = db2()
    return mydb, cursor
