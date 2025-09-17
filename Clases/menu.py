from Producto import *  
from Carrito import Carrito
from Pago import Pago
from Factura import Factura
from Descuento import Descuento
from Registro import Registro

mi_carrito = Carrito()
mi_descuento = Descuento()


def buscar_producto_por_codigo_txt(codigo: int):
    archivos = {
        "Fruta": Fruta,
        "Verdura": Verdura,
        "Carne": Carne,
        "Limpieza": Limpieza
    }
    
    for nombre_archivo, clase in archivos.items():
        archivo_txt = nombre_archivo + ".txt"
        if archivo_vacio(archivo_txt):
            continue
        with open(archivo_txt, "r") as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith(f"Código: {codigo}"):
                    partes = linea.split(", ")
                    cod = int(partes[0].split(": ")[1])
                    nombre = partes[1].split(": ")[1]
                    precio = float(partes[2].split(": ")[1])
                    stock = int(partes[3].split(": ")[1])
                    
                    if clase == Fruta:
                        vitaminas = partes[4].split(": ")[1]
                        return Fruta(cod, nombre, precio, stock, vitaminas)
                    elif clase == Verdura:
                        conservacion = partes[4].split(": ")[1]
                        return Verdura(cod, nombre, precio, stock, conservacion)
                    elif clase == Carne:
                        animal = partes[4].split(": ")[1]
                        return Carne(cod, nombre, precio, stock, animal)
                    elif clase == Limpieza:
                        descripcion = partes[4].split(": ")[1]
                        return Limpieza(cod, nombre, precio, stock, descripcion)
    return None

def menu_principal():
    while True:
        print("°°°°°Bienvenido a supermercado Mariana y Santiago°°°°°")
        print("1.Ingresar como cliente")
        print("2.Ingresar como administrador")
        print("0.Salir")

        op:int = int(input("Ingrese la opción deseada: "))

        if(op == 1):
            menu_cliente()
        elif(op == 2):
            usuario:str = input("Ingrese su usuario: ")
            contraseña:str = input("Ingrese su contraseña: ")
            autenticacion = autenticador(usuario,contraseña)

            if(autenticacion == True):
                menu_admin()
            else:
                print("Error, usted no es admin") 
                break   
              
        elif(op == 0):
            print("Hasta luego")
            break
        else:
            print("Opción no válida, intente de nuevo") 

def menu_cliente():
    while True:
        print("")
        print("-----Menú clientes-----")
        print("1. Todos los productos.")
        print("2. Frutas.")
        print("3. Verduras.")
        print("4. Carnes.")
        print("5. Limpieza.")
        print("6. Ver el Carrito.")
        print("7. Pagar.")
        print("0.Salir")
        print("")

        opC:int = int(input("Ingrese la opción deseada: "))   

        if(opC == 1):
            print("")
            verInventario("Fruta", "Verdura", "Carne", "Limpieza")
        elif(opC == 2):
            print("")
            verFruta("Fruta.txt")  
        elif(opC == 3):
            print("")
            verVerdura("Verdura.txt")    
        elif(opC == 4):
            print("")
            verCarnes("Carne.txt")   
        elif(opC == 5):
            print("")
            verLimpio("Limpieza.txt") 
        elif(opC == 6):
            print("")
            menu_carrito()
        elif(opC == 7):
            print("")
            menu_Facturacion()
            
            
            
        elif(opC == 0):
            print("")
            print("Hasta luego")
            break    
        else:
            print("")
            ("Opción no válida, intente de nuevo")              

