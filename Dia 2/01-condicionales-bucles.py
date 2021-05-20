# Metodo que sirve para ingresar datos por la terminal
#edad = int(input("Ingresa otra vez tu edad: "))
##print(type(edad), edad)

## CONDICION
## IF (SI) ELSE (SINO)
## el ELIF siempre va antes del else, el else se utiliza como ultima medida si no logro hacer match con alguna de las anteriores condiciones
#restriccion_edad = 18
#if edad >= restriccion_edad and edad < 65 :
#    print("Eres mayor de edad")
#elif edad >= 65 :
#    print('Eres jubilado') 
#else :
#    print('Eres menos de edad')

## Operadores Ternarios    

#respuesta = "ERES MAYOR DE EDAD" if(edad >= 18) else "ERES MENOR DE EDAD"
#print(respuesta)


#numero = int(input("Ingrese un número: "))

#if numero == 0 :
#    print("El numero digitado es 0")
#elif numero < 0 :
#    print("El numero ingresado es negativo")
#else :
#    print("Su numero es positivo")




# FOR

mes = ['ENERO','FEBRERO','MARZO','ABRIL']
for i in mes:
    print(i)

# range(n) => n será el tope y la serie comenzará en 0
# range(n,m) => n será el piso o la cantidad inicial y m sera el tope
# range (n,m,p) => n será el piso o la cantidad inicial, m sera el tope y p será el cuanto se modificará en cada ciclo ese valor
for numero in range(1,10):
    print(numero)


for i in range(200,300,5):
    print(i)

# el for tambien sirve para iterar todas las colecciones de datos

diccionario = {
        "nombre" : "eduardo",
        "apellido" : "Martinez"
        }
# En el caso de un diccionario al momento de iterar, iterará las llaves
for i in diccionario :
    print(diccionario[i])


# De los siguinete numero indicar cuantos son positivos y cuantos son negativos
numeros = [1,-4,5,-14,-16,-50,6,-100]
np = 0
nn = 0
for i in numeros:
    if i > 0:
        np += 1
    else :
        nn += 1
print(f"La cantidad de número positivos son: {np} y negativos es {nn}")



# break => hace que el bucle finalice de manera repentina sin terminar todo 
# el ciclo completo
for i in range(10):
    print(i)
    if i == 5:
        break
# continue => salta la iteracion actual y no permite que el resto del codigo se ejecute
for i in range(10):
    if i == 5:
        continue
    print(i)
    
# dados los siguientes numeros numeros = [1, 2, 5, 9, 12, 15, 10, 34, 867, 67] # indicar cuantos de ellos son multiplos de 3 y de 5, ademas, si hay un multiplo de 3 y de 5 no contabilizarlo

numerosA = [1, 2, 5, 9, 12, 15, 10, 34, 867, 67]
m3 = 0
m5 = 0

for i in numerosA:
    if  i % 3 == 0 and i % 5 == 0:
      continue
    elif i % 3 == 0:
        m3 += 1
    elif i % 5 == 0:
        m5 += 1

print( f'Los numeros multiplos de -3- son {m3} y multiplos de -5- son {m5}')

edad = 25 
while edad > 18 :
    print(edad)
    edad -= 1

# ingresar por teclado 3 nombres y de acuerdo a ello indicar cuantos pertenecen a la siguiente lista de personas inscritas 
inscritos = ["raul", "pedro", "maria", "roxana", "margioret"]
for i  in range(1,4):
    nombre_ingresado = input("Ingrese el nombre {}: " .format(i))
    if(nombre_ingresado in inscritos):
        print("Bienvenido(a)" .format(nombre_ingresado))



