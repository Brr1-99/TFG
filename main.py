from _datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost'
app.config['SQLALCHEMY_BINDS'] = {
    'inventario': 'mysql://root@localhost/inventario',
    'mantenimiento': 'mysql://root@localhost/mantenimiento'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "sE+gcUVWsU491sJ"

db = SQLAlchemy(app)


class Maquina_Herramienta(db.Model):
    __bind_key__ = 'inventario'
    id = db.Column('id', db.Integer, primary_key=True)
    location = db.Column('Localización', db.String(50), nullable=False)
    description = db.Column('Descripción', db.String(100), nullable=False)

    def __init__(self, location, description):
        self.location = location
        self.description = description


# Rutas Web
@app.route('/')
def main():
    return render_template('portada.html')


if __name__ == '__main__':
    db.create_all(bind='inventario')
    app.run(port=3000, debug=True)
