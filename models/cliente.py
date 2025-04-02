from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Cliente:
    cliente_id: Optional[int] = None
    usuario_id: Optional[int] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    rfc: Optional[str] = None
    fecha_registro: Optional[date] = None
    
    def validate(self) -> bool:
        """Valida los datos del cliente"""
        if not all([self.nombre, self.telefono, self.rfc]):
            return False
        if len(self.telefono) != 10 or not self.telefono.isdigit():
            return False
        if len(self.rfc) not in (12, 13):
            return False
        return True
    
    def __str__(self):
        return f"{self.nombre} ({self.rfc})"