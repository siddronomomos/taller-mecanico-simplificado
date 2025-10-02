from typing import List, Optional

from api_client import ApiClient, ApiError, shared_client
from models.pieza import Pieza


class PiezaDAO:
    def __init__(self, client: Optional[ApiClient] = None):
        self.client = client or shared_client

    def _to_model(self, data: dict) -> Pieza:
        return Pieza(
            pieza_id=data.get('id'),
            descripcion=data.get('descripcion'),
            existencias=data.get('existencias', 0),
            precio=float(data.get('precio', 0)),
        )

    def save(self, pieza: Pieza) -> bool:
        if not pieza.validate():
            return False

        payload = {
            'descripcion': pieza.descripcion,
            'existencias': pieza.existencias,
            'precio': pieza.precio,
        }

        try:
            data = self.client.post('/piezas', json=payload)
            if isinstance(data, dict):
                pieza.pieza_id = data.get('id')
            return True
        except ApiError as error:
            print(f"Error al guardar pieza: {error}")
            return False

    def update(self, pieza: Pieza) -> bool:
        if not pieza.pieza_id or not pieza.validate():
            return False

        payload = {
            'descripcion': pieza.descripcion,
            'existencias': pieza.existencias,
            'precio': pieza.precio,
        }

        try:
            self.client.put(f"/piezas/{pieza.pieza_id}", json=payload)
            return True
        except ApiError as error:
            print(f"Error al actualizar pieza: {error}")
            return False

    def update_stock(self, pieza_id: int, cantidad: int) -> bool:
        try:
            data = self.client.patch(f"/piezas/{pieza_id}/stock", json={'delta': cantidad})
            return bool(data)
        except ApiError as error:
            print(f"Error al actualizar stock: {error}")
            return False

    def delete(self, pieza_id: int) -> bool:
        try:
            self.client.delete(f"/piezas/{pieza_id}")
            return True
        except ApiError as error:
            print(f"Error al eliminar pieza: {error}")
            return False

    def get(self, pieza_id: int) -> Optional[Pieza]:
        try:
            data = self.client.get(f"/piezas/{pieza_id}")
            if isinstance(data, dict):
                return self._to_model(data)
            return None
        except ApiError as error:
            print(f"Error al obtener pieza: {error}")
            return None

    def get_all(self) -> List[Pieza]:
        try:
            data = self.client.get('/piezas') or []
            return [self._to_model(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener piezas: {error}")
            return []