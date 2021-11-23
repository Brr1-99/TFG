from lib.db_for_columns import db_for_columns
result = 0


def insert_tables(join1, join2):
    global result
    col1 = db_for_columns(join1[0][0], join1[0][1])
    col2 = db_for_columns(join2[0][0], join2[0][1])
    for col_1 in col1:
        for col_2 in col2:
            if join2[0][1] == 'id_'+str(col_1):
                result = 2
                break
            elif 'id_'+str(col_2) == join1[0][1]:
                result = 1
                break
    print(result)
