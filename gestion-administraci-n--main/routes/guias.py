from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from models.guia import GuiaAprendizaje
from models.instructor import Instructor
from models.programa_formacion import ProgramaFormacion
from datetime import datetime
import os
from flask import current_app

guias_bp = Blueprint('guias', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}  # Define las extensiones permitidas
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@guias_bp.route('/guias')
def listar_guias():
    if 'instructor_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))
    
    guias = GuiaAprendizaje.objects().order_by('-fecha_subida')
    return render_template('guias/listar.html', guias=guias)

@guias_bp.route('/guias/subir', methods=['GET', 'POST'])
def subir_guia():
    if 'instructor_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            programa_id = request.form['programa_formacion']
            archivo_pdf = request.files['archivo_pdf']
            
            if not archivo_pdf or not allowed_file(archivo_pdf.filename):
                flash('Solo se permiten archivos PDF', 'danger')
                return redirect(request.url)
            
            # Guardar el archivo PDF
            filename = secure_filename(f"{datetime.now().timestamp()}_{archivo_pdf.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            archivo_pdf.save(filepath)
            
            # Obtener referencias
            programa = ProgramaFormacion.objects.get(id=programa_id)
            instructor = Instructor.objects.get(id=session['instructor_id'])
            
            # Crear la guía
            guia = GuiaAprendizaje(
                nombre=nombre,
                descripcion=descripcion,
                programa_formacion=programa,
                archivo_pdf=filename,
                instructor=instructor
            )
            guia.save()
            
            flash('Guía de aprendizaje subida correctamente', 'success')
            return redirect(url_for('guias.listar_guias'))
        
        except Exception as e:
            flash(f'Error al subir la guía: {str(e)}', 'danger')
    
    programas = ProgramaFormacion.objects()
    return render_template('guias/subir.html', programas=programas)

@guias_bp.route('/guias/descargar/<filename>')
def descargar_guia(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@guias_bp.route('/agregar_programa', methods=['GET', 'POST'])
def agregar_programa():
    if 'instructor_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        nombre = request.form['nombre']
        try:
            programa = ProgramaFormacion(nombre=nombre)
            programa.save()
            flash('Programa creado exitosamente', 'success')
            return redirect(url_for('guias.agregar_programa'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('guias/agregar_programa.html')