
def extractCols(arr_cols):
    text = ''
    for col in arr_cols[:-1]:
        text += "`" + str(col) + "` = %s ,"
    text += "`" + str(arr_cols[-1]) + "` = %s "
    return text
