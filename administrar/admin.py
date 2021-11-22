from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from lib.comprobar_sesión import comprobar_sesion
from config.mydb1 import db1, db2
import bcrypt

admin = Blueprint('bp_admin', __name__, static_folder="static", template_folder="templates_admin")

mydb1, cursor1 = db1()
mydb2, cursor2 = db2()

# Encriptamiento
semilla = bcrypt.gensalt()


@admin.route("/registrar", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        login = comprobar_sesion()[0]
        if login:
            return render_template('index.html')
        else:
            return render_template('registrar.html')
    else:
        nombre = request.form['Nombre registro']
        correo = request.form['Correo registro']
        password = request.form['Password registro']

        if request.form['Administrador'] == "on":
            rol = 'Administrador'
        else:
            rol = 'Jefe de planta'

        password_encode = password.encode("utf-8")
        encriptado = bcrypt.hashpw(password_encode, semilla)

        cursor2.execute('SELECT id from `roles` WHERE `Nombre rol` = "{0}"'.format(rol))
        id_rol = cursor2.fetchone()

        cursor2.execute("""INSERT INTO `Usuarios`(`Nombre`,`Correo registro`, `Contraseña`)
                        VALUES ( %s, %s, %s )""", (nombre, correo, encriptado))
        mydb2.commit()

        cursor2.execute('SELECT id FROM `usuarios` WHERE `Nombre` = "{0}"'.format(nombre))
        id_user = cursor2.fetchone()

        cursor2.execute("""INSERT INTO `rol-usuarios`(`id_rol`,`id_usuarios`)
                                VALUES ( %s, %s )""", (id_rol, id_user))
        mydb2.commit()

        session['Nombre registro'] = nombre
        session['Correo registro'] = correo

        flash("Se ha registrado correctamente. Por favor inicie sesión")

        return render_template('ingresar.html')


@admin.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if request.method == "GET":
        login = comprobar_sesion()[0]
        if login:
            return redirect(url_for('index'))
        else:
            return render_template('ingresar.html')
    else:
        correo = request.form['Correo login']
        password = request.form['Password login']
        password_encode = password.encode('utf-8')

        cursor2.execute("""SELECT  `Correo registro` , `Contraseña`, `Nombre`, `id`
        FROM `Usuarios`
        WHERE `Correo registro` = %s """, [correo])

        mydb2.commit()

        usuario = cursor2.fetchone()

        if usuario:
            encriptado = usuario[1]
            if encriptado == bcrypt.hashpw(password_encode, encriptado.encode('utf-8')).decode('utf-8'):
                session['Nombre registro'] = usuario[2]
                session['Correo registro'] = correo
                session['id_user'] = usuario[-1]
                flash(f"Bienvenido usuario: {usuario[2]}. Su id es : '{usuario[-1]}'.")
                return redirect(url_for('bp_inicio.inicio'))

            else:
                flash("La contraseña es incorrecta")

                return render_template('ingresar.html')

        else:
            flash("El correo no existe, por favor regístrese")

            return render_template('registrar.html')
