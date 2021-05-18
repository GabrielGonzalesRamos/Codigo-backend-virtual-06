# Operadores de comparación 
# == es igual que  |  en python no existe el "==="
# != diferente 
# <, > menor que, mayor que 
# <=, >=, menor o igual  que, mayor o igual que
numero1, numero2 = 10, 20 
print(numero1 < numero2)
#if(persona < 18 && nacionalidad == 'colombiano'){...}

# Operadores Lógicos
# AND (en JS es &&) => sirve para validar que las dos condiciones sean VERDADERAS
# OR (en JS es ||) => sirve para validar que al menos una de las condiciones sea VERDADERA
# (codicion1 OR condicion2 OR condicion3){INGRESARÁ SI AL MENOS UNA ES VERDADERA}
# NOT (en JS es !) => invierte el resultado
print((10 > 5)and(10 > 11))
print((10 > 5)or(10 > 11))
print(not (10 > 5))

# Operadores de Identidad
# is => es
# is not => no es
# sirve para ver si estan apuntando a la misma direccion de memoria
frutas = ['MANZANA','PIÑA','FRESA','SANDIA']
frutas2 = frutas
print(frutas is frutas2)

# dos tipos de variables  => variables MUTABLES y las variables INMUTABLES
# mutables => es cuando nosotros hacemos una copia de esa variable, la copia tambien se esta alojando en el mismo espacio de memoria, son las conecciones de datos
# => listas, tuplas, diccionarios, conjuntos
# inmutables => es cuando hacemos una copia y se aloja en otra posicion de memoria
# => strings, int, boolean, etc

nombres = ['eduardo', 'raul','carlos','estefani']
nombres_alumnos = nombres
nombres_alumnos[0] = 'carmen'
nacionalidad = 'ecuatoriana'
nacionalidad2 = nacionalidad
nacionalidad2 = 'brazileña'

# Sirve para poder ubicar el identificador unico de esa variable en todo el compilador de python
# Para saber su posicion en hexadecimal tendriamos que convertirlo a ese valor
print(id(nombres))
print(id(nombres_alumnos))

print(id(nacionalidad))
print(id(nacionalidad2))

print(nombres)
print(nacionalidad2)
