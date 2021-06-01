from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import math
from os import environ


load_dotenv()
print(environ.get("HOST"))
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = environ.get("HOST_DB")
app.config['MYSQL_DATABASE_USER'] = environ.get("USER_DB")
app.config['MYSQL_DATABASE_PASSWORD'] = environ.get("PASSWORD")
app.config['MYSQL_DATABASE_DB'] = environ.get("DATABASE")
app.config['MYSQL_DATABASE_PORT'] = int(environ.get("PORT"))
#print(app.config)

# CREAMOS UNA INSTANCIA DE LA CLASE MySQL y le pasamos a su constructor la configuracion

mysql = MySQL(app)

@app.route("/alumnos")
def gestion_alumnos():
    # PRIMERO SE CREA UN CURSOR QUE SE CONECTARÁ A LA BD 
    # LUEGO REGISTROS LA SENTENCIA YA SEA UN DDL o UN DML
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM alumnos")
    # CAPTURO LA INFORMACION DE LA CONSULTA
    alumnos = cur.fetchall()
    alumnos_dict = []
    for alumno in alumnos:
        alumno_dict = {
            "id": alumno[0],
            "matricula": alumno[1],
            "nombre": alumno[2],
            "apellido": alumno[3],
            "localidad": alumno[4],
            "fecha_nacimiento": alumno[5]
        }
        alumnos_dict.append(alumno_dict)
    return {
        "data": alumnos_dict
    }    

@app.route("/alumnos-paginados", methods=['GET'])
def alumnos_paginados():
    if(request.args.get('pagina') and request.args.get('porPagina')):
        # HELPER
        porPagina = int(request.args.get('porPagina'))
        pagina = int(request.args.get('pagina'))
        limit = porPagina
        offset = ( pagina - 1 ) * porPagina
        cur =  mysql.get_db().cursor()
        # %s cadena (lo vuelve string)
        # %d integral
        # %f flotante
        # %.<digitos> numeros flotantes con una cantidad fija de decimales
        cur.execute("SELECT * FROM alumnos LIMIT %s OFFSET %s" % (limit, offset)) 
        resultado = cur.fetchall()
        print(len(resultado))
        # AHORA HACEMOS LOS DATOS DE PAGINACION
        cur.execute("SELECT COUNT(*) FROM alumnos") 
        total = int(cur.fetchone()[0])
        itemsPorPagina = porPagina if total >= porPagina else total
        totalPaginas = math.ceil(total / itemsPorPagina)
        if pagina > 1:
            paginaPrevia = pagina - 1 if pagina <= totalPaginas else None
        else:
            paginaPrevia = None
        if totalPaginas > 1:
            paginaContinua = pagina + 1 if pagina < totalPaginas else None
        else:
            paginaContinua = None    
        print(resultado)
    return {
        "data": [],
        "paginacion": {
            "total": total, #Total de paginas
            "porPagina": itemsPorPagina, # pagina actual
            "paginaPrevia": request.host_url + "alumnos-paginados?pagina=" + str(paginaPrevia) + "&porPagina=" + str(porPagina) if paginaPrevia else None, # pagina previa
            "paginaContinua": request.host_url + "alumnos-paginados?pagina=" + str(paginaContinua) + "&porPagina=" + str(porPagina) if paginaContinua else None, # pagina continua
            "totalPaginas": totalPaginas # total de paginas
        }
    }

app.run(debug=True, port=8000)
