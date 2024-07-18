# Importación de módulos necesarios
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_weasyprint import HTML, render_pdf  # Para renderizar PDFs en Flask
from models.models import Usuario, agregar_usuario, obtener_usuario_por_correo, existe_usuario  # Importación de modelos y funciones de base de datos
import openai  # Para interactuar con la API de OpenAI

import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



# Configuración de la aplicación Flask
app = Flask(__name__, static_folder='static')  # Creación de la aplicación Flask
app.secret_key = 'tu_clave_secreta_aqui'  # Clave secreta para sesiones de Flask


@app.route('/')
def index():
    """
    Ruta principal que renderiza la página de inicio (Index.html).
    """
    return render_template('Index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Maneja el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        nombre = request.form['nombres_completos']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        
        # Verifica si el usuario ya existe
        if existe_usuario(correo):
            flash('El correo electrónico ya está registrado.', 'error')
        else:
            # Crea un nuevo usuario y lo agrega a la base de datos
            nuevo_usuario = Usuario(nombre, correo, contraseña)
            agregar_usuario(nuevo_usuario)
            flash('Registro exitoso. Por favor inicie sesión.', 'success')
        
        return redirect(url_for('index'))
    
    return render_template('Index.html')

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    """
    Maneja el inicio de sesión de usuarios existentes.
    """
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        
        # Busca el usuario en la base de datos
        usuario = obtener_usuario_por_correo(correo)
        
        if usuario and usuario.verificar_contraseña(contraseña):
            # Establece una sesión para el usuario logueado
            session['usuario_logueado'] = usuario.correo
            return redirect(url_for('instruciones'))
        else:
            flash('Correo electrónico o contraseña incorrecta.', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/instruciones')
def instruciones():
    return render_template('instruciones.html')

@app.route('/funcionamiento')
def funcionamiento():
    """
    Renderiza la página de funcionamiento, requiere inicio de sesión.
    """
    if 'usuario_logueado' not in session:
        flash('Por favor, inicie sesión para ver esta página.', 'warning')
        return redirect(url_for('index'))
    
    correo = session['usuario_logueado']
    usuario = obtener_usuario_por_correo(correo)
    return render_template('funcionamiento.html', usuario=usuario)

@app.route('/principal')
def principal():
    return render_template('principal.html')



@app.route('/guardar_respuesta', methods=['POST'])
def guardar_respuesta():
    """
    Guarda respuestas proporcionadas por el usuario en MongoDB.
    """
    data = request.get_json()
    texto = data['texto']
    imagen_actual = data['imagen_actual']
    
    # Inserta la respuesta en la colección 'respuestas' de MongoDB
    db.respuestas.insert_one({
        'etiqueta': imagen_actual,
        'texto': texto
    })
    
    return jsonify({"mensaje": "Guardado exitosamente"})

@app.route('/perfil')
def perfil():
    """
    Renderiza la página de perfil del usuario.
    """
    return render_template('perfil.html')

@app.route('/descargar_resultados')
def descargar_resultados():
    """
    Descarga resultados en formato PDF, utilizando diagnósticos generados por OpenAI.
    """
    # Verifica que el usuario esté logueado
    if 'usuario_logueado' not in session:
        flash('Por favor, inicie sesión para acceder a esta funcionalidad.', 'warning')
        return redirect(url_for('index'))

    # Función para construir el prompt basado en la etiqueta
    def construir_prompt(etiqueta, texto_usuario):
        # Define descripciones basadas en la etiqueta de la imagen
        if etiqueta == "img1":
            descripcion = "Si ves una mariposa o un murciélago, indica..."
        elif etiqueta == "img2":
            descripcion = "Ver dos figuras humanas sugiere..."
        else:
            descripcion = "Interpretación general."
        
        return f"Interpretar la respuesta '{texto_usuario}' para la imagen {etiqueta}: {descripcion}"

    # Función para generar diagnósticos utilizando OpenAI
    def generar_diagnostico(texto_prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=texto_prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()

    # Obtener todas las respuestas almacenadas en MongoDB
    respuestas = db.respuestas.find({})
    diagnosticos = []

    # Generar diagnósticos para cada respuesta y guardarlos en una lista
    for respuesta in respuestas:
        etiqueta = respuesta['etiqueta']
        texto_usuario = respuesta['texto']
        prompt = construir_prompt(etiqueta, texto_usuario)
        diagnostico = generar_diagnostico(prompt)
        diagnosticos.append((etiqueta, diagnostico))

    # Renderiza la plantilla 'resultados_pdf.html' y genera el PDF
    html = render_template('resultados_pdf.html', diagnosticos=diagnosticos)
    return render_pdf(HTML(string=html))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No image uploaded', 'error')
        return redirect(url_for('index'))

    image = request.files['image']
    image = Image.open(image)
    # Extracción de texto utilizando Tesseract
    extracted_text = pytesseract.image_to_string(image)

    # Obtener texto adicional del formulario
    additional_text = request.form.get('additional_text', '')

    # Análisis del texto utilizando la nueva API de GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": "Eres un asistente médico útil."},
        {"role": "user", "content": f"Brindar posibles recomendaciones precisas basadas en el siguiente texto extraído de una imagen médica: {extracted_text} y la información adicional: {additional_text}"}
        ],
        max_tokens=500
    )

    analysis = response.choices[0].message['content'].strip()

    return render_template('perfil.html',  extracted_text=extracted_text, additional_text=additional_text, analysis=analysis, usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)