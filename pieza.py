class Pieza:
    def __init__(self, pieza_id=None, descripcion="", existencias=0):
        self.pieza_id = pieza_id
        self.descripcion = descripcion
        self.existencias = existencias
    
    def getID(self):
        return self.pieza_id
    
    def setID(self, pieza_id):
        self.pieza_id = pieza_id
    
    def getDescripcion(self):
        return self.descripcion
    
    def setDescripcion(self, descripcion):
        self.descripcion = descripcion
    
    def getExistencias(self):
        return self.existencias
    
    def setExistencias(self, existencias):
        self.existencias = existencias
