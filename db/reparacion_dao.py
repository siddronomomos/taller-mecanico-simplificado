from typing import List, Optional
from mysql.connector import Error
from models.reparacion import Reparacion
from db.connection import Connection

class ReparacionDAO:
    def __init__(self):
        self.connection = Connection()
    
    def save(self, reparacion: Reparacion) -> bool:
        if not reparacion.validate():
            return False
            
        query = """
            INSERT INTO reparaciones (matricula, fecha_entrada, fecha_salida, estado)
            VALUES (%(matricula)s, %(fecha_entrada)s, %(fecha_salida)s, %(estado)s)
        """
        params = {
            'matricula': reparacion.matricula,
            'fecha_entrada': reparacion.fecha_entrada,
            'fecha_salida': reparacion.fecha_salida,
            'estado': reparacion.estado
        }
        
        try:
            self.connection.cursor.execute(query, params)
            reparacion.folio = self.connection.cursor.lastrowid
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al guardar reparación: {e}")
            self.connection.rollback()
            return False
    
    def update(self, reparacion: Reparacion) -> bool:
        if not reparacion.validate() or not reparacion.folio:
            return False
            
        query = """
            UPDATE reparaciones
            SET matricula = %(matricula)s,
                fecha_entrada = %(fecha_entrada)s,
                fecha_salida = %(fecha_salida)s,
                estado = %(estado)s
            WHERE folio = %(folio)s
        """
        params = {
            'folio': reparacion.folio,
            'matricula': reparacion.matricula,
            'fecha_entrada': reparacion.fecha_entrada,
            'fecha_salida': reparacion.fecha_salida,
            'estado': reparacion.estado
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al actualizar reparación: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, folio: int) -> bool:
        query = "DELETE FROM reparaciones WHERE folio = %s"
        
        try:
            self.connection.cursor.execute(query, (folio,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar reparación: {e}")
            self.connection.rollback()
            return False
    
    def get(self, folio: int) -> Optional[Reparacion]:
        query = """
            SELECT r.*, v.marca, v.modelo, c.nombre as cliente_nombre
            FROM reparaciones r
            JOIN vehiculos v ON r.matricula = v.matricula
            JOIN clientes c ON v.cliente_id = c.cliente_id
            WHERE r.folio = %s
        """
        
        try:
            self.connection.cursor.execute(query, (folio,))
            result = self.connection.cursor.fetchone()
            
            if result:
                reparacion = Reparacion(
                    folio=result['folio'],
                    matricula=result['matricula'],
                    fecha_entrada=result['fecha_entrada'],
                    fecha_salida=result['fecha_salida'],
                    estado=result['estado']
                )
                reparacion.info_vehiculo = f"{result['marca']} {result['modelo']}"
                reparacion.info_cliente = result['cliente_nombre']
                return reparacion
            return None
        except Error as e:
            print(f"Error al obtener reparación: {e}")
            return None
    
    def get_all(self) -> List[Reparacion]:
        query = """
            SELECT r.*, v.marca, v.modelo, c.nombre as cliente_nombre
            FROM reparaciones r
            JOIN vehiculos v ON r.matricula = v.matricula
            JOIN clientes c ON v.cliente_id = c.cliente_id
            ORDER BY r.fecha_entrada DESC
        """
        reparaciones = []
        
        try:
            self.connection.cursor.execute(query)
            results = self.connection.cursor.fetchall()
            
            for result in results:
                reparacion = Reparacion(
                    folio=result['folio'],
                    matricula=result['matricula'],
                    fecha_entrada=result['fecha_entrada'],
                    fecha_salida=result['fecha_salida'],
                    estado=result['estado']
                )
                reparacion.info_vehiculo = f"{result['marca']} {result['modelo']}"
                reparacion.info_cliente = result['cliente_nombre']
                reparaciones.append(reparacion)
            return reparaciones
        except Error as e:
            print(f"Error al obtener reparaciones: {e}")
            return []
    
    def get_by_vehicle(self, matricula: str) -> List[Reparacion]:
        query = """
            SELECT r.*
            FROM reparaciones r
            WHERE r.matricula = %s
            ORDER BY r.fecha_entrada DESC
        """
        reparaciones = []
        
        try:
            self.connection.cursor.execute(query, (matricula,))
            results = self.connection.cursor.fetchall()
            
            for result in results:
                reparaciones.append(Reparacion(
                    folio=result['folio'],
                    matricula=result['matricula'],
                    fecha_entrada=result['fecha_entrada'],
                    fecha_salida=result['fecha_salida'],
                    estado=result['estado']
                ))
            return reparaciones
        except Error as e:
            print(f"Error al obtener reparaciones por vehículo: {e}")
            return []