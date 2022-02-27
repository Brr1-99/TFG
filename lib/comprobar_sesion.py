from flask import session


def comprobar_sesion():
    validez = False
    nombre = session.get('Nombre registro')
    id = session.get('id_user')
    if nombre:
        validez = True
    return validez, id
