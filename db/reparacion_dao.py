from datetime import date
from typing import List, Optional

from api_client import ApiClient, ApiError, shared_client
from models.reparacion import Reparacion


class ReparacionDAO:
    def __init__(self, client: Optional[ApiClient] = None):
        self.client = client or shared_client

    def _parse_date(self, value: Optional[str]) -> Optional[date]:
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None

    def _normalize(self, data: dict) -> Reparacion:
        reparacion = Reparacion(
            folio=data.get('folio'),
            matricula=data.get('matricula'),
            fecha_entrada=self._parse_date(data.get('fechaEntrada')),
            fecha_salida=self._parse_date(data.get('fechaSalida')),
            estado=data.get('estado', 'pendiente')
        )
        reparacion.info_vehiculo = data.get('infoVehiculo')
        reparacion.info_cliente = data.get('infoCliente')
        return reparacion

    def _serialize(self, reparacion: Reparacion) -> dict:
        return {
            'matricula': reparacion.matricula,
            'fechaEntrada': reparacion.fecha_entrada.isoformat() if reparacion.fecha_entrada else None,
            'fechaSalida': reparacion.fecha_salida.isoformat() if reparacion.fecha_salida else None,
            'estado': reparacion.estado,
        }

    def save(self, reparacion: Reparacion) -> Optional[int]:
        if not reparacion.validate():
            return None

        payload = self._serialize(reparacion)

        try:
            data = self.client.post('/reparaciones', json=payload) or {}
            folio = data.get('folio')
            reparacion.folio = folio
            return folio
        except ApiError as error:
            print(f"Error al guardar reparación: {error}")
            return None

    def update(self, reparacion: Reparacion) -> bool:
        if not reparacion.folio or not reparacion.validate():
            return False

        payload = self._serialize(reparacion)

        try:
            self.client.put(f"/reparaciones/{reparacion.folio}", json=payload)
            return True
        except ApiError as error:
            print(f"Error al actualizar reparación: {error}")
            return False

    def delete(self, folio: int) -> bool:
        try:
            self.client.delete(f"/reparaciones/{folio}")
            return True
        except ApiError as error:
            print(f"Error al eliminar reparación: {error}")
            return False

    def get(self, folio: int) -> Optional[Reparacion]:
        try:
            data = self.client.get(f"/reparaciones/{folio}")
            if not data:
                return None
            return self._normalize(data)
        except ApiError as error:
            print(f"Error al obtener reparación: {error}")
            return None

    def get_all(self) -> List[Reparacion]:
        try:
            data = self.client.get('/reparaciones') or []
            return [self._normalize(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener reparaciones: {error}")
            return []

    def get_by_vehicle(self, matricula: str) -> List[Reparacion]:
        try:
            data = self.client.get(f"/reparaciones/vehiculo/{matricula}") or []
            return [self._normalize(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener reparaciones por vehículo: {error}")
            return []

    def delete_with_transaction(self, folio: int) -> bool:
        return self.delete(folio)