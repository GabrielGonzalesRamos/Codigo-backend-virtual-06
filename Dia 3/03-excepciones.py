# Las excepciones son formas de evitar que nuestros
# programas se casheen (se caigan) y asi controlar de una
# mejor manera el cilo de nuestro programa

try:
    numero = int(input("Ingrese un número: "))
    print(numero + 10)
except ZeroDivisionError:
    print("No se puede dividir entre 0")
except ValueError:
    print("Debiste ingresar un numero")
except KeyboardInterrupt:
    print("Proceso cancelado")
#print(10/0)    

## Finally  => no le importa si todo salio bien o si hubo un error, igual se ejecutará
## Pero luego mostrará el erro si es que no se declaro una excepción

## Else => para usar el else se debe de declarar un except y este se ejecutará cuando no ingresa a ningun except
## Osea la operacion fue exitosa

try:
    print(10/1)
except:
    print("Error")
else:
    print("Todo bien")
finally:
    print("Ejecutado de todas maneras")



e = 0
for i in range(1,5):
    try:
        int(input("Ingresa un número : "))
    except ValueError:
        print("Debe de ingresar un número")
        e += 1
print(f"Hubo {e} intentos fallidos")


