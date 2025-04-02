# create_admin.py
import bcrypt
from db.connection import Connection

def create_admin_user():
    conn = None
    try:
        # Datos del admin
        username = "admin"
        password = "admin"
        nombre = "Administrador"
        perfil = "admin"
        
        # Generar hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Conexión a la base de datos
        conn = Connection()
        cursor = conn.con.cursor(dictionary=True)
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE user_name = %s", (username,))
        if cursor.fetchone():
            print(f"El usuario '{username}' ya existe en la base de datos")
            return False
        
        # Insertar nuevo admin
        cursor.execute(
            """INSERT INTO usuarios 
            (nombre, user_name, password, perfil) 
            VALUES (%s, %s, %s, %s)""",
            (nombre, username, hashed_password, perfil)
        )
        conn.con.commit()
        
        print(f"Usuario admin creado exitosamente: {username}/{password}")
        return True
        
    except Exception as e:
        print(f"Error al crear usuario admin: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_admin_user()