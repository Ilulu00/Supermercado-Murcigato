from Registro import Registro
from Descuento import Descuento
class Pago:
    
    def __init__(self, metodo_pago: str, monto: float, Desc: Descuento, Regt: Registro):
        self.metodo_pago = metodo_pago
        self._monto = monto
        self.Descuento = Desc
        self.Registro = Regt
    
    def pagar(self):
        if self.metodo_pago == "efectivo": #si el metodo a utilizar es efectivo, entra por aqui y llama al metodo.
            return self._pagar_efectivo()
        elif self.metodo_pago == "tarjeta": #si el metodo a utilizar es tarjeta, entra por aqui y llama al metodo.
            return self._pagar_tarjeta()
        else:
            print("Método de pago no válido.")
            return False
    
    def _pagar_efectivo(self) -> bool: #Metod0 privado, para que solo se pueda acceder desde dentro de la clase
        Dinero = float(input(f"Total a pagar: {self._monto}. Por favor, ingrese el dinero: "))
        if Dinero >= self._monto: 
            Devuelta = Dinero - self._monto
            round(Devuelta, 2)
            print(f"Pago exitoso, devuelta: {Devuelta}. Gracias por su compra {self.Registro.nombre}" )
            return True
        else:
            print("Falta dinero, Por favor digite la cantidad adecuada.")
            return False #quiere decir que no se pudo completar el pago
    
    def _pagar_tarjeta(self) -> bool: #Metodo privado, para que solo se pueda acceder desde dentro de la clase
        num_tarjeta = input("Ingrese su numero de tarjeta: ")
        num_tarjeta = num_tarjeta.replace(" ", "").replace("-", "") #Limpia la tarjeta de espcios y guiones.
        if len(num_tarjeta) == 16 and num_tarjeta.isdigit():  #verifica si la tarjeta cumple con los requisitos de una tarjeta, que tanga 16 digitos y sea todo numeros.
             print(f"Pago de {self.monto} realizado con tarjeta {num_tarjeta[-4:]}. Gracias por su compra {self.Registro.nombre}")
             return True
        else:
            print("Tarjeta erronea. Intente de nuevo.")
            return False 
           
        
        
    
    
    
    
    
    
    #def Pagar(self, metodo_pago: str, Desc: float, monto: float, Regt: Registro)-> None:
        
        
         #print(f"Pago de {self.monto} realizado con {self.metodo}.")

        