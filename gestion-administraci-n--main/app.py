from flask import Flask, redirect, url_for
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from models.instructor import Instructor
from models.regional import Regional
from mongoengine import connect

load_dotenv()

# Configuración única de Flask
app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY')

# Configuración para subir archivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configuración de MongoDB
#app.config['MONGODB_SETTINGS'] = {'db': 'Gestionadministrativos','host': 'mongodb://localhost:27017'
# }
uri = "mongodb+srv://ferneym2003:ya78HJwphH2hOEwB@cluster0.kgcrm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
app.config['MONGODB_SETTINGS'] = {
    'db': 'Gestionadministrativos',
    'host': uri,
    #'port': 27017/instructor/
}

db = MongoEngine(app)

# Crear carpeta de uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Importar y registrar blueprints
from routes.auth import auth_bp
from routes.guias import guias_bp

app.register_blueprint(auth_bp)
app.register_blueprint(guias_bp)

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)