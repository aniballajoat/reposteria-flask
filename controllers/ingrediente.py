from flask_restful import Resource,reqparse
from models.ingrediente import IngredienteModel
from config.conexion_bd import base_de_datos

serializerIngredientes = reqparse.RequestParser(bundle_errors=True)
serializerIngredientes.add_argument(
    'nombre',               #nombre del atributo en el body
    type=str,               #tipo de dato que me tiene que mandar
    required=True,          #si es de caracter obligatorio o no
    help="falta el nombre", #mensaje de ayuda en el caso fuese obligatorio y no me lo mandase
    location='json'         #en que parte del request me mandara, ya sea json (body) o url
)


class IngredientesController(Resource):
    def get(self):
        ingredientes = base_de_datos.session.query(IngredienteModel).all()
        resultado = []
        for ingrediente in ingredientes:
            print(ingrediente.json())
            resultado.append(ingrediente.json())
        return {
            'success':True,
            'content':resultado.json(),
            'message':None
        }
    
    def post(self):
        data = serializerIngredientes.parse_args()
        nuevoIngrediente = IngredienteModel(nombre=data.get(
            'nombre')
            )
        print(nuevoIngrediente)
        nuevoIngrediente.save()

        return {
            'succes':True,
            'content':nuevoIngrediente.json(),
            'message':'Ingrediente creado exitosamente'
        },201

class IngredienteController(Resource):
    def get(self,id):
        ingrediente = base_de_datos.session.query(IngredienteModel).filter_by(ingredienteId=id).first()
        print(ingrediente)
        return ({
            'success':True,
            'content': ingrediente.json(),
            'message':None
        },200) if ingrediente else ({
            'success':False,
            'content': None,
            'message':'Ingrediente no encontrado'
        }, 404)
    def put(self,id):
        ingrediente = base_de_datos.session.query(IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente:
            data = serializerIngredientes.parse_args()
            ingrediente.ingredienteNombre = data.get('nombre')
            ingrediente.save()

            return{
                'success': True,
                'content': ingrediente.json(),
                'message':'Ingrediente actualizado correctamente'
            },201
        else:
            return{
                'success': False,
                'content': None,
                'message':'Ingrediente no encontrado'
            },404