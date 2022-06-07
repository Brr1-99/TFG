from flask import Blueprint, render_template
from lib.comprobar_sesion import comprobar_sesion
from lib.cards import cards

iniciar = Blueprint('bp_inicio', __name__, static_folder="static", template_folder="templates")


@iniciar.route('/')
def inicio():
    """
    Comprueba el inicio de sesión
    Si no ha iniciado sesión, se le redirige a la página de ingreso
    En caso contrario, se le lleva a la página de inicio
    """
    login = comprobar_sesion()[0]
    if login:
        return render_template('inicio.html', cards=cards)
    else:
        return render_template('ingresar.html')

