from sqlalchemy.sql.sqltypes import String
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class IngredienteModel(base_de_datos.Model):
    __tablename__ = "ingredientes"

    ingredienteId = Column(name='id', primary_key=True,autoincrement=True, unique=True, type_=types.Integer, nullable=False)
    ingredienteNombre = Column(name='nombre', type_=String(length=45), unique=True)

    def __init__(self, nombre):
        self.ingredienteNombre = nombre


