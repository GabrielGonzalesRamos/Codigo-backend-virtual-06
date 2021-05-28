-- ESTO ES UN COMENTARIO
-- SQL ES UN LENGUAJE DE SENTENCIAS ESTRUCTURADO
CREATE DATABASE pruebas;
USE pruebas;
CREATE TABLE alumnos(
# ACA AHORA VENDRA TODAS LAS COLUMNAS DE ESA TABLA DE ALUMNOS
# SOLO PUEDE EXISTIR UNA COLUMNA AUTO INCREMENTABLE POR TABLA
  id integer primary key not null auto_increment,
  nombre varchar(40),
  apellido varchar(25),
  sexo varchar(10),
  numero_emergencia int,
  religion varchar(10),
  fecha_nacimiento date
);

# PARA INGRESAR LOS DATOS A UNA TABLA ES :
INSERT INTO alumnos( nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento) VALUES ("Eduardo","De Rivero","M","987654321","CATOLICO","1990-08-14");
INSERT INTO alumnos( nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento) VALUES ("Fiorella","Cclla","F","900000000","ATEO","1993-01-07");
INSERT INTO alumnos( nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento) VALUES ("Matheus","Peña","M","911111111","EVANGELICO","1989-04-06");
INSERT INTO alumnos( nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento) VALUES ("Aldo","Cortina Lozano","M","922222222","CATOLICO","1990-08-14");
SELECT * FROM alumnos;
SELECT * FROM alumnos WHERE nombre = "Eduardo" and sexo = "M";
DELETE FROM alumnos WHERE nombre = "Eduardo";





CREATE TABLE habilidades(
id int auto_increment not null unique primary key,
# primary key es un identificador unico sirve para la indexación
# Solo puede haber un auto_increment por tabla !!!
descripcion varchar(100) not null,
nivel varchar(15),
alumno_id int not null
);

CREATE TABLE habilidades_alumnos(
id int auto_increment not null unique primary key,
alumno_id int not null,
habilidad_id int not null,
# Las llaves foreneas son la representación de la tabla en la se está haciendo la realción 
foreign key(habilidad_id) references habilidades(id),
foreign key(alumno_id) references alumnos(id)
);

SELECT * FROM alumnos;

# 

