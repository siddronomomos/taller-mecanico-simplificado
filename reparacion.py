class Reparacion:
    def __init__(self, folio=None, matricula=None, fecha_entrada=None, fecha_salida=None):
        self.folio = folio
        self.matricula = matricula
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
    
    def getFolio(self):
        return self.folio
    
    def setFolio(self, folio):
        self.folio = folio
    
    def getMatricula(self):
        return self.matricula
    
    def setMatricula(self, matricula):
        self.matricula = matricula
    
    def getFechaEntrada(self):
        return self.fecha_entrada
    
    def setFechaEntrada(self, fecha_entrada):
        self.fecha_entrada = fecha_entrada
    
    def getFechaSalida(self):
        return self.fecha_salida
    
    def setFechaSalida(self, fecha_salida):
        self.fecha_salida = fecha_salida
