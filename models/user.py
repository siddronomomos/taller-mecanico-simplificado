from dataclasses import dataclass
from typing import Optional, Literal

PerfilType = Literal['admin', 'mecanico', 'aux']

@dataclass
class User:
    usuario_id: Optional[int] = None
    nombre: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
    perfil: PerfilType = 'aux'
    
    def validate(self) -> bool:
        if not all([self.nombre, self.user_name, self.password]):
            return False
        if len(self.user_name) < 4:
            return False
        if len(self.password) < 6:
            return False
        return True
    
    def set_password(self, password: str):
        import bcrypt
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def check_password(self, password: str) -> bool:
        import bcrypt
        try:
            # Asegúrate que self.password es el hash almacenado
            if not self.password or not isinstance(self.password, str):
                return False
                
            # Verifica el formato del hash
            if not self.password.startswith('$2b$'):
                print(f"Hash inválido: {self.password}")
                return False
                
            # Compara la contraseña
            return bcrypt.checkpw(password.encode(), self.password.encode())
        except Exception as e:
            print(f"Error en check_password: {str(e)}")
            return False
    
    def __str__(self):
        return f"{self.nombre} ({self.perfil})"