relaciones = {'componente':['maquina_herramienta','protocolos'],
              'actuacion': ['incidencias'],
              'incidencias': ['maquina_herramienta','protocolos','actuacion'],
              'maquina_herramienta': ['componente', 'incidencias', 'actuacion_preventivo'],
              'protocolos':['incidencias', 'componente'],
              'actuacion_preventivo':['maquina_herramienta']
              }
def relaciones1(vector):


def table_joints(vector_joins):
    if len(vector_joins) == 1:
        relaciones1(vector_joins)
    else:
        print('b')