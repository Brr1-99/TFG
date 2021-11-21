
def table_for_joints(db, table):
    tables = []
    row_pairs = []
    table_mid = []
    if db == 'inventario':
        if table == 'componente':
            tables.append([db, 'maquina_herramienta'])
            row_pairs.append(['id', 'id'])
            table_mid.append('componente_maquina')
    return tables, row_pairs, table_mid
