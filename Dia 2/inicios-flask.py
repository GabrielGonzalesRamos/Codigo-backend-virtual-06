from flask_cors import CORS
from flask import Flask, request


# __name__ muestra si el archivo en el cual se esta llamando a la clase Flask, 
# es el archivo principal del proyecto, para evitar que la isntancia de la clase
# de Flask se pueda crear varias veces  (patron Singleton)

# si estamos en el archivo principal nos impirmirá => __main__, caso contrario
# imprimirá otra cosa
print(__name__)
app = Flask(__name__)

# hacerlo de esta manera hara que todos los valores se seteen a un que permita aboslutamente TODOS
# los origenes, metodos y cabeceras
CORS(app, methods=['GET','POST'], origins=['*'])
productos = []

# Debajo de todo decorador se debe de poner una funcion o una clase
# un decorador es un patron de software que se utiliza para modificar el 
# funcionamiento de una función o clase en particular sin la necesidad
# de emplear otro metodos como herencia

@app.route("/")
def inicio():
    print("Me están llamado")
    return "Saludos desde mi API"

@app.route("/productos", methods=['GET', 'POST', 'PUT'])
# Controlador : lo que va a suceder con cada ruta cuando se ejcuta un método
def gestion_productos():
    data = request.get_json() #Mediante este método podemos ver la informacion que me esta mandando el frontedn mendiante el body
    if request.method == 'POST':
        print(data)
        productos.append(data)
        return {
            "message": "Producto creado exitosamente",
            "content": data
        }, 201
    if request.method == 'GET':
        return{
            "message": "Estos son los productos registrados",
            "content": productos
        }, 200

# NOTA! : Al hacer un get queda PROHIBIDO enviar información mediante el body
@app.route("/productos/<int:id>", methods=['PUT','DELETE','GET'])
def gestion_producto(id):
    if len(productos) <= id:
        return {
            "mensaje": "Producto no encontrado"
        }
    if request.method == "GET":
        return {
            "content": productos[id]
        }, 200
    elif request.method == "DELETE":
        productos.pop(id)
        return{
             "mensaje": "Producto eliminado exitosamente"
        }   
    elif request.method == "PUT":
        data = request.get_json()
        productos[id] = data

        return {
            "mensaje": "Producto actualizado exitosamente",
            "content": productos[id]
        }

@app.route("/productos/buscar")
def buscar_productos():
    print(request.args.get("nombre"))
    return "ok"



app.run(debug=True)

# NOTA! : todo codigo que pongamos luego del metodo run() NUNCA se ejecutará, debido 
#  a que el método run() hace que se quede "colgado" mi programa levantando un servidor
 