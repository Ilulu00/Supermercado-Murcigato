from Producto import Producto
class Carrito:
    
    def __init__(self):
        self.productos = []
        self.total = 0
    
    def agregar_producto(self, producto: Producto) -> None: 
        self.productos.append(producto.codigo)
        self.total += producto.precio
        print(f"Se agrego el producto {producto.nombre} al carrito.")
    
    def quitar_producto(self, producto: Producto) -> None: 
        if producto in self.Productos:
            self.productos.remove(producto.codigo)
            self.total -= producto.precio
            print(f"Se quito el producto {producto.nombre} del carrito.")
        else:
            print(f"El producto {producto.nombre} no existe en el carrito.")
    
    def mostrar_carrito(self) -> None:
        print("====Carrito de Compras====")
        if not self.productos:
            print("Lo siento, no hay nada en tu carrito de compras.")
        else:
            for p in self.productos:  #For para iterar sobre los productos y mostrarlos
                print(f"- {Producto.nombre} -> ${Producto.percio}")
            print(f"Total: ${self.total}")
            