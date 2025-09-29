from typing import List, Optional
from mysql.connector import Error, IntegrityError
from models.cliente import Cliente
from db.connection import Connection

class ClienteDAO:
    def __init__(self):
        self.connection = Connection()
    
    def save(self, cliente: Cliente) -> Optional[Cliente]:
        if not cliente.validate():
            return None
            
        query = """
            INSERT INTO clientes (usuario_id, nombre, telefono, rfc)
            VALUES (%(usuario_id)s, %(nombre)s, %(telefono)s, %(rfc)s)
        """
        params = {
            'usuario_id': cliente.usuario_id,
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'rfc': cliente.rfc
        }
        
        try:
            self.connection.cursor.execute(query, params)
            cliente.cliente_id = self.connection.cursor.lastrowid
            self.connection.commit()
            return cliente
        except Error as e:
            print(f"Error al guardar cliente: {e}")
            self.connection.rollback()
            return None
    
    def update(self, cliente: Cliente) -> bool:
        if not cliente.validate() or not cliente.cliente_id:
            return False
            
        query = """
            UPDATE clientes
            SET nombre = %(nombre)s,
                telefono = %(telefono)s,
                rfc = %(rfc)s
            WHERE cliente_id = %(cliente_id)s
        """
        params = {
            'cliente_id': cliente.cliente_id,
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'rfc': cliente.rfc
        }
        
        try:
            self.connection.cursor.execute(query, params)
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except Error as e:
            print(f"Error al actualizar cliente: {e}")
            self.connection.rollback()
            return False
    
    def delete(self, cliente_id: int) -> bool:
        query = "DELETE FROM clientes WHERE cliente_id = %s"
        
        try:
            self.connection.cursor.execute(query, (cliente_id,))
            self.connection.commit()
            return self.connection.cursor.rowcount > 0
        except IntegrityError:
            # Error de clave foránea: el cliente tiene registros asociados
            self.connection.rollback()
            raise IntegrityError("El cliente tiene vehículos u otros registros asociados y no puede ser eliminado.")
        except Error as e:
            print(f"Error al eliminar cliente: {e}")
            self.connection.rollback()
            return False
    
    def get(self, cliente_id: int) -> Optional[Cliente]:
        query = "SELECT * FROM clientes WHERE cliente_id = %s"
        
        try:
            self.connection.cursor.execute(query, (cliente_id,))
            result = self.connection.cursor.fetchone()
            
            if result:
                return Cliente(
                    cliente_id=result['cliente_id'],
                    usuario_id=result['usuario_id'],
                    nombre=result['nombre'],
                    telefono=result['telefono'],
                    rfc=result['rfc'],
                    fecha_registro=result['fecha_registro']
                )
            return None
        except Error as e:
            print(f"Error al obtener cliente: {e}")
            return None
    
    def get_all(self) -> List[Cliente]:
        query = "SELECT * FROM clientes ORDER BY nombre"
        clientes = []
        
        try:
            self.connection.cursor.execute(query)
            results = self.connection.cursor.fetchall()
            
            for result in results:
                clientes.append(Cliente(
                    cliente_id=result['cliente_id'],
                    usuario_id=result['usuario_id'],
                    nombre=result['nombre'],
                    telefono=result['telefono'],
                    rfc=result['rfc'],
                    fecha_registro=result['fecha_registro']
                ))
            return clientes
        except Error as e:
            print(f"Error al obtener clientes: {e}")
            return []