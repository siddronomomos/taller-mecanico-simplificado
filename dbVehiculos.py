from conection import Connection as con
from vehiculo import Vehiculo
from cliente import Cliente
class dbVehiculo:
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
    
    def save(self, vehiculo: Vehiculo) -> bool:
        try:
            self.cursor.execute("""
                INSERT INTO vehiculos (matricula, serie, modelo, marca, cliente_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (vehiculo.getMatricula(), vehiculo.getSerie(), vehiculo.getModelo(), vehiculo.getMarca(), vehiculo.getClienteID()))
            self.connection.commit()
        except:
            return False
        return True
    
    def update(self, vehiculo: Vehiculo) -> bool:
        try:
            self.cursor.execute("""
                UPDATE vehiculos
                SET serie = %s, modelo = %s, marca = %s, cliente_id = %s
                WHERE matricula = %s
            """, (vehiculo.getSerie(), vehiculo.getModelo(), vehiculo.getMarca(), vehiculo.getClienteID(), vehiculo.getMatricula()))
            self.connection.commit()
        except:
            return False
        return True
    
    def delete(self, vehiculo: Vehiculo) -> bool:
        try:
            self.cursor.execute("""
                DELETE FROM vehiculos
                WHERE matricula = %s
            """, (vehiculo.getMatricula(),))
            self.connection.commit()
        except:
            return False
        return True
    
    def get(self, vehiculo: Vehiculo) -> Vehiculo | None:
        try:
            self.cursor.execute("""
                SELECT * FROM vehiculos
                WHERE matricula = %s
            """, (vehiculo.getMatricula(),))
            row = self.cursor.fetchone()
            vehiculo.setMatricula(row[0])
            vehiculo.setSerie(row[1])
            vehiculo.setModelo(row[2])
            vehiculo.setMarca(row[3])
            vehiculo.setClienteID(row[4])
        except:
            return None
        return vehiculo
    
    def getAll(self) -> list[Vehiculo]:
        vehiculos = []
        self.cursor.execute("SELECT * FROM vehiculos")
        rows = self.cursor.fetchall()
        for row in rows:
            vehiculo = Vehiculo()
            vehiculo.setMatricula(row[0])
            vehiculo.setSerie(row[1])
            vehiculo.setModelo(row[2])
            vehiculo.setMarca(row[3])
            vehiculo.setClienteID(row[4])
            vehiculos.append(vehiculo)
        return vehiculos
    
    def getVehiculosCliente(self, cliente: Cliente) -> list[Vehiculo]:
        vehiculos = []
        self.cursor.execute("SELECT * FROM vehiculos WHERE cliente_id = %s", (cliente.getID(),))
        rows = self.cursor.fetchall()
        for row in rows:
            vehiculo = Vehiculo()
            vehiculo.setMatricula(row[0])
            vehiculo.setSerie(row[1])
            vehiculo.setModelo(row[2])
            vehiculo.setMarca(row[3])
            vehiculo.setClienteID(row[4])
            vehiculos.append(vehiculo)
        return vehiculos
    
    def getCliente(self, vehiculo: Vehiculo) -> Cliente | None:
        from dbClientes import dbCliente
        dbcliente = dbCliente()
        cliente = Cliente()
        cliente.setID(vehiculo.getClienteID())
        return dbcliente.get(cliente)