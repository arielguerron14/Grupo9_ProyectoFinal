# Importación de módulos necesarios
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

from models.models import Usuario, agregar_usuario, obtener_usuario_por_correo, existe_usuario  # Importación de modelos y funciones de base de datos

import openai  # Para interactuar con la API de OpenAI

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['C']  # Nombre de la base de datos en MongoDB

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
            return redirect(url_for('funcionamiento'))
        else:
            flash('Correo electrónico o contraseña incorrecta.', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

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

if __name__ == '__main__':
    app.run(debug=True)