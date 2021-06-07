from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class RecetaModel(base_de_datos.Model):
    __tablename__="recetas"
    recetaId = Column(name='id', primary_key=True, 
                nullable=False, unique=True, type_=types.Integer, autoincrement=True)
    recetaCantidad = Column(name='cantidad', type_=types.Integer)
    recetaUnidadMedida = Column(name='unidad_medida', type_=types.String(20))

    postre = Column(ForeignKey(column='postres.id', ondelete="CASCADE"),
                    name='postre_id', type_=types.Integer, nullable=False)
    ingrediente = Column(ForeignKey(column='ingredientes.id', ondelete="CASCADE"),
                    name='ingredientes_id', type_=types.Integer, nullable=False)

    def __init__(self, cantidad, unidad_medida, postre, ingrediente):
        self.recetaCantidad = cantidad
        self.recetaUnidadMedida = unidad_medida
        self.postre = postre
        self.ingrediente = ingrediente