from typing import List, Optional

from api_client import ApiClient, ApiError, shared_client
from models.cliente import Cliente


class ClienteDAO:
    def __init__(self, client: Optional[ApiClient] = None):
        self.client = client or shared_client

    def _to_model(self, data: dict) -> Cliente:
        return Cliente(
            cliente_id=data.get('id'),
            usuario_id=data.get('usuarioId'),
            nombre=data.get('nombre'),
            telefono=data.get('telefono'),
            rfc=data.get('rfc'),
            fecha_registro=data.get('fechaRegistro'),
        )

    def save(self, cliente: Cliente) -> Optional[Cliente]:
        if not cliente.validate():
            return None

        payload = {
            'usuarioId': cliente.usuario_id,
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'rfc': cliente.rfc,
        }

        try:
            data = self.client.post('/clientes', json=payload)
            if isinstance(data, dict):
                nuevo = self._to_model(data)
                cliente.cliente_id = nuevo.cliente_id
                cliente.fecha_registro = nuevo.fecha_registro
            return cliente
        except ApiError as error:
            print(f"Error al guardar cliente: {error}")
            return None

    def update(self, cliente: Cliente) -> bool:
        if not cliente.cliente_id or not cliente.validate():
            return False

        payload = {
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'rfc': cliente.rfc,
        }

        try:
            self.client.put(f"/clientes/{cliente.cliente_id}", json=payload)
            return True
        except ApiError as error:
            print(f"Error al actualizar cliente: {error}")
            return False

    def delete(self, cliente_id: int) -> bool:
        try:
            self.client.delete(f"/clientes/{cliente_id}")
            return True
        except ApiError as error:
            if error.status_code == 409:
                raise ApiError(error.status_code, "El cliente tiene registros relacionados", error.details)
            print(f"Error al eliminar cliente: {error}")
            return False

    def get(self, cliente_id: int) -> Optional[Cliente]:
        try:
            data = self.client.get(f"/clientes/{cliente_id}")
            if isinstance(data, dict):
                return self._to_model(data)
            return None
        except ApiError as error:
            print(f"Error al obtener cliente: {error}")
            return None

    def get_all(self) -> List[Cliente]:
        try:
            data = self.client.get('/clientes') or []
            return [self._to_model(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener clientes: {error}")
            return []