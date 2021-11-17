from flask import Blueprint, render_template, session

iniciar = Blueprint('bp_inicio', __name__, static_folder="static", template_folder="templates")


@iniciar.route('/')
def inicio():
    login = comprobar_sesion()
    if login:
        return render_template('inicio.html')
    else:
        return render_template('ingresar.html')


def comprobar_sesion():
    validez = False
    nombre = session.get('Nombre registro')
    if nombre:
        validez = True
    return validez
