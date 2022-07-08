import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

"""
Se guarda la información relacionada al servidor
en un archivo oculto
"""
host = os.getenv("host") or ""
user = os.getenv("user") or ""
password = os.getenv("password") or ""


def db1() -> tuple[MySQLdb.connect, MySQLdb.connections.cursor]:
    """
    Se crea la conexion a la base de datos y su cursor 
    para poder realizar acciones sobre ella
    """
    mydb1 = MySQLdb.connect(host='localhost',
                            user='root',
                            password='',
                            db='inventario')

    cursor1 = mydb1.cursor()
    return mydb1, cursor1


def db2() -> tuple[MySQLdb.connect, MySQLdb.connections.cursor]:
    mydb2 = MySQLdb.connect(host='localhost',
                            user='root',
                            password='',
                            db='manten_correctivo')

    cursor2 = mydb2.cursor()
    return mydb2, cursor2


def db3() -> tuple[MySQLdb.connect, MySQLdb.connections.cursor]:
    mydb3 = MySQLdb.connect(host='localhost',
                            user='root',
                            password='',
                            db='manten_preventivo')

    cursor3 = mydb3.cursor()
    return mydb3, cursor3
