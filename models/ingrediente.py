from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm

class IngredienteModel(base_de_datos.Model):
    __tablename__ = "ingredientes"
    ingredienteId = Column(name= "id", primary_key=True, 
                            type_=types.Integer, unique=True, autoincrement=True, nullable=False)
    ingredienteNombre = Column(
        name='nombre', type_=types.String(length=45), nullable=False)
    recetas = orm.relationship('RecetaModel', backref='recetaIngrediente')

    # asi se crean las relaciones entre un modelo y otro
    # ondelete sirve para indicar que accion tomaran todas las FK cuando una pk sea eliminada
    # CASCADE => Eliminara en forma de cascada primero la PK y luego todas sus FK
    # DELETE => Se eliminara y dejara las FK con el mismo valor generandoinformacion incorrecta
    # RESTRICT => restringir la eliminacion siempre y cuando tenga FK existentes
    # None => (default)no hagas nada
    recetas = orm.relationship('RecetaModel', backref='recetaIngrediente')

    def __init__(self,nombre):
        self.ingredienteNombre = nombre

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def json(self):
        return{
            "id": self.ingredienteId,
            "nombre":self.ingredienteNombre
        }