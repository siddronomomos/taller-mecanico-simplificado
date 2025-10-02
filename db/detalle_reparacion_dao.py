from typing import Dict, List, Optional

from api_client import ApiClient, ApiError, shared_client


class DetalleReparacionDAO:
    def __init__(self, client: Optional[ApiClient] = None):
        self.client = client or shared_client

    def _normalize(self, data: dict) -> Dict:
        return {
            'detalle_id': data.get('id'),
            'folio': data.get('folio'),
            'pieza_id': data.get('piezaId'),
            'cantidad': data.get('cantidad'),
            'precio_unitario': data.get('precioUnitario'),
            'descripcion': data.get('descripcionPieza'),
            'precio_actual': data.get('precioActual'),
        }

    def save(self, folio: int, pieza_id: int, cantidad: int, precio_unitario: float) -> bool:
        payload = {
            'folio': folio,
            'piezaId': pieza_id,
            'cantidad': cantidad,
            'precioUnitario': precio_unitario,
        }

        try:
            self.client.post('/detalles', json=payload)
            return True
        except ApiError as error:
            print(f"Error al guardar detalle de reparación: {error}")
            return False

    def delete(self, detalle_id: int) -> bool:
        try:
            self.client.delete(f"/detalles/{detalle_id}")
            return True
        except ApiError as error:
            print(f"Error al eliminar detalle de reparación: {error}")
            return False

    def delete_by_folio(self, folio: int) -> bool:
        detalles = self.get_by_folio(folio)
        resultado = True
        for detalle in detalles:
            if detalle.get('detalle_id') and not self.delete(detalle['detalle_id']):
                resultado = False
        return resultado

    def get(self, detalle_id: int) -> Optional[Dict]:
        detalles = self.get_by_folio(0)
        for detalle in detalles:
            if detalle.get('detalle_id') == detalle_id:
                return detalle
        return None

    def get_by_folio(self, folio: int) -> List[Dict]:
        try:
            data = self.client.get(f"/detalles/folio/{folio}") or []
            return [self._normalize(item) for item in data]
        except ApiError as error:
            print(f"Error al obtener detalles por folio: {error}")
            return []

    def get_by_pieza(self, pieza_id: int) -> List[Dict]:
        # No existe endpoint específico; devolvemos lista vacía para compatibilidad.
        return []

    def get_total_by_folio(self, folio: int) -> float:
        detalles = self.get_by_folio(folio)
        return sum((detalle['cantidad'] or 0) * (detalle['precio_unitario'] or 0) for detalle in detalles)

    def update(self, detalle_id: int, cantidad: int, precio_unitario: float) -> bool:  # pragma: no cover - no endpoint disponible
        return False

    def update_pieza_stock(self, pieza_id: int, cantidad: int) -> bool:  # pragma: no cover - manejado por la API
        return False