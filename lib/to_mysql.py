
def to_mysql(data: list[str]) -> str:
    mysql_data = str(tuple(data)).replace("'", "`")
    return mysql_data