def menu_admin():
    while True:
        print("")
        print("-----Menú adiministrador-----")
        print("1.Inventario")            
        print("2.Agregar producto")            
        print("3.Eliminar producto")            
        print("4.Modificar producto")       
        print("0.Salir")
        print("")

        opA:int = int(input("Ingrese la opción deseada: "))     

        if(opA == 1):
            print("")
            verInventario("Fruta", "Verdura", "Carne", "Limpieza")

        elif(opA == 2):
            opU = menu_productos()
            if(opU == 1):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                nombre:str = input("Ingrese el nombre del produto: ")
                precio:float = float(input("Ingrese el precio del producto: "))
                stock:int = int(input("Ingrese el stock del producto: "))
                vitaminas:str = input("Ingrese las vitaminas que contiene: ")
                Fruta.nueva_fruta(codigo,nombre,precio,stock,vitaminas)
                print("")
            elif(opU == 2):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                nombre:str = input("Ingrese el nombre del produto: ")
                precio:float = float(input("Ingrese el precio del producto: "))
                stock:int = int(input("Ingrese el stock del producto: "))
                conservacion:str = input("Ingrese el metodo de conservación: ")
                print("")
                Verdura.nueva_verdura(codigo,nombre,precio,stock,conservacion)
            elif(opU == 3):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                nombre:str = input("Ingrese el nombre del produto: ")
                precio:float = float(input("Ingrese el precio del producto: "))
                stock:int = int(input("Ingrese el stock del producto: "))
                animal:str = input("Ingrese el animal de donde proviene: ")
                print("")
                Carne.nueva_carne(codigo,nombre,precio,stock,animal)
            elif(opU == 4):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                nombre:str = input("Ingrese el nombre del produto: ")
                precio:float = float(input("Ingrese el precio del producto: "))
                stock:int = int(input("Ingrese el stock del producto: "))
                descripcion:str = input("Ingrese la descripción: ")
                print("")
                Limpieza.nuevo_limpieza(codigo,nombre,precio,stock,descripcion)
            elif(opU == 0):
                print("")
                print("Hasta luego")
                print("")
                break 
            else:
                print("")
                print("Opción no válida, intente de nuevo")     
                print("")

        elif(opA == 3):
            opU = menu_productos()
            if(opU == 1):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                Fruta.eliminar_fruta(codigo)
            elif(opU == 2):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                Verdura.eliminar_verdura(codigo)    
            elif(opU == 3):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                Carne.eliminar_carne(codigo)    
            elif(opU == 4):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                Limpieza.eliminar_limpieza(codigo)    
            elif(opU == 0):
                print("")
                print("Hasta luego")
                print("")
                break
            else:
                print("")
                print("Opción no válida, intente de nuevo")  
                print("")  

        elif(opA == 4):
            opU:int = menu_productos()
            if(opU == 1):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                campoCambiar:str = input("Ingrese el campo del valor a cambiar (nombre, precio, stock, vitaminas): ")
                Nvalor = input("Ingrese el nuevo valor: ")
                print("")
                Fruta.actualizar_fruta(codigo,campoCambiar,Nvalor)
            elif(opU == 2):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                campoCambiar:str = input("Ingrese el campo del valor a cambiar (nombre, precio, stock, conservacion): ")
                Nvalor = input("Ingrese el nuevo valor: ")
                print("")
                Verdura.actualizar_verdura(codigo,campoCambiar,Nvalor)   
            elif(opU == 3):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                campoCambiar:str = input("Ingrese el campo del valor a cambiar: (nombre, precio, stock, animalProviene): ")
                Nvalor = input("Ingrese el nuevo valor: ")
                print("")
                Carne.actualizar_carne(codigo,campoCambiar,Nvalor)  
            elif(opU == 4):
                print("")
                codigo:int = int(input("Ingrese el código del producto: "))
                campoCambiar:str = input("Ingrese el campo del valor a cambiar: (nombre, precio, stock, descripcion): ")
                Nvalor = input("Ingrese el nuevo valor: ")
                print("")
                Limpieza.actualizar_Limpieza(codigo,campoCambiar,Nvalor)   
            elif(opU == 0):
                print("")
                print("Hasta luego")
                print("")
                break
            else:
                print("")
                print("Opción no válida, intente de nuevo")    
                print("") 
        elif(opA == 0):
            print("")
            print("Hasta luego")
            print("")
            break
        else:
            print("")
            print("Opción no válida, intente de nuevo")
            print("")

def menu_productos() -> int:
    print("")
    print("1.Frutas")
    print("2.Verduras")
    print("3.Carnes")
    print("4.Limpieza")
    print("0.Salir")
    print("")

    opP:int = int(input("Ingrese la opción deseada: "))   
    print("")

    return opP

def autenticador(user: str, contraseña: str) -> bool:
    with open("Admin.txt", "r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            usuario_archivo, contraseña_archivo = linea.split(",")
            
            if user == usuario_archivo and contraseña == contraseña_archivo:
                return True
    return False


def menu_carrito():
    print("====Tu carrito====")
    print("1. Agregar un producto a tu carrito. ")
    print("2. Ver tu carrito: ")
    print("3. Quitar un producto de tu carrito.")
    
    try:
        opMC = int(input("Ingrese la opción deseada: "))
    except ValueError:
            print("Por favor, ingrese una opcion valida..")

    if(opMC == 1):
            codigo = int(input("Ingrese el código del producto a agregar: "))
            producto = buscar_producto_por_codigo_txt(codigo)
            if producto:
                mi_carrito.agregar_producto(producto)
                print(f"{producto.nombre} agregado al carrito!")
            else:
                print("Producto no encontrado.")
                
    elif(opMC == 2):
            mi_carrito.mostrar_carrito()
            
    elif(opMC == 3):
            codigo = int(input("Ingrese el código del producto a quitar: "))
            producto = buscar_producto_por_codigo_txt(codigo)
            if producto:
                mi_carrito.quitar_producto(producto)
                print(f"{producto.nombre} removido del carrito!")
            else:
                print("Producto no encontrado.")
    else:
        print("Opción no válida.")

def menu_Facturacion():
    print("====Facturación====")
    print("1. Metodo de pago a utilizar y factura.")
    
    try:
        opMF = int(input("Ingrese la opcion a mostrar: "))
    except ValueError:
        print("Por favor, ingrese una opcion valida.")    
    
    if(opMF == 1):
         if mi_carrito.total == 0:
            print("El carrito está vacío.")
         else:
            print("===Mi carrito===")
            mi_carrito.mostrar_carrito()
            
            total_con_descuento = mi_descuento.aplicar_descuento(mi_carrito.total)
            print(f"Total a pagar con descuento aplicado: {total_con_descuento}")
            
            metodo = input("Ingrese método de pago (efectivo/tarjeta): ")
            mi_metodo_pago = Pago(metodo_pago=metodo, monto=mi_carrito.total, Desc=mi_descuento, Regt=mi_registro)
            Pag = mi_metodo_pago.pagar()
            if Pag:
                mi_factura = Factura(Regt=mi_registro, Pag=mi_metodo_pago, Desc=mi_descuento, carrito=mi_carrito)
                mi_factura.mostrar_factura()
                mi_factura.guardar_factura()
            else:
                print("No se pudo realizar el pago, por ende no se puede generar una factura.")
    else:
        print("Opción no válida.")
        
    
    
    

menu_principal() 