# Un controlador es el comportamiento que va a tener mi API
# cuando se llame a determinada ruta
# /postres GET  => mostrar los postres
from os import name
from models.postre import PostreModel
from flask_restful import Resource, reqparse
from config.conexion_bd import base_de_datos

# Serializador o serializer
# un pequeño filtro de lo que necesitará el post

# Agrupa los errores bundle_errors
serializerPostres = reqparse.RequestParser(bundle_errors=True)
serializerPostres.add_argument(
    'nombre', # nombre del atributo en el body
    type=str, # tipo de dato que me tiene que mandar
    required=True, # si es de caracter obligatorio o no 
    help="Falta el nombre", # mensaje de ayuda en el caso fuese obligatorio y no me lo mandase
    location='json' # en que parte del request me mandará, ya sea json (body) o url
)
serializerPostres.add_argument(
    'porcion',
    type=str,
    required=True,
    help="Falta la porcion CODE: {error_msg}",
    choices=('Familiar', 'Personal', 'Mediano'),
    location='json'
)



class PostresController(Resource):
    """Será la encargada de la gestion de todos los postres y su creacion"""
    def get(self):
        # SELECT * FROM postres;
        postres = PostreModel.query.all()
        resultado = []
        for postre in postres:
            resultado.append(postre.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }, 201

    def post(self):
        data = serializerPostres.parse_args()
        nuevoPostre = PostreModel(nombre=data.get('nombre'), porcion=data.get('porcion'))
        print(nuevoPostre)
        nuevoPostre.save()
        return {
            'success': True,
            'content': nuevoPostre.json(),
            'message': "Postre creado exitosamente"
        }, 201




class PostreController(Resource):
    def get(self, id):
        
        #La documentacion nativa de SQLAlchemy
        otro_postre = base_de_datos.session.query(PostreModel).filter(PostreModel.postreId == id).first()
        otro_postre_2 = base_de_datos.session.query(PostreModel).filter_by(postreId = id).first()
        #La documentacion del flask sql alchemy
        postre = PostreModel.query.filter_by(postreId = id).first()
        print(postre)
        print(otro_postre)
        print(otro_postre_2)
        return 'ok'