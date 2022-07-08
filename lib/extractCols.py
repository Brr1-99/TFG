
def extractCols(arr_cols: list[str]) -> str: 
    """
    Cambia el formato de texto de las columnas 
    para que no de errores al pasar las órdenes a MariaDB
    """
    text = ''
    for col in arr_cols[:-1]:
        text += "`" + str(col) + "` = %s ,"
    text += "`" + str(arr_cols[-1]) + "` = %s "
    return text
