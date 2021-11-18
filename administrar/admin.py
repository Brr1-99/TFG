from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from lib.comprobar_sesión import comprobar_sesion
from config.mydb1 import db1, db2
import bcrypt

admin = Blueprint('bp_admin', __name__, static_folder="static", template_folder="templates")

mydb1, cursor1 = db1()
mydb2, cursor2 = db2()

# Encriptamiento
semilla = bcrypt.gensalt()


@admin.route("/registrar", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        login = comprobar_sesion()
        if login:
            return render_template('index.html')
        else:
            return render_template('registrar.html')
    else:
        nombre = request.form['Nombre registro']
        correo = request.form['Correo registro']
        password = request.form['Password registro']
        password_encode = password.encode("utf-8")
        encriptado = bcrypt.hashpw(password_encode, semilla)

        cursor2.execute("""INSERT INTO `Usuarios`(`Nombre`,`Correo registro`, `Contraseña`)
                        VALUES ( %s, %s, %s )""", (nombre, correo, encriptado))
        mydb2.commit()

        session['Nombre registro'] = nombre
        session['Correo registro'] = correo

        flash("Se ha registrado correctamente. Por favor inicie sesión")

        return render_template('ingresar.html')


@admin.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if request.method == "GET":
        login = comprobar_sesion()
        if login:
            return redirect(url_for('index'))
        else:
            return render_template('ingresar.html')
    else:
        correo = request.form['Correo login']
        password = request.form['Password login']
        password_encode = password.encode('utf-8')

        cursor2.execute("""SELECT  `Correo registro` , `Contraseña`, `Nombre`
        FROM `Usuarios`
        WHERE `Correo registro` = %s """, [correo])

        mydb2.commit()

        usuario = cursor2.fetchone()

        if usuario:
            encriptado = usuario[1]
            if encriptado == bcrypt.hashpw(password_encode, encriptado.encode('utf-8')).decode('utf-8'):
                session['Nombre registro'] = usuario[2]
                session['Correo registro'] = correo

                return redirect(url_for('bp_inicio.inicio'))

            else:
                flash("La contraseña es incorrecta")

                return render_template('ingresar.html')

        else:
            flash("El correo no existe, por favor regístrese")

            return render_template('registrar.html')
