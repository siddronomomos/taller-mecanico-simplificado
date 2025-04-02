from typing import List, Optional
from mysql.connector import Error
from models.user import User, PerfilType
from db.connection import Connection

class UserDAO:
    def __init__(self):
        self.connection = Connection()
        self.cursor = self.connection.con.cursor(dictionary=True)
    
    def save(self, user: User) -> bool:
        if not user.validate():
            return False
            
        query = """
            INSERT INTO usuarios (nombre, user_name, password, perfil)
            VALUES (%(nombre)s, %(user_name)s, %(password)s, %(perfil)s)
        """
        params = {
            'nombre': user.nombre,
            'user_name': user.user_name,
            'password': user.password,
            'perfil': user.perfil
        }
        
        try:
            self.connection.cursor.execute(query, params)
            user.usuario_id = self.connection.cursor.lastrowid
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al guardar usuario: {e}")
            self.connection.rollback()
            return False
    
    def update(self, user: User) -> bool:
        if not user.validate() or not user.usuario_id:
            return False
            
        query = """
            UPDATE usuarios
            SET nombre = %(nombre)s,
                user_name = %(user_name)s,
                password = %(password)s,
                perfil = %(perfil)s
            WHERE usuario_id = %(usuario_id)s
        """
        params = {
            'usuario_id': user.usuario_id,
            'nombre': user.nombre,
            'user_name': user.user_name,
            'password': user.password,
            'perfil': user.perfil
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar usuario: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, usuario_id: int) -> bool:
        query = "DELETE FROM usuarios WHERE usuario_id = %s"
        
        try:
            self.connection.cursor.execute(query, (usuario_id,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
            self.connection.rollback()
            return False
    
    def get(self, usuario_id: int) -> Optional[User]:
        query = "SELECT * FROM usuarios WHERE usuario_id = %s"
        
        try:
            self.connection.cursor.execute(query, (usuario_id,))
            result = self.connection.cursor.fetchone()
            
            if result:
                user = User(
                    usuario_id=result['usuario_id'],
                    nombre=result['nombre'],
                    user_name=result['user_name'],
                    password=result['password'],
                    perfil=result['perfil']
                )
                return user
            return None
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        query = "SELECT * FROM usuarios WHERE user_name = %s"
        
        try:
            self.connection.cursor.execute(query, (username,))
            result = self.connection.cursor.fetchone()
            
            if result:
                user = User(
                    usuario_id=result['usuario_id'],
                    nombre=result['nombre'],
                    user_name=result['user_name'],
                    password=result['password'],
                    perfil=result['perfil']
                )
                return user
            return None
        except Error as e:
            print(f"Error al obtener usuario por nombre: {e}")
            return None
    
    def login(self, username: str, password: str) -> Optional[User]:
        try:
            self.cursor.execute(
                "SELECT * FROM usuarios WHERE user_name = %s",
                (username,)
            )
            result = self.cursor.fetchone()
            
            if not result:
                return None
                
            user = User()
            user.usuario_id = result['usuario_id']
            user.nombre = result['nombre']
            user.user_name = result['user_name']
            user.password = result['password']  # Asegúrate que esto está incluido
            user.perfil = result['perfil']
            
            # Verificación de contraseña mejorada
            if not user.password.startswith('$2b$'):
                print(f"Error: Formato de hash inválido para usuario {username}")
                return None
                
            if user.check_password(password):
                return user
                
            return None
            
        except Exception as e:
            print(f"Error en login: {str(e)}")
            return None
    
    def get_all(self) -> List[User]:
        query = "SELECT * FROM usuarios ORDER BY nombre"
        users = []
        
        try:
            self.connection.cursor.execute(query)
            results = self.connection.cursor.fetchall()
            
            for result in results:
                users.append(User(
                    usuario_id=result['usuario_id'],
                    nombre=result['nombre'],
                    user_name=result['user_name'],
                    password=result['password'],
                    perfil=result['perfil']
                ))
            return users
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    def get_by_profile(self, perfil: PerfilType) -> List[User]:
        query = "SELECT * FROM usuarios WHERE perfil = %s ORDER BY nombre"
        users = []
        
        try:
            self.connection.cursor.execute(query, (perfil,))
            results = self.connection.cursor.fetchall()
            
            for result in results:
                users.append(User(
                    usuario_id=result['usuario_id'],
                    nombre=result['nombre'],
                    user_name=result['user_name'],
                    password=result['password'],
                    perfil=result['perfil']
                ))
            return users
        except Error as e:
            print(f"Error al obtener usuarios por perfil: {e}")
            return []
        
    def reset_password(self, username: str, new_password: str) -> bool:
        try:
            user = User()
            user.user_name = username
            user.set_password(new_password)
            
            self.cursor.execute(
                "UPDATE usuarios SET password = %s WHERE user_name = %s",
                (user.password, username)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error al resetear password: {str(e)}")
            return False