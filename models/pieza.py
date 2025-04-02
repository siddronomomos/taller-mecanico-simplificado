from dataclasses import dataclass
from typing import Optional

@dataclass
class Pieza:
    pieza_id: Optional[int] = None
    descripcion: Optional[str] = None
    existencias: int = 0
    precio: float = 0.0
    
    def validate(self) -> bool:
        if not self.descripcion or len(self.descripcion) < 3:
            return False
        if self.existencias < 0:
            return False
        if self.precio < 0:
            return False
        return True
    
    def __str__(self):
        return f"{self.descripcion} - {self.existencias} unidades"