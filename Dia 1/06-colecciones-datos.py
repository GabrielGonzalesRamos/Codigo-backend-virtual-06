# una forma de almacenar varios valores en una misma variable
# LISTAS
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
