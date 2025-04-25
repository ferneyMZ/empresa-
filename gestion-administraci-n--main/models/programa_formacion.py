from mongoengine import *

class ProgramaFormacion(Document):
    nombre = StringField(required=True, unique=True)
    
    def __str__(self):
        return self.nombre