from mongoengine import *
from datetime import datetime

class GuiaAprendizaje(Document):
    nombre = StringField(required=True)
    descripcion = StringField(required=True)
    programa_formacion = ReferenceField('ProgramaFormacion')
    archivo_pdf = StringField(required=True)
    fecha_subida = DateTimeField(default=datetime.utcnow)
    instructor = ReferenceField('Instructor')
    
    meta = {
        'indexes': [
            'nombre',
            'programa_formacion',
            'instructor'
        ]
    }