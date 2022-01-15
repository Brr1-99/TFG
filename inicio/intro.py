from flask import Blueprint, render_template
from lib.comprobar_sesión import comprobar_sesion
from lib.cards import cards

iniciar = Blueprint('bp_inicio', __name__, static_folder="static", template_folder="templates_intro")


@iniciar.route('/')
def inicio():
    login = comprobar_sesion()[0]
    if login:
        return render_template('inicio.html', cards=cards)
    else:
        return render_template('ingresar.html')

