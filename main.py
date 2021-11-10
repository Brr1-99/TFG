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


class maquina_herramienta(db.Model):
    __bind_key__ = 'inventario'
    id = db.Column('id', db.Integer, primary_key=True)
    location = db.Column('Location', db.String(50), nullable=False)
    description = db.Column('Description', db.String(100), nullable=False)
    lista = db.relationship('Lista', backref='maquina_herramienta', uselist=False)

    def __init__(self, location, description):
        self.location = location
        self.description = description


Lista_Componentes = db.Table('Lista_Componentes', db.Column('id_list', db.Integer, db.ForeignKey('lista.id_list')), db.Column('id_component', db.Integer, db.ForeignKey('component.id_component')))


class Lista(db.Model):
    __bind_key__ = 'inventario'
    id_list = db.Column('id', db.Integer, primary_key=True)
    id_maquina = db.Column(db.Integer, db.ForeignKey('maquina_herramienta.id'))
    details = db.relationship('Componente', secondary=Lista_Componentes, backref=db.backref('details', lazy='dynamic'))

    def __init__(self, id_maquina):
        self.id_maquina = id_maquina


class Componente(db.Model):
    __bind_key__ = 'inventario'
    id_component = db.Column('id', db.Integer, primary_key=True)
    tipo = db.Column('Tipo', db.String(50), nullable=False)
    cost = db.Column('Coste', db.Integer, nullable=False)

    def __init__(self, tipo, cost):
        self.type = tipo
        self.cost = cost


# Rutas Web
@app.route('/')
def main():
    return render_template('portada.html')


if __name__ == '__main__':
    db.create_all(bind='inventario')
    app.run(port=3000, debug=True)
