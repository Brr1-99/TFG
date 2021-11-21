
def table_for_joints(db):
    tables = []
    row_pairs = []
    table_mid = []
    if db == 'inventario':
        tables.append(['componente', 'maquina_herramienta'])
        row_pairs.append(['id', 'id'])
        table_mid.append('componente_maquina')
    return tables, row_pairs, table_mid
