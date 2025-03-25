class Cliente:
    def __init__(self):
        self.cliente_id = None
        self.usuario_id = None
        self.nombre = None
        self.telefono = None
        self.rfc = None

    def setID(self, cliente_id: int) -> bool:
        self.cliente_id = cliente_id
        return True
    
    def getID(self) -> int | None:
        return self.cliente_id
    
    def setUsuarioID(self, usuario_id: int) -> bool:
        self.usuario_id = usuario_id
        return True
    
    def getUsuarioID(self) -> int | None:
        return self.usuario_id
    
    def setNombre(self, nombre: str) -> bool:
        self.nombre = nombre
        return True
    
    def getNombre(self) -> str | None:
        return self.nombre
    
    def setTelefono(self, telefono: str) -> bool:
        self.telefono = telefono
        return True
    
    def getTelefono(self) -> str | None:
        return self.telefono
    
    def setRFC(self, rfc: str) -> bool:
        self.rfc = rfc
        return True
    
    def getRFC(self) -> str | None:
        return self.rfc
