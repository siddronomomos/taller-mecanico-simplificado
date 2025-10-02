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
    info_vehiculo: Optional[str] = None
    info_cliente: Optional[str] = None
    
    def validate(self) -> bool:
        """Valida que los campos obligatorios estén presentes y que las fechas sean lógicas."""
        if not all([self.matricula, self.fecha_entrada]):
            return False
        
        # La fecha de salida no puede ser anterior a la de entrada
        if self.fecha_salida and self.fecha_salida < self.fecha_entrada:
            raise ValueError("La fecha de salida no puede ser anterior a la fecha de entrada.")
            
        return True
    
    @property
    def dias_reparacion(self) -> int:
        if self.fecha_entrada and self.fecha_salida:
            return (self.fecha_salida - self.fecha_entrada).days
        return 0
    
    def __str__(self):
        return f"Rep #{self.folio} - {self.matricula}"