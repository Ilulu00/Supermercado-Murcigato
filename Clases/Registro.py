class Registro:
    
    def __init__(self, id_reg: int, nombre: str, apellido: str, direccion: str, correo:str, contraseña:str , estado: str = "Pendiente"): #Constructor para la clase registro
        self.id_reg = id_reg
        self.nombre = nombre
        self.apellido = apellido
        self.nombre = direccion
        self._correo = correo
        self._contraseña = contraseña 
        self.estado = "Pendiente" #En el estado, por defecto siempre estara en pendiente
        
    def Datos_Registro(self) -> None:
        self.nombre = str(input("Ingrese su nombre: "))
        self.apellido = str(input("Ingrese su apellido: "))
        self.direccion = str(input("Ingrese su direccion por favor: "))
        self._correo = str(input("Ingrese su correo electronico: "))
        self._contraseña = str(input("Ingrese la contraseña: "))
        
    def autenticador(self, correo: str, contraseña: str) -> str:
        return self.correo == correo and self._contraseña == contraseña #Verifica si el correo y la contraseña que digito el usuario es la que ingreso, la correcta 
    

        
