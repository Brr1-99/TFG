from lib.db_for_columns import db_for_columns
from lib.db_cursor import db_cursor
from lib.to_mysql import to_mysql
result = 0


def mysql(option, data1, data2, columna):
    """
    Se crean los nuevos valores en la tabla de unión
    """
    if option == 0:
        name = [data1[0][1], data2[0][1]]
        name.sort()
        table = str(name[0]) + '_' + str(name[1])
        col = db_for_columns(data1[0][0], table)
        mydb, cursor = db_cursor(data1[0][0])

        col_name = []
        for column in col:
            col_name.append(column[0])

        names = to_mysql(col_name)
        datas = []
        if name[0] == data1[0][1]:
            datas = [data1[0][2], data2[0][2]]
        else:
            datas = [data2[0][2], data1[0][2]]
        cursor.execute('INSERT INTO `{0}` {1} VALUES {2}'.format(table, names, tuple(datas)))
        mydb.commit()

    elif option == 1:

        mydb, cursor = db_cursor(data1[0][0])
        table = data1[0][1]
        name = columna
        datas = data2[0][2]
        id_ppal_table = data1[0][2]
        cursor.execute('UPDATE `{0}` SET `{1}`= {2} WHERE `id` = {3}'.format(table, name[0], datas, id_ppal_table))
        mydb.commit()

    else:

        mydb, cursor = db_cursor(data2[0][0])
        table = data2[0][1]
        name = columna
        datas = data1[0][2]
        id_ppal_table = data2[0][2]
        cursor.execute('UPDATE `{0}` SET `{1}`= {2} WHERE `id` = {3}'.format(table, name[0], datas, id_ppal_table))
        mydb.commit()


def insert_tables(join1, join2):
    """
    Se comprueba el orden en el que se mandaron las dos columnas a unir para evitar errores
    """
    global result
    col = []
    col1 = db_for_columns(join1[0][0], join1[0][1])
    col2 = db_for_columns(join2[0][0], join2[0][1])
    for col_1 in col1:
        for col_2 in col2:
            if 'id_'+str(join2[0][1]) == col_1[0]:
                result = 1
                col.append(col_1[0])
                break
            elif col_2[0] == 'id_'+str(join1[0][1]):
                result = 2
                col.append(col_2[0])
                break
    mysql(result, join1, join2, col)
