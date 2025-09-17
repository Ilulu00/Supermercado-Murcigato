from Registro import Registro
from Pago import Pago
from Descuento import Descuento
from Carrito import Carrito

class Factura:
    def __init__(self, Regt: Registro, Pag: Pago, Desc: Descuento, carrito: Carrito):
        self.Registro = Regt
        self.Pago = Pag
        self.Descuento = Desc
        self.Carrito = carrito

    def mostrar_factura(self) -> None:
        print(f"Factura del cliente: {self.Registro.nombre} {self.Registro.apellido}")
        print("Productos: ")
        self.Carrito.mostrar_carrito()
        print(f"El metodo de pago es: {self.Pago.metodo_pago}")
        Totaldescuento = self.Carrito.total - self.Descuento.resultado()
        print(f"Total con descuento: ${Totaldescuento}")
    
    def guardar_factura(self) -> None:
        Totaldescuento = self.Carrito.total - self.Descuento.resultado()
        
        facturaTxt = []
        facturaTxt.append(f"Factura de: {self.Registro.nombre} {self.Registro.apellido}\n")
        facturaTxt.append("Productos:\n")
        self.Carrito.mostrar_carrito()
        facturaTxt.append(f"\nMetodo de pago utilizado: {self.Pago.metodo_pago}.\n")
        facturaTxt.append(f"Total sin descuento: {self.dinero_total}")
        facturaTxt.append(f"Descuento aplicado: {self.Descuento.resultado()}\n")
        facturaTxt.append(f"Total pagado: {Totaldescuento}")
        
        with open(f"factura_{self.Registro.nombre}_{self.Registro.apellido}.txt", "w", encoding="utf-8") as f:
            f.writelines(facturaTxt)
        print("Factura generada con exito.")
