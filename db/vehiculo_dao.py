from typing import List, Optional
from mysql.connector import Error
from models.vehiculo import Vehiculo
from db.connection import Connection

class VehiculoDAO:
    def __init__(self):
        self.connection = Connection()
    
    def save(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.validate():
            return False
            
        query = """
            INSERT INTO vehiculos (matricula, serie, modelo, marca, anio, cliente_id)
            VALUES (%(matricula)s, %(serie)s, %(modelo)s, %(marca)s, %(anio)s, %(cliente_id)s)
        """
        params = {
            'matricula': vehiculo.matricula,
            'serie': vehiculo.serie,
            'modelo': vehiculo.modelo,
            'marca': vehiculo.marca,
            'anio': vehiculo.anio,
            'cliente_id': vehiculo.cliente_id
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al guardar vehículo: {e}")
            self.connection.rollback()
            return False
    
    def update(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.validate():
            return False
            
        query = """
            UPDATE vehiculos
            SET serie = %(serie)s,
                modelo = %(modelo)s,
                marca = %(marca)s,
                anio = %(anio)s,
                cliente_id = %(cliente_id)s
            WHERE matricula = %(matricula)s
        """
        params = {
            'matricula': vehiculo.matricula,
            'serie': vehiculo.serie,
            'modelo': vehiculo.modelo,
            'marca': vehiculo.marca,
            'anio': vehiculo.anio,
            'cliente_id': vehiculo.cliente_id
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar vehículo: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, matricula: str) -> bool:
        query = "DELETE FROM vehiculos WHERE matricula = %s"
        
        try:
            self.connection.cursor.execute(query, (matricula,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar vehículo: {e}")
            self.connection.rollback()
            return False
    
    def get(self, matricula: str) -> Optional[Vehiculo]:
        query = """
            SELECT v.*, c.nombre as cliente_nombre
            FROM vehiculos v
            JOIN clientes c ON v.cliente_id = c.cliente_id
            WHERE v.matricula = %s
        """
        
        try:
            self.connection.cursor.execute(query, (matricula,))
            result = self.connection.cursor.fetchone()
            
            if result:
                vehiculo = Vehiculo(
                    matricula=result['matricula'],
                    serie=result['serie'],
                    modelo=result['modelo'],
                    marca=result['marca'],
                    anio=result['anio'],
                    cliente_id=result['cliente_id']
                )
                vehiculo.cliente_nombre = result['cliente_nombre']
                return vehiculo
            return None
        except Error as e:
            print(f"Error al obtener vehículo: {e}")
            return None
    
    def get_all(self) -> List[Vehiculo]:
        query = """
            SELECT v.*, c.nombre as cliente_nombre
            FROM vehiculos v
            JOIN clientes c ON v.cliente_id = c.cliente_id
            ORDER BY v.marca, v.modelo
        """
        vehiculos = []
        
        try:
            self.connection.cursor.execute(query)
            results = self.connection.cursor.fetchall()
            
            for result in results:
                vehiculo = Vehiculo(
                    matricula=result['matricula'],
                    serie=result['serie'],
                    modelo=result['modelo'],
                    marca=result['marca'],
                    anio=result['anio'],
                    cliente_id=result['cliente_id']
                )
                vehiculo.cliente_nombre = result['cliente_nombre']
                vehiculos.append(vehiculo)
            return vehiculos
        except Error as e:
            print(f"Error al obtener vehículos: {e}")
            return []
    
    def get_by_client(self, cliente_id: int) -> List[Vehiculo]:
        query = """
            SELECT v.*
            FROM vehiculos v
            WHERE v.cliente_id = %s
            ORDER BY v.marca, v.modelo
        """
        vehiculos = []
        
        try:
            self.connection.cursor.execute(query, (cliente_id,))
            results = self.connection.cursor.fetchall()
            
            for result in results:
                vehiculos.append(Vehiculo(
                    matricula=result['matricula'],
                    serie=result['serie'],
                    modelo=result['modelo'],
                    marca=result['marca'],
                    anio=result['anio'],
                    cliente_id=result['cliente_id']
                ))
            return vehiculos
        except Error as e:
            print(f"Error al obtener vehículos por cliente: {e}")
            return []