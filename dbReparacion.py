from conection import Connection as con
from reparacion import Reparacion

class dbReparacion:
    def __init__(self):
        self.connection = con()
        self.cursor = self.connection.open()
        if self.cursor is None:
            raise ConnectionError("Error al conectar con la base de datos")
    
    def save(self, reparacion: Reparacion) -> bool:
        try:
            self.cursor.execute(
                """
                INSERT INTO reparaciones (matricula, fecha_entrada, fecha_salida)
                VALUES (%s, %s, %s)
                """,
                (reparacion.getMatricula(), reparacion.getFechaEntrada(), reparacion.getFechaSalida())
            )
            self.connection.commit()
        except:
            return False
        return True
    
    def update(self, reparacion: Reparacion) -> bool:
        try:
            self.cursor.execute(
                """
                UPDATE reparaciones
                SET matricula = %s, fecha_entrada = %s, fecha_salida = %s
                WHERE folio = %s
                """,
                (reparacion.getMatricula(), reparacion.getFechaEntrada(), reparacion.getFechaSalida(), reparacion.getFolio())
            )
            self.connection.commit()
        except:
            return False
        return True
    
    def delete(self, reparacion: Reparacion) -> bool:
        try:
            self.cursor.execute("DELETE FROM reparaciones WHERE folio = %s", (reparacion.getFolio(),))
            self.connection.commit()
        except:
            return False
        return True
    
    def get(self, reparacion: Reparacion) -> Reparacion | None:
        try:
            self.cursor.execute("SELECT * FROM reparaciones WHERE folio = %s", (reparacion.getFolio(),))
            row = self.cursor.fetchone()
            if row:
                return Reparacion(row[0], row[1], row[2], row[3])
        except:
            return None
        return None
    
    def getAll(self) -> list[Reparacion]:
        try:
            self.cursor.execute("SELECT * FROM reparaciones")
            rows = self.cursor.fetchall()
            return [Reparacion(row[0], row[1], row[2], row[3]) for row in rows]
        except:
            return []
