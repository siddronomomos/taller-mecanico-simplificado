from typing import List, Optional

from api_client import ApiClient, ApiError, shared_client
from models.user import PerfilType, User


class UserDAO:
    """Acceso a usuarios mediante la API REST."""

    def __init__(self, client: Optional[ApiClient] = None):
        self.client = client or shared_client

    def _to_model(self, data: dict) -> User:
        return User(
            usuario_id=data.get('id'),
            nombre=data.get('nombre'),
            user_name=data.get('userName'),
            perfil=data.get('perfil'),
        )

    def save(self, user: User) -> bool:
        if not user.validate():
            return False

        payload = {
            'nombre': user.nombre,
            'userName': user.user_name,
            'password': user.password,
            'perfil': user.perfil,
        }

        try:
            data = self.client.post('/users', json=payload)
            if isinstance(data, dict):
                user.usuario_id = data.get('id')
            user.password = None
            return True
        except ApiError as error:
            print(f"Error al guardar usuario: {error}")
            return False

    def update(self, user: User) -> bool:
        if not user.usuario_id or not user.validate(update=True):
            return False

        payload = {
            'nombre': user.nombre,
            'userName': user.user_name,
            'perfil': user.perfil,
        }
        if user.password:
            payload['password'] = user.password

        try:
            self.client.put(f"/users/{user.usuario_id}", json=payload)
            user.password = None
            return True
        except ApiError as error:
            print(f"Error al actualizar usuario: {error}")
            return False

    def delete(self, usuario_id: int) -> bool:
        try:
            self.client.delete(f"/users/{usuario_id}")
            return True
        except ApiError as error:
            print(f"Error al eliminar usuario: {error}")
            return False

    def get(self, usuario_id: int) -> Optional[User]:
        try:
            data = self.client.get(f"/users/{usuario_id}")
            if isinstance(data, dict):
                return self._to_model(data)
            return None
        except ApiError as error:
            print(f"Error al obtener usuario: {error}")
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            usuarios = self.client.get('/users') or []
            for item in usuarios:
                if item.get('userName') == username:
                    return self._to_model(item)
            return None
        except ApiError as error:
            print(f"Error al obtener usuario por nombre: {error}")
            return None

    def login(self, username: str, password: str) -> Optional[User]:
        try:
            data = self.client.post('/auth/login', json={'userName': username, 'password': password})
            if isinstance(data, dict):
                return self._to_model(data.get('user', data))
            return None
        except ApiError as error:
            print(f"Error en login: {error}")
            return None

    def get_all(self) -> List[User]:
        try:
            data = self.client.get('/users') or []
            return [self._to_model(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener usuarios: {error}")
            return []

    def get_by_profile(self, perfil: PerfilType) -> List[User]:
        try:
            data = self.client.get('/users') or []
            return [self._to_model(item) for item in data if item.get('perfil') == perfil]
        except ApiError as error:
            print(f"Error al obtener usuarios por perfil: {error}")
            return []

    def reset_password(self, username: str, new_password: str) -> bool:
        user = self.get_by_username(username)
        if not user:
            return False

        user.password = new_password
        return self.update(user)