from conection import Connection as con
from cliente import Cliente
from dbVehiculo import dbVehiculo
from user import User
from dbUser import dbUser
from vehiculo import Vehiculo

class dbCliente:
    def __init__(self):
        self.connection = con()
        self.cursor = self.connection.open()
        if self.cursor == None:
            raise ConnectionError("Error al conectar con la base de datos")
        
    def test_connection(self) -> bool:
        try:
            self.cursor.execute("SELECT 1")
        except Exception as e:
            print(f"Prueba de conexión fallida: {e}")
            return False
        return True
    
    def save(self, cliente: Cliente) -> bool:
        try:
            self.cursor.execute("""
                INSERT INTO clientes (usuario_id, nombre, telefono, rfc)
                VALUES (%s, %s, %s, %s)
            """, (cliente.getUsuarioID(), cliente.getNombre(), cliente.getTelefono(), cliente.getRFC()))
            self.connection.commit()
        except:
            return False
        return True
    
    def update(self, cliente: Cliente) -> bool:
        try:
            self.cursor.execute("""
                UPDATE clientes
                SET usuario_id = %s, nombre = %s, telefono = %s, rfc = %s
                WHERE cliente_id = %s
            """, (cliente.getUsuarioID(), cliente.getNombre(), cliente.getTelefono(), cliente.getRFC(), cliente.getID()))
            self.connection.commit()
        except:
            return False
        return True
    
    def delete(self, cliente: Cliente) -> bool:
        try:
            self.cursor.execute("""
                DELETE FROM clientes
                WHERE cliente_id = %s
            """, (cliente.getID(),))
            self.connection.commit()
        except:
            return False
        return True
    
    def get(self, cliente: Cliente) -> Cliente | None:
        try:
            self.cursor.execute("""
                SELECT * FROM clientes
                WHERE cliente_id = %s
            """, (cliente.getID(),))
            row = self.cursor.fetchone()
            cliente.setID(row[0])
            cliente.setUsuarioID(row[1])
            cliente.setNombre(row[2])
            cliente.setTelefono(row[3])
            cliente.setRFC(row[4])
            return cliente
        except:
            return None
        
    def getAll(self) -> list[Cliente]:
        try:
            self.cursor.execute("SELECT * FROM clientes")
            rows = self.cursor.fetchall()
            clientes = []
            for row in rows:
                c = Cliente()
                c.setID(row[0])
                c.setUsuarioID(row[1])
                c.setNombre(row[2])
                c.setTelefono(row[3])
                c.setRFC(row[4])
                clientes.append(c)
            return clientes
        except:
            return []
        
    def getUsuario(self, cliente: Cliente) -> User | None:
        dbuser = dbUser()
        user = User()
        user.setID(cliente.getUsuarioID())
        return dbuser.get(user)
        
    
    def getVehiculos(self, cliente: Cliente) -> list[Vehiculo]:
        dbvehiculo = dbVehiculo()
        vehiculo = Vehiculo()
        vehiculo.setClienteID(cliente.getID())
        return dbvehiculo.getVehiculosCliente(vehiculo)
    
        