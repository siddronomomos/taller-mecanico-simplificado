from conection import Connection as con
from pieza import Pieza

class dbPiezas:
    def __init__(self):
        self.connection = con()
        self.cursor = self.connection.open()
        if self.cursor is None:
            raise ConnectionError("Error al conectar con la base de datos")

    def save(self, pieza: Pieza) -> bool:
        try:
            self.cursor.execute("""
                INSERT INTO piezas (descripcion, existencias)
                VALUES (%s, %s)
            """, (pieza.getDescripcion(), pieza.getExistencias()))
            self.connection.commit()
        except:
            return False
        return True

    def update(self, pieza: Pieza) -> bool:
        try:
            self.cursor.execute("""
                UPDATE piezas
                SET descripcion = %s, existencias = %s
                WHERE pieza_id = %s
            """, (pieza.getDescripcion(), pieza.getExistencias(), pieza.getID()))
            self.connection.commit()
        except:
            return False
        return True

    def delete(self, pieza: Pieza) -> bool:
        try:
            self.cursor.execute("""
                DELETE FROM piezas
                WHERE pieza_id = %s
            """, (pieza.getID(),))
            self.connection.commit()
        except:
            return False
        return True

    def get(self, pieza: Pieza) -> Pieza | None:
        try:
            self.cursor.execute("""
                SELECT * FROM piezas
                WHERE pieza_id = %s
            """, (pieza.getID(),))
            row = self.cursor.fetchone()
            if row:
                pieza.setID(row[0])
                pieza.setDescripcion(row[1])
                pieza.setExistencias(row[2])
                return pieza
        except:
            return None
        return None

    def getAll(self) -> list[Pieza]:
        try:
            self.cursor.execute("SELECT * FROM piezas")
            rows = self.cursor.fetchall()
            piezas = []
            for row in rows:
                p = Pieza()
                p.setID(row[0])
                p.setDescripcion(row[1])
                p.setExistencias(row[2])
                piezas.append(p)
            return piezas
        except:
            return []
