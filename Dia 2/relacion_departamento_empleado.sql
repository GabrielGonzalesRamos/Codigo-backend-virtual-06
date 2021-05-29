CREATE DATABASE IF NOT EXISTS EMPRESA;
USE EMPRESA;

CREATE TABLE departamentos(
id int auto_increment not null unique primary key,
nombre_departamento varchar(40),
numero_empleados int,
nivel int
);


CREATE TABLE empleados(
id int auto_increment not null unique primary key,
nombre varchar(40),
apellido varchar(40),
identificador int,
supervisor_id int,
departamentos_id int,
constraint relacion_departamento_empleado foreign key (departamentos_id) references departamentos(id),
constraint relacion_empleado_empleado foreign key (supervisor_id) references empleados(id)
);


INSERT INTO departamentos (nombre, piso)VALUES ('Ventas',1), ('Administracion',2), ('Finanzas',2), ('Marketing',3);