from typing import List, Optional, Dict
from mysql.connector import Error
from db.connection import Connection
from models.pieza import Pieza

class DetalleReparacionDAO:
    def __init__(self):
        self.connection = Connection()
    
    def save(self, folio: int, pieza_id: int, cantidad: int, precio_unitario: float) -> bool:
        """Guarda un nuevo detalle de reparación en la base de datos"""
        query = """
            INSERT INTO detalle_reparaciones (folio, pieza_id, cantidad, precio_unitario)
            VALUES (%(folio)s, %(pieza_id)s, %(cantidad)s, %(precio_unitario)s)
        """
        params = {
            'folio': folio,
            'pieza_id': pieza_id,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al guardar detalle de reparación: {e}")
            self.connection.rollback()
            return False
    
    def update(self, detalle_id: int, cantidad: int, precio_unitario: float) -> bool:
        """Actualiza un detalle de reparación existente"""
        query = """
            UPDATE detalle_reparaciones
            SET cantidad = %(cantidad)s,
                precio_unitario = %(precio_unitario)s
            WHERE detalle_id = %(detalle_id)s
        """
        params = {
            'detalle_id': detalle_id,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar detalle de reparación: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, detalle_id: int) -> bool:
        """Elimina un detalle de reparación por su ID"""
        query = "DELETE FROM detalle_reparaciones WHERE detalle_id = %s"
        
        try:
            self.connection.cursor.execute(query, (detalle_id,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar detalle de reparación: {e}")
            self.connection.rollback()
            return False
    
    def delete_by_folio(self, folio: int) -> bool:
        """Elimina todos los detalles asociados a un folio de reparación"""
        query = "DELETE FROM detalle_reparaciones WHERE folio = %s"
        
        try:
            self.connection.cursor.execute(query, (folio,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar detalles por folio: {e}")
            self.connection.rollback()
            return False
    
    def get(self, detalle_id: int) -> Optional[Dict]:
        """Obtiene un detalle de reparación por su ID"""
        query = """
            SELECT d.*, p.descripcion as pieza_descripcion
            FROM detalle_reparaciones d
            JOIN piezas p ON d.pieza_id = p.pieza_id
            WHERE d.detalle_id = %s
        """
        
        try:
            self.connection.cursor.execute(query, (detalle_id,))
            result = self.connection.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error al obtener detalle de reparación: {e}")
            return None
    
    def get_by_folio(self, folio: int) -> List[Dict]:
        """Obtiene todos los detalles asociados a un folio de reparación"""
        query = """
            SELECT d.*, p.descripcion as pieza_descripcion, p.precio as precio_actual
            FROM detalle_reparaciones d
            JOIN piezas p ON d.pieza_id = p.pieza_id
            WHERE d.folio = %s
            ORDER BY d.detalle_id
        """
        detalles = []
        
        try:
            self.connection.cursor.execute(query, (folio,))
            results = self.connection.cursor.fetchall()
            return results
        except Error as e:
            print(f"Error al obtener detalles por folio: {e}")
            return []
    
    def get_by_pieza(self, pieza_id: int) -> List[Dict]:
        """Obtiene todos los detalles asociados a una pieza específica"""
        query = """
            SELECT d.*, r.fecha_entrada, r.estado
            FROM detalle_reparaciones d
            JOIN reparaciones r ON d.folio = r.folio
            WHERE d.pieza_id = %s
            ORDER BY r.fecha_entrada DESC
        """
        detalles = []
        
        try:
            self.connection.cursor.execute(query, (pieza_id,))
            results = self.connection.cursor.fetchall()
            return results
        except Error as e:
            print(f"Error al obtener detalles por pieza: {e}")
            return []
    
    def get_total_by_folio(self, folio: int) -> float:
        """Calcula el total de la reparación sumando todos los detalles"""
        query = """
            SELECT SUM(cantidad * precio_unitario) as total
            FROM detalle_reparaciones
            WHERE folio = %s
        """
        
        try:
            self.connection.cursor.execute(query, (folio,))
            result = self.connection.cursor.fetchone()
            return result['total'] if result and result['total'] else 0.0
        except Error as e:
            print(f"Error al calcular total de reparación: {e}")
            return 0.0
    
    def update_pieza_stock(self, pieza_id: int, cantidad: int) -> bool:
        """Actualiza el stock de una pieza después de asignarla a una reparación"""
        query = """
            UPDATE piezas
            SET existencias = existencias - %s
            WHERE pieza_id = %s AND existencias >= %s
        """
        
        try:
            self.connection.cursor.execute(query, (cantidad, pieza_id, cantidad))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar stock de pieza: {e}")
            self.connection.rollback()
            return False