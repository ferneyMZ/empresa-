from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from models.instructor import Instructor  # Solo importa lo que existe
from models.regional import Regional
from models.programa_formacion import ProgramaFormacion  # Import the missing model
import yagmail
import os
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        
        instructor = Instructor.objects(correo=correo).first()
        
        if instructor and instructor.check_password(password):
            session['instructor_id'] = str(instructor.id)
            session['nombre_instructor'] = instructor.nombre_completo
            session['regional_id'] = str(instructor.regional.id) if instructor.regional else None
            return redirect(url_for('guias.listar_guias'))
        else:
            flash('Credenciales incorrectas', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            nombre_completo = request.form['nombre_completo']
            correo = request.form['correo']
            password = request.form['password']
            regional_id = request.form['regional']
            
            regional = Regional.objects.get(id=regional_id)
            
            instructor = Instructor(
                nombre_completo=nombre_completo,
                correo=correo,
                regional=regional
            )
            instructor.set_password(password)
            instructor.save()
            
            # Enviar correo con credenciales
            enviar_correo_registro(instructor, password)
            
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'danger')
    
    regionales = Regional.objects()
    return render_template('auth/register.html', regionales=regionales)

def enviar_correo_registro(instructor, password):
    try:
        yag = yagmail.SMTP(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASSWORD'))
        
        subject = 'Bienvenido a la Plataforma de Guías de Aprendizaje SENA'
        contents = f"""
        <h2>Bienvenido {instructor.nombre_completo}</h2>
        <p>Tu registro en la plataforma de Guías de Aprendizaje del SENA ha sido exitoso.</p>
        <p><strong>Tus credenciales de acceso son:</strong></p>
        <ul>
            <li>Correo: {instructor.correo}</li>
            <li>Contraseña: {password}</li>
        </ul>
        <p>Te recomendamos cambiar tu contraseña después de iniciar sesión.</p>
        """
        
        yag.send(to=instructor.correo, subject=subject, contents=contents)
    except Exception as e:
        print(f"Error enviando correo: {str(e)}")

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/agregar_regional', methods=['GET', 'POST'])
def agregar_regional():
    if request.method == 'POST':
        nombre = request.form['nombre']
        try:
            regional = Regional(nombre=nombre)
            regional.save()
            flash('Regional creada exitosamente', 'success')
            return redirect(url_for('auth.agregar_regional'))
        except Exception as e:
            flash(f'Error al crear regional: {str(e)}', 'danger')
    
    return render_template('auth/agregar_regional.html')

@auth_bp.route('/agregar_programa', methods=['GET', 'POST'])
def agregar_programa():
    if 'instructor_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        nombre = request.form['nombre']
        try:
            programa = ProgramaFormacion(nombre=nombre)
            programa.save()
            flash('Programa de formación creado exitosamente', 'success')
            return redirect(url_for('auth.agregar_programa'))
        except Exception as e:
            flash(f'Error al crear programa: {str(e)}', 'danger')
    
    return render_template('auth/agregar_programa.html')
