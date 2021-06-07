# un controlador es el comportamiento que va a tener mi API cuando se llame a determinada ruta
# /postres GET => mostrar los postres
#from typing_extensions import Required
from flask_restful import Resource, reqparse
from models.postre import PostreModel
from config.conexion_bd import base_de_datos


# serializer (serializador)
serializerPostres = reqparse.RequestParser(bundle_errors=True)
serializerPostres.add_argument(
    'nombre',               #nombre del atributo en el body
    type=str,               #tipo de dato que me tiene que mandar
    required=True,          #si es de caracter obligatorio o no
    help="falta el nombre", #mensaje de ayuda en el caso fuese obligatorio y no me lo mandase
    location='json'         #en que parte del request me mandara, ya sea json (body) o url
)

serializerPostres.add_argument(
    'porcion',
    type=str,
    required=True,
    help="Falta la porcion {error_msg}",
    choices=('Familiar','Personal','Mediano'),
    location='json'
)
class PostresController(Resource):
    def get(self):
        # SELECT * FROM postres;
        postres = PostreModel.query.all()
        resultado = []
        for postre in postres:
            print(postre.json())
            resultado.append(postre.json())
        return {
            'success':True,
            'content':resultado,
            'message':None
        }


    def post(self):
        data = serializerPostres.parse_args()
        nuevoPostre = PostreModel(nombre=data.get(
            'nombre'), porcion=data.get('porcion')
            )
        print(nuevoPostre)
        nuevoPostre.save()

        return {
            'succes':True,
            'content':nuevoPostre.json(),
            'message':'Postre creado exitosamente'
        },201
class PostreController(Resource):
    def get(self,id):
        postre = PostreModel.query.filter_by(postreId=id).first()
        print(postre)
        return ({
            'success':True,
            'content': postre.json(),
            'message':None
        },200) if postre else ({
            'success':False,
            'content': None,
            'message':'Postre no encontrado'
        }, 404)
    def put(self,id):
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).first()
        if postre:
            data = serializerPostres.parse_args()
            postre.postreNombre = data.get('nombre')
            postre.postrePorcion = data.get('porcion')
            postre.save()

            return{
                'success': True,
                'content': postre.json(),
                'message':'Postre actualizado correctamente'
            },201
        else:
            return{
                'success': False,
                'content': None,
                'message':'Postre no encontrado'
            },404
    def delete(self,id):
        #postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).delete(synchronize_session='fetch')
        #base_de_datos.session.commit()
        postre = base_de_datos.session.query(
            PostreModel).filter_by(postreId=id).first()
        if postre:
            postre.delete()
            return{
                'success':True,
                'content':postre.json(),
                'message': 'Postre eliminado exitosamente'
            }
        else:
            return{
                'success': False,
                'content': None,
                'message':'Postre no existe'
            }
class BusquedaPostre(Resource):
    serializerBusqueda = reqparse.RequestParser()
    serializerBusqueda.add_argument(
        'nombre',
        type= str,
        location='args',
        required=False,
    )
    serializerBusqueda.add_argument(
        'porcion',
        type=str,
        location='args',
        required=False,
        choices=('Familiar','Personal','Mediano'),
        help='Opcion invalida, las opciones son Familiar, Personal, Mediano'
    )

    def get(self):
        #Ejercicio
        #primero validar si hay nombre, porcion o ambos
        #luego devolver todos los postres que hagan match con la busqueda
        filtros = self.serializerBusqueda.parse_args()
        
        if filtros.get('nombre'):
            if filtros.get('porcion'):
                resultado = base_de_datos.session.query(PostreModel).filter_by(
                    postreNombre=filtros.get('nombre'),postrePorcion=filtros.get('porcion')).all()
            else:
                resultado = base_de_datos.session.query(PostreModel).filter_by(
                postreNombre=filtros.get('nombre')).all()
        elif filtros.get('porcion'):
            resultado = base_de_datos.session.query(PostreModel).filter_by(
                postrePorcion=filtros.get('porcion')).all()
        else:
            return{
                'message': 'Necesitas dar al menos un parametro'
            },400
        postres = []
        for postre in resultado:
            postres.append(postre.json())
        return{
            "message": None,
            "content":postres,
            "success":True
        }