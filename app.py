from controllers.preparacion import PreparacionesController
from flask import Flask, request
# Para usar las variables declaradas en el archivo .env
from dotenv import load_dotenv
from os import environ
from config.conexion_bd import base_de_datos
from flask_restful import Api
from controllers.postre import BusquedaPostre, PostresController, PostreController
from controllers.ingrediente import IngredienteController,IngredientesController
from controllers.preparacion import PreparacionesController
from models.receta import RecetaModel
from flask_swagger_ui import get_swaggerui_blueprint


load_dotenv()

# Configurar el swagger en FLASK
SWAGGER_URL = "/api/docs" # Esta variable sirve para indicar en que ruta (endpoint) se encuentra la documentacion
API_URL = "/static/swagger.json" # indica la ubicacion del archivo json
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Reposteria Flask - Swagger Documentation"
    }
)
# Fin configuracion
app = Flask(__name__)
# sirve para registrar en el caso que nosotros tengamos un proyecto interno para agregarlo a un proyecto principal
app.register_blueprint(swagger_blueprint)
api = Api(app)
# dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')


# si se establece en TRUE, Flask-SQLAlchemy rastreara las modificaciones de los objetos y lanzara
# señales. su valor predeterminado es None, igual habilita el tracking pero emite una advertencia
# que se deshabilitara de manera predeterminada en futuras versiones. esto consume memoria adicional
# y si no se va a utilizar es mejor desactivarla (False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# crea todas las tablas definidas en los modelos en el proyecto
base_de_datos.init_app(app)

# sirve para eliminar todas las tablas y limpiar la BD
# esto se utiliza en fasesa tempranas del proyecto y antes de pasar a produccion si 
# usamos la misma bd, para limpiar la informacion falsa

base_de_datos.create_all(app=app)
@app.route("/")
def initial_controller():
    return{
        "message": "Bienvenido a mi API de RECETAS DE POSTRES 🎂"
    }
# defino las rutas usando Flask Restful
api.add_resource(PostresController,"/postres")
api.add_resource(PostreController,"/postres/<int:id>")
api.add_resource(BusquedaPostre, "/busqueda_postre")
api.add_resource(PreparacionesController, "/preparaciones", "/preparaciones/<int:postre_id>")
api.add_resource(IngredienteController,"/ingredientes/<int:id>")
api.add_resource(IngredientesController,"/ingredientes")


if __name__ =='__main__':
    app.run(debug=True)