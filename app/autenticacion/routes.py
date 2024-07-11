from flask import request, redirect, url_for
from models.models import Usuario, agregar_usuario
from app import app

@app.route('/register', methods=['POST'])
def register():
    nombres_completos = request.form['nombres_completos']
    correo = request.form['correo']
    contraseña = request.form['contraseña']

    usuario = Usuario(nombres_completos, correo, contraseña)
    agregar_usuario(usuario)

    return redirect(url_for('/templates/Index.html'))