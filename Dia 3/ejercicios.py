

def MakeRectangle():

    h = int(input('Ingrese la altura del cuadrado : ')) 
    b = int(input('Ingrese la base del cuadrado : ')) 
    for j in range(h):
        for i in range(b):
          print('*', end='')
        print(" ")  


def MakeTriangle():
    h = int(input('Ingrese la altura del triangulo : '))
    h += 1
    for i in range(h):
        h -= 1
        print("\n")
        if h > 0:
            for j in range(h):
                print('*', end='')


def Collatz():
    c = int(input('Ingrese un número : '))
    l = [c]
    for j in l:
        if l[-1] != 1:
            if l[-1] % 2 == 0:
                p = int(l[-1] / 2)
                l.append(p)
            else:
                i = int(( l[-1] * 3 ) + 1)
                l.append(i)
    print(l)     




















print("*********************")
print("*********************")
print("a . Hacer un réctangulo")
print("b . Hacer un octágono")
print("c . Hacer un triangulo")
print("d . Serie de Collatz")
print("e . Salir")
print("*********************")
print("*********************")









o = input("Ingrese una opcción: ")
if o == "a":
    MakeRectangle()
elif o == "b":
    print("b")
elif o == "c":
    MakeTriangle()
elif o == "d":
    Collatz()
elif o == "e":
    print("Saliendo")    
    exit()
else :
    print("Opccion erronea, saliendo")    
    exit()






# ejemplo:
# Para evitar que en cada impresion se ejecute en una nueva linea, se puede agregar el parametro end y este indicara como queremos que actue 
#al finalizar la linea, su valor por defecto es \n, pero si le cambiamos a * entonces, al finalizar la impresion, colocara un asterisco en vez de un salto de linea
# for numero in range(5):
#     print(numero, end="*")

# Escriba una funcion que le pida al usuario ingresar la altura y el ancho de un rectangulo y
# que lo dibuje usando *, ejemplo:
# altura: 5
# ancho: 4
# Resultado:
# ****
# ****
# ****
# ****
# ****

        







# Escribir una funcion que nosotros le ingresemos el lado de un octagono y que lo dibuje
# Ejemplo:
# Lados: 5
#       *****
#      *******
#     *********
#    ***********
#   *************
#   ************* -
#   *************
#   ************* -
#   *************
#    ***********
#     *********
#      *******
#       *****







# De acuerdo a la altura que nosotros ingresemos, nos tiene que dibujar el triangulo
# invertido
# Ejemplo
# Altura: 4
# ****
# ***
# **
# *







# Ingresar un numero entero y ese numero debe de llegar a 1 usando la serie de Collatz
# si el numero es par, se divide entre dos
# si el numero es impar, se multiplica por 3 y se suma 1
# la serie termina cuando el numero es 1
# Ejemplo 19
# 19 58 29 88 44 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 12

# Una vez resuelto todos los ejercicios, crear un menu de seleccion que permita escoger
# que ejercicio queremos ejecutar hasta que escribamos "salir" ahi recien va a terminar
# de escoger el ejercicio


   





