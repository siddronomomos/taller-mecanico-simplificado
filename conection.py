import mysql.connector
import mysql.connector.cursor

class Connection:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'taller_mecanico'
        self.con = None
        self.cursor = None
    
    def open(self) -> mysql.connector.cursor.MySQLCursor:
        try:
            self.con = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.con.cursor()
        except:
            exit("Error al conectar a la base de datos")
            return None
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.con.database = self.database
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(30) NOT NULL,
                user_name VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(30) NOT NULL,
                perfil VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cliente_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT(10) NOT NULL,
                nombre VARCHAR(30) NOT NULL,
                telefono VARCHAR(10) NOT NULL,
                rfc VARCHAR(13) NOT NULL UNIQUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                matricula VARCHAR(10) NOT NULL PRIMARY KEY,
                serie VARCHAR(10) NOT NULL,
                modelo VARCHAR(20) NOT NULL,
                marca VARCHAR(20) NOT NULL,
                cliente_id INT(10) NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reparaciones (
                folio INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                matricula VARCHAR(10) NOT NULL,
                fecha_entrada VARCHAR(10) NOT NULL,
                fecha_salida VARCHAR(10) NOT NULL,
                FOREIGN KEY (matricula) REFERENCES vehiculos(matricula) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS piezas (
                pieza_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                descripcion VARCHAR(500) NOT NULL,
                existencias INT(10) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS det_rep_pieza (
                det_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                folio INT(10) NOT NULL,
                pieza_id INT(10) NOT NULL,
                cantidad INT(10) NOT NULL,
                FOREIGN KEY (folio) REFERENCES reparaciones(folio) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (pieza_id) REFERENCES piezas(pieza_id) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        
        return self.cursor
    
    def close(self):
        self.cursor.close()
        self.con.close()
        return True
    
    def commit(self):
        self.con.commit()
        return True
    
    def rollback(self):
        self.con.rollback()
        return True