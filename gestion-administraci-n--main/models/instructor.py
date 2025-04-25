from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash

class Instructor(Document):
    nombre_completo = StringField(required=True)
    correo = EmailField(required=True)
    password_hash = StringField(required=True)
    regional = ReferenceField('Regional')
    activo = BooleanField(default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)