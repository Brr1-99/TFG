from flask import Blueprint, render_template
from lib.comprobar_sesión import comprobar_sesion

iniciar = Blueprint('bp_inicio', __name__, static_folder="static", template_folder="templates")


@iniciar.route('/')
def inicio():
    login = comprobar_sesion()
    if login:
        return render_template('inicio.html')
    else:
        return render_template('ingresar.html')

