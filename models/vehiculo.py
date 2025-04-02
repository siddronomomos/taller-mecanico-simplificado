from dataclasses import dataclass
from typing import Optional

@dataclass
class Vehiculo:
    matricula: Optional[str] = None
    serie: Optional[str] = None
    modelo: Optional[str] = None
    marca: Optional[str] = None
    anio : Optional[int] = None
    cliente_id: Optional[int] = None
    
    def validate(self) -> bool:
        if not all([self.matricula, self.serie, self.modelo, self.marca, self.anio, self.cliente_id]):
            return False
        if len(self.matricula) not in (7, 8):
            return False
        return True
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.matricula}"