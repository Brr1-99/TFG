import MySQLdb


def db1():
    mydb1 = MySQLdb.connect(host='localhost',
                            user='root',
                            password='',
                            db='inventario')

    cursor1 = mydb1.cursor()
    return mydb1, cursor1


def db2():
    mydb2 = MySQLdb.connect(host='localhost',
                            user='root',
                            password='',
                            db='manten_correctivo')

    cursor2 = mydb2.cursor()
    return mydb2, cursor2


def db3():
    mydb3 = MySQLdb.connect(host='localhost',
                            user='root',
                            password='',
                            db='manten_preventivo')

    cursor3 = mydb3.cursor()
    return mydb3, cursor3
