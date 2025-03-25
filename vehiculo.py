class Vehiculo:
    def __init__(self):
        self.matricula = None
        self.serie = None
        self.modelo = None
        self.marca = None
        self.cliente_id = None
    
    def getMatricula(self) -> str | None:
        return self.matricula
    
    def setMatricula(self, matricula: str) -> bool:
        self.matricula = matricula
        return True
    
    def getSerie(self) -> str | None:
        return self.serie
    
    def setSerie(self, serie: str) -> bool:
        self.serie = serie
        return True
    
    def getModelo(self) -> str | None:
        return self.modelo
    
    def setModelo(self, modelo: str) -> bool:
        self.modelo = modelo
        return True
    
    def getMarca(self) -> str | None:
        return self.marca
    
    def setMarca(self, marca: str) -> bool:
        self.marca = marca
        return True
    
    def getClienteID(self) -> int | None:
        return self.cliente_id
    
    def setClienteID(self, cliente_id: int) -> bool:
        self.cliente_id = cliente_id
        return True