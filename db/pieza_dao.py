from typing import List, Optional
from mysql.connector import Error
from models.pieza import Pieza
from db.connection import Connection

class PiezaDAO:
    def __init__(self):
        self.connection = Connection()
    
    def save(self, pieza: Pieza) -> bool:
        if not pieza.validate():
            return False
            
        query = """
            INSERT INTO piezas (descripcion, existencias, precio)
            VALUES (%(descripcion)s, %(existencias)s, %(precio)s)
        """
        params = {
            'descripcion': pieza.descripcion,
            'existencias': pieza.existencias,
            'precio': pieza.precio
        }
        
        try:
            self.connection.cursor.execute(query, params)
            pieza.pieza_id = self.connection.cursor.lastrowid
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al guardar pieza: {e}")
            self.connection.rollback()
            return False
    
    def update(self, pieza: Pieza) -> bool:
        if not pieza.validate() or not pieza.pieza_id:
            return False
            
        query = """
            UPDATE piezas
            SET descripcion = %(descripcion)s,
                existencias = %(existencias)s,
                precio = %(precio)s
            WHERE pieza_id = %(pieza_id)s
        """
        params = {
            'pieza_id': pieza.pieza_id,
            'descripcion': pieza.descripcion,
            'existencias': pieza.existencias,
            'precio': pieza.precio
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar pieza: {e}")
            self.connection.rollback()
            return False
    
    def update_stock(self, pieza_id: int, cantidad: int) -> bool:
        query = """
            UPDATE piezas
            SET existencias = existencias + %s
            WHERE pieza_id = %s AND existencias + %s >= 0
        """
        
        try:
            self.connection.cursor.execute(query, (cantidad, pieza_id, cantidad))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar stock: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, pieza_id: int) -> bool:
        query = "DELETE FROM piezas WHERE pieza_id = %s"
        
        try:
            self.connection.cursor.execute(query, (pieza_id,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar pieza: {e}")
            self.connection.rollback()
            return False
    
    def get(self, pieza_id: int) -> Optional[Pieza]:
        query = "SELECT * FROM piezas WHERE pieza_id = %s"
        
        try:
            self.connection.cursor.execute(query, (pieza_id,))
            result = self.connection.cursor.fetchone()
            
            if result:
                return Pieza(
                    pieza_id=result['pieza_id'],
                    descripcion=result['descripcion'],
                    existencias=result['existencias'],
                    precio=result['precio']
                )
            return None
        except Error as e:
            print(f"Error al obtener pieza: {e}")
            return None
    
    def get_all(self) -> List[Pieza]:
        query = "SELECT * FROM piezas ORDER BY descripcion"
        piezas = []
        
        try:
            self.connection.cursor.execute(query)
            results = self.connection.cursor.fetchall()
            
            for result in results:
                piezas.append(Pieza(
                    pieza_id=result['pieza_id'],
                    descripcion=result['descripcion'],
                    existencias=result['existencias'],
                    precio=result['precio']
                ))
            return piezas
        except Error as e:
            print(f"Error al obtener piezas: {e}")
            return []