from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Integer
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class PostreModel(base_de_datos.Model): #Esta clase será una tabla
    postreId = Column(name='id', primary_key=True, autoincrement=True, unique=True, type_=types.Integer)
    postreNombre = Column(name='nombre')
