import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, nombre, correo, contraseña):
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña  # La contraseña se pasa aquí en texto plano y se hashea en agregar_usuario

    def verificar_contraseña(self, contraseña_plana):
         return check_password_hash(self.contraseña, contraseña_plana)


def conectar_bd():
    return psycopg2.connect(
        dbname='evaindRegistros',
        user='postgres',
        password='arbolito157',
        host='localhost',
        port='5432'
    )

def inicializar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()
    # Asegúrate de que el nombre de la columna aquí coincida con el de tu base de datos
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        correo TEXT NOT NULL UNIQUE,
                        contraseña TEXT NOT NULL)""")  # Cambiado contraseña_hash a contraseña
    conn.commit()
    conn.close()

def agregar_usuario(usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    contraseña_hash = generate_password_hash(usuario.contraseña)
    # Cambiado contraseña_hash a contraseña, para coincidir con tu esquema de base de datos
    cursor.execute("""INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s, %s)""",
                   (usuario.nombre, usuario.correo, contraseña_hash))
    conn.commit()
    conn.close()

def obtener_usuario_por_correo(correo):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Asegúrate de seleccionar la columna 'contraseña', no 'contraseña_hash'
    cursor.execute("SELECT id, nombre, correo, contraseña FROM usuarios WHERE correo = %s", (correo,))
    usuario_data = cursor.fetchone()
    conn.close()
    if usuario_data:
        usuario = Usuario(usuario_data[1], usuario_data[2], usuario_data[3])
        usuario.id = usuario_data[0]  # Asigna el id después de la creación
        return usuario
    return None

def existe_usuario(correo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

# Inicializar la base de datos al arrancar la aplicación
inicializar_bd()