from flask_restful import Resource, reqparse
from models.movimiento import MovimientoModel
from datetime import datetime
from flask_jwt import jwt_required, current_identity

class MovimientosController(Resource):
    movimientoSerializer = reqparse.RequestParser(bundle_errors=True)
    movimientoSerializer.add_argument( 'nombre', type=str, required=True, help="Falta el nombre", location='json')
    movimientoSerializer.add_argument( 'monto', type=float, required=True, help="Falta el monto", location='json')
    movimientoSerializer.add_argument( 'fecha', type=str, required=False, location='json')
    movimientoSerializer.add_argument( 'imagen', type=str, required=False, location='json')
    movimientoSerializer.add_argument( 'tipo', type=str, required=True,  help="Falta el tipo", location='json', choices=['ingreso', 'egreso'])
    
    # Con el decorador jwt_required se indica que el metodo de esta clase recibirá una token  (Es protegida)
    @jwt_required()
    def post(self):
        print(current_identity)
        data = self.movimientoSerializer.parse_args()
        print(data)
        try:
            # strptime : Convierte de un string a una fecha mediante un formato 
            # strftime : Convierte de una fecha a un string
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
        except:
            return {
                "success": False,
                "message": "Formato de fecha incorrecto, El formato debe de ser YYYY-MM-DD HH-MM-SS"
            }    
        print(type(fecha))
        return 'ok'

    def get(self):
        pass