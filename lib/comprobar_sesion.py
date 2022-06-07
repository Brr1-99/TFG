from flask import session


def comprobar_sesion():
    """
    Se comunica si la sesión está iniciada o no 
    """
    validez = False
    id = None
    nombre = session.get('Nombre registro')
    id = session.get('id_user')
    if nombre:
        validez = True
    return validez, id
