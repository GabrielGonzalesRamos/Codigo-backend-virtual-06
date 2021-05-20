# una forma de almacenar varios valores en una misma variable
# LISTAS => coleccion de elementos ordenados
colores = ['azul','negro','amarillo','purpura']
misc = ['eduardo', 18, False, 14.5, '2015-04-14', ['1',2] ]
print(colores[1])
# imprimir la ultima posicion de la lista
print(colores[len(colores) - 1])

# imprimir desde la posicion 0 hasta las posicion 2
print(colores[0:2])
# imprimir desde la posicion 1 hasta la final
print(colores[1:])


# la forma de copiar el contenido y ya no utilizar la misma posicion de memoria para ambas variables es :
# en JS era colores2 = [ ...colores2  ]
# solo el contenido más no la posicion de memoria
colores2 = colores[:]
colores2[0]= "violeta"
print(colores2)
# colores2 = [ ...colores  ]

# solamente se puede usar las posiciones de una variable str(string) para leer mas, no para modifciar su contenido
# nombre[1] = "e"

# metodo para agregar un nuevo elemento a una lista
colores.append('indigo')
print(colores)

# metodo para eliminar un valor solamente si existe lo eliminará, sino indicará un error

colores.remove('indigo')
color_eliminado = colores.pop(0)
print(color_eliminado)


# TUPLAS => colección de elementos ordenada  NO SE PUEDE MODIFICAR LUEGO DE SU CREACIÓN

notas = (14,16,17,11,5,1,5,5,5)
print(notas[0])
print(notas[-1])
# print(notas[0]) = 20 NO SE PUEDE, DEBIDO A QUE ES UNA TUPLA
print(len(notas))

print(f'La cantidad de elementos de la tupla es {len(notas)}')

# ver si hay elementos repetidos dentro de una tupla 

print(notas.count(5))

# NO SE PUEDEN ELIMINAR LOS ELEMENTOS DENTRO DE LAS TUPLAS



# CONJUNTO => Es una coleccion de elementos DESORDENADA, osea que una vez que la creemos no  podremos revisar sus posiciones ya que se ordenadan aleatoriamente

estaciones = {"VERANO","OTOÑO","PRIMAVERA","INVIERNO"}
print(estaciones)
estaciones.add("OTOÑOVERANO")
print(estaciones)


# el metodo in sirve para validar si un valor esta dentro de una coleccion
print("OTOÑOINVIERNO" in estaciones)
# ESTO NO SE PUEDE HACER EN LOS CONJUNTOS print(estaciones[0])


# DICCIONARIO => Es una coleccion de elementos que estan INDEXADOS, que nosotros manejamos el nombre de su llave 

persona = {
        'id': 1,
        'nombre': 'Juancito',
        "relacion": "Soltero",
        "fecha_nacimiento": "1992/08/04",
        "hobbies": [
            {
                "nombre": "Futbol",
                "conocimiento": "Intercambio"
                },
            {
                "nombre": "Drones",
                "conocimiento": "Basico"
                }
            ]
        }

print(persona['hobbies'][0]["nombre"])
persona['apellido'] = 'Martinez'
print(persona)
# En python si la llave del diccionario no existe lanzará un error y hará que el programa no continue
id_eliminado = persona.pop('id')
print(id_eliminado)



libro = {
        "nombre": "Harry Potter",
        "autor": "J.K. Rowling",
        "editorial": "Editorial",
        "año": 2018,
        "idiomas": [
            {
                "nombre": "español"
                },
            {
                "nombre" : "ingles"
                },
            {
                "nombre" : "frances"
                },
            {
                "nombre" : "aleman"
                }
            ],
        "calificacion": 5,
        "imdb": "00asd12-asd878-a4s5d4a5-a45sd4a5sd",
        "tomos" : ("La piedra filosofal", "La camara secreta", "El vuelo del fenix")
        }


print(libro['autor'])
print(libro['tomos'][1])
print(len(libro['idiomas']))





