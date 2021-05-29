CREATE DATABASE zapateria;
USE zapateria;
CREATE TABLE categorias(
  id integer primary key not null auto_increment,
  nombre varchar(50),
  abbr varchar(10),
  imagen text
);
CREATE TABLE productos(
  id integer primary key not null auto_increment,
  nombre varchar(50),
  precio decimal(5,2),
  ## n1 n2 n3 . n4 n5
  ## (n , m) 999.99
  ## Al final de cuentas un boolean es un tinyint en el cual 1 = TRUE y 0 FALSE
  disponible boolean,
  categoria_id int, # Repetir el valor de la categoria_id
  # contraint sirve para modificar el nombre con el cual se creará la relación de 
  # la tabla categoria y la tabla producto, el valor por defecto es :
  # categorias_productos_ibfk_n => n es el numero de creación de la contrainst
  # ibfk => innodb foreign key
  constraint relacion_producto_categoria foreign key (categoria_id) references categorias(id)
);

INSERT INTO categorias (nombre, abbr, imagen) VALUE
                                                ("ZAPATO","ZAP", "url1"),
                                                ("ZAPATILLA","ZAPT","url2"),
                        ("BOTIN","BOT","url3"),
                        ("BOTA","BOTA","url4");
                        
INSERT INTO productos (nombre, precio, disponible, categoria_id) VALUES
					  ("ZAPATO VERANO", 99.90, true, 1),
                      ("ZAPATO HOMBRE", 120.00, true, 1),
                      ("ZAPATO MUJER", 199.00, false, 1),
                      ("ZAPATILLA TREKKIN HOMBRE", 189.90, true, 2),
                      ("ZAPATILLA RUN MUJER", 220.00, true, 2),
                      ("ZAPATILLA OFFROAD MUJER", 320.89, true, 2),
                      ("BOTIN TACO 4", 520.00, true, 3),
                      ("BOTA TACO 10", 710, false, 4);                     


SELECT * FROM  categorias;


SELECT * FROM productos WHERE precio BETWEEN 100 AND 250;
SELECT * FROM productos WHERE nombre LIKE '%HOMBRE%';
SELECT * FROM productos WHERE nombre LIKE '%4%';
SELECT * FROM productos WHERE disponible IS true;
SELECT * FROM productos WHERE nombre LIKE '%ZAPATILLA%';
SELECT * FROM productos WHERE precio > 500 AND disponible IS false;
SELECT * FROM productos WHERE nombre LIKE '%ZAPATILLA%'  UNION  SELECT * FROM productos WHERE nombre LIKE '%BOTA%';

SELECT * FROM categorias;
SELECT * FROM productos;
INSERT INTO categorias (nombre, abbr, imagen) VALUE ("BEBES","BEB", "url5");
INSERT INTO productos (nombre, precio, disponible) VALUES ("SANDALIAS BOB TORONJA", 19.90, true);

#----------------------------
# SELECIONAME TODOS LOS NOMBRES CUYO ALIAS SERÁ NOMBRE DEL PRODUCTO, PRECIOS Y DISPONIBILIDAD DE 
# LA TABLA CATEGORIAS INTERSECCION CON LA TABLA PRODUCTOS CUANDO C.ID = P.CATEGORIA_ID NOMBRE  Y
# DONDE NOMBRE  SEA IGUAL A ZAPATO
SELECT c.nombre FROM categorias AS c INNER JOIN productos AS p ON c.id =  p.categoria_id
WHERE c.nombre = 'ZAPATO';
#----------------------------

## INNER JOIN ES LO MISMO QUE JOIN
SELECT * FROM categorias LEFT JOIN productos ON categorias.id =  productos.categoria_id;
SELECT * FROM categorias RIGHT JOIN productos ON categorias.id =  productos.categoria_id;

