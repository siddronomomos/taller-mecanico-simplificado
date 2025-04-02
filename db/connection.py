import mysql.connector
from mysql.connector import Error
from typing import Optional
from config import Config

class Connection:
    _instance: Optional['Connection'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            # Primero conecta sin especificar la base de datos
            self.con = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            self.cursor = self.con.cursor(dictionary=True)
            
            # Crear la base de datos si no existe
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
            self.cursor.execute(f"USE {Config.DB_NAME}")
            
            # Luego crear las tablas
            self._create_tables()
        except Error as e:
            raise ConnectionError(f"Error al conectar a la base de datos: {e}")
    def _create_tables(self):
        tables = [
            """CREATE TABLE IF NOT EXISTS usuarios (
                usuario_id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(30) NOT NULL,
                user_name VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                perfil ENUM('admin', 'mecanico', 'aux') NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS clientes (
                cliente_id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                nombre VARCHAR(30) NOT NULL,
                telefono VARCHAR(10) NOT NULL,
                rfc VARCHAR(13) NOT NULL UNIQUE,
                fecha_registro DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
            )""",
            """CREATE TABLE IF NOT EXISTS vehiculos (
                matricula VARCHAR(10) PRIMARY KEY,
                serie VARCHAR(10) NOT NULL,
                modelo VARCHAR(20) NOT NULL,
                marca VARCHAR(20) NOT NULL,
                anio INT,
                cliente_id INT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
            )""",
            """CREATE TABLE IF NOT EXISTS piezas (
                pieza_id INT AUTO_INCREMENT PRIMARY KEY,
                descripcion VARCHAR(500) NOT NULL,
                existencias INT NOT NULL DEFAULT 0,
                precio DECIMAL(10,2) NOT NULL DEFAULT 0.00
            )""",
            """CREATE TABLE IF NOT EXISTS reparaciones (
                folio INT AUTO_INCREMENT PRIMARY KEY,
                matricula VARCHAR(10) NOT NULL,
                fecha_entrada DATE NOT NULL,
                fecha_salida DATE,
                estado ENUM('pendiente', 'en_proceso', 'completada') DEFAULT 'pendiente',
                FOREIGN KEY (matricula) REFERENCES vehiculos(matricula)
            )""",
            """CREATE TABLE IF NOT EXISTS detalle_reparaciones (
                detalle_id INT AUTO_INCREMENT PRIMARY KEY,
                folio INT NOT NULL,
                pieza_id INT NOT NULL,
                cantidad INT NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (folio) REFERENCES reparaciones(folio),
                FOREIGN KEY (pieza_id) REFERENCES piezas(pieza_id)
            )"""
        ]
        try:
            for table in tables:
                self.cursor.execute(table)
            self.con.commit()
        except Error as e:
            print(f"Error al crear tablas: {e}")
            self.con.rollback()
    
    def close(self):
        if hasattr(self, 'con') and self.con.is_connected():
            self.cursor.close()
            self.con.close()
    
    def commit(self):
        self.con.commit()
    
    def rollback(self):
        self.con.rollback()
    
    def __del__(self):
        self.close()