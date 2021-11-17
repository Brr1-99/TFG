
def to_mysql(data):
    mysql_data = str(tuple(data)).replace("'", "`")
    return mysql_data
