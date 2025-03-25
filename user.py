
class User:
    def __init__(self):
        self.id = None
        self.nombre = None
        self.user_name = None
        self.password = None
        self.perfil = None

    def getID(self) -> int | None:
        return self.id
    
    def setID(self, id: int) -> bool:
        self.id = id
        return True

    def getNombre(self) -> str | None:
        return self.nombre
    
    def setNombre(self, nombre: str) -> bool:
        self.nombre = nombre
        return True
    
    def getUserName(self) -> str | None:
        return self.user_name
    
    def setUserName(self, user_name: str) -> bool:
        self.user_name = user_name
        return True
    
    def getPassword(self) -> str | None:
        return self.password
    
    def setPassword(self, password: str) -> bool:
        self.password = password
        return True
    
    def getPerfil(self) -> str | None:
        return self.perfil
    
    def setPerfil(self, perfil: str) -> bool:
        self.perfil = perfil
        return True
