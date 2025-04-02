from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Reparacion:
    folio: Optional[int] = None
    matricula: Optional[str] = None
    fecha_entrada: Optional[date] = None
    fecha_salida: Optional[date] = None
    estado: str = "pendiente"
    
    def validate(self) -> bool:
        if not all([self.matricula, self.fecha_entrada]):
            return False
        if self.fecha_salida and self.fecha_salida < self.fecha_entrada:
            return False
        return True
    
    @property
    def dias_reparacion(self) -> int:
        if self.fecha_entrada and self.fecha_salida:
            return (self.fecha_salida - self.fecha_entrada).days
        return 0
    
    def __str__(self):
        return f"Rep #{self.folio} - {self.matricula}"