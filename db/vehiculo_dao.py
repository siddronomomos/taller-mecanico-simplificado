from typing import List, Optional

from api_client import ApiClient, ApiError, shared_client
from models.vehiculo import Vehiculo


class VehiculoDAO:
    def __init__(self, client: Optional[ApiClient] = None):
        self.client = client or shared_client

    def _to_model(self, data: dict) -> Vehiculo:
        vehiculo = Vehiculo(
            matricula=data.get('matricula'),
            serie=data.get('serie'),
            modelo=data.get('modelo'),
            marca=data.get('marca'),
            anio=data.get('anio'),
            cliente_id=data.get('clienteId'),
        )
        vehiculo.cliente_nombre = data.get('clienteNombre')
        return vehiculo

    def save(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.validate():
            return False

        payload = {
            'matricula': vehiculo.matricula,
            'serie': vehiculo.serie,
            'modelo': vehiculo.modelo,
            'marca': vehiculo.marca,
            'anio': vehiculo.anio,
            'clienteId': vehiculo.cliente_id,
        }

        try:
            self.client.post('/vehiculos', json=payload)
            return True
        except ApiError as error:
            print(f"Error al guardar vehículo: {error}")
            return False

    def update(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.validate():
            return False

        payload = {
            'serie': vehiculo.serie,
            'modelo': vehiculo.modelo,
            'marca': vehiculo.marca,
            'anio': vehiculo.anio,
            'clienteId': vehiculo.cliente_id,
        }

        try:
            self.client.put(f"/vehiculos/{vehiculo.matricula}", json=payload)
            return True
        except ApiError as error:
            print(f"Error al actualizar vehículo: {error}")
            return False

    def delete(self, matricula: str) -> bool:
        try:
            self.client.delete(f"/vehiculos/{matricula}")
            return True
        except ApiError as error:
            print(f"Error al eliminar vehículo: {error}")
            return False

    def get(self, matricula: str) -> Optional[Vehiculo]:
        try:
            data = self.client.get(f"/vehiculos/{matricula}")
            if isinstance(data, dict):
                return self._to_model(data)
            return None
        except ApiError as error:
            print(f"Error al obtener vehículo: {error}")
            return None

    def get_all(self) -> List[Vehiculo]:
        try:
            data = self.client.get('/vehiculos') or []
            return [self._to_model(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener vehículos: {error}")
            return []

    def get_by_client(self, cliente_id: int) -> List[Vehiculo]:
        try:
            data = self.client.get('/vehiculos') or []
            return [self._to_model(item) for item in data if item.get('clienteId') == cliente_id]
        except ApiError as error:
            print(f"Error al obtener vehículos por cliente: {error}")
            return []