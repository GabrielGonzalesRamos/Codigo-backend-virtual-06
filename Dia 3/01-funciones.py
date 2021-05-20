# una funcion es un bloque de codigo que se puede reutilizar cuantas veces sea necesario

def saludar():
    """ Funcion que saluda cordialmente  """
    print("Hola amigos buenas tardes")
saludar()

# las funciones TAMBIEN pueden recibir parametros que son variables que solamente
# existiran dentro de las mismas

def saludarConNombre(nombre):
    """ Funcion que recibe un nombre e imprime un saludo personalizado  """
    print(f"Hola {nombre}, buenas tardes")

saludarConNombre("José")   


# para definir parametros opcionales se tiene que indicar cual sera su valor en el
# caso que al llamar a la funcion no se provea dicho parametro
def saludoOpcional(nombre=None):
    print(f"Hola {nombre}, ¿Como estas?")

saludoOpcional()


# Los parametros opccionales deben de ir al final
def registro(correo, nombre=None):
    print("Registro exitoso")

registro("admin@admin.com")

# funcion que reciba dos numeros y si la sumatoria de ambos numeros es par, indicar
# su mitad y si es impar, retoronar el resultado de la sumatoria



def parImpar( a,b  ):
    if ( a + b ) % 2 == 0:
        print(f"Su numero es par y la division entre dos es: {( a + b)/2}")
    else :
        print(f"Su numero es impar y la suma entre los dos es {(a + b )}")

parImpar(9,8)

 


# el parametro *args es una lista dinamica de elementos para recibir un numero ilimitado de argumentos
def inscritos( *args ):
    print(args)
inscritos("Eduardo","Carlos","Ricardo","Gmelina","Jesus",1,50.36565,False)


# si queremos modificar una variable que se encuentra de manera global (en todo el documento) en una
# funcion, tendremos que definir dicha variable de manera global para que, si existe fuera de la funcion, la 
# sobreescriba, si no cambiamos el valor, mantendrá el mismo que se declaro fuera de la funcion


def alumnos( *args  ):
    aprobado = 0
    desaprobado = 0
    for i in args:
        if (i["nota"] > 10):
            aprobado += 1
        else :
            desaprobado += 1 
    print(f" Existen: \n {aprobado} alumnos aprobados \n y {desaprobado} alumnos desaprobados")        
alumnos({"nombre": "Eduardo", "nota": 7}, 
        {"nombre": "Fidel", "nota": 16}, 
        {"nombre": "Raul", "nota": 18}, 
        {"nombre": "Marta", "nota": 20}, 
        {"nombre": "Juliana", "nota": 14}, 
        {"nombre": "Fabiola", "nota": 16}, 
        {"nombre": "Lizbeth", "nota": 15},
        {"nombre": "Gabriel", "nota": 2})

# Keyword arguments => **kwargs sirve para pasar un numero indeterminado de parametros PERO
# a diferencia del args en este caso tenemos que definir el nombre del parametro

def indeterminada(**kwargs):
    indeterminada(nombre="Eduardo",apellido="de Rivero", nacionalidad="Peruano")
    indeterminada(nombre="Maria",apellido="Bustinza", sexo="Femenino")
    indeterminada(nota=20, edad=18)

def mifuncion(*args, **kwargs):
    print(args)
    print(kwargs)
mifuncion(10,"eduardo",False,nacionalidad="Peruano")


def multiplicacion(numero1, numero2):
    return numero1 * numero2
print(multiplicacion(10,15))

