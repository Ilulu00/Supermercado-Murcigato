class Producto:
    def __init__(self,codigo:int,nombre:str,precio:float,stock:int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock#

class Fruta(Producto):
    def __init__(self,codigo:int,nombre:str,precio:float,stock:int,vitaminas:str):
        super().__init__(codigo,nombre,precio,stock)
        self.vitaminas = vitaminas

    def __str__(self):
        return (f"Código: {self.codigo}, Nombre: {self.nombre}, Precio: {self.precio}, Stock: {self.stock}, Vitaminas: {self.vitaminas}")
    
    @staticmethod #Para que permita guardar la nueva fruta de manera automática en el archivo
    def nueva_fruta(codigo:int,nombre:str,precio:float,stock:int,vitaminas:str):
        NFruta = Fruta(codigo,nombre,precio,stock,vitaminas)

        with open("Fruta.txt","a") as archivo: #La a es de append (agrega la nueva información al final)
            archivo.write (str(NFruta) + "\n")

            print (f"Nueva fruta: {NFruta}")

    @staticmethod
    def eliminar_fruta(codigo:int):
        vacio:bool = archivo_vacio("Fruta.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Fruta.txt","r") as archivo: #La r es de read (para que lea y guarde en la variable lineas)
                lineas = archivo.readlines()        

            with open("Fruta.txt", "w") as archivo:
                codigoEncontrado:bool = False
                for linea in lineas:
                    if linea.startswith(str(codigo) + " "):
                        codigoEncontrado = True
                        continue #Hace que cuando se encuentra la línea salte a la siguiente iteración sin escribir la línea con el código
                    archivo.write (linea)

        if (codigoEncontrado == True):
            print(f"La fruta con código: {codigo} ha sido eliminada de manera exitosa")
        else:
            print(f"La fruta con código: {codigo} no fue encontrada")

           

    @staticmethod
    def actualizar_fruta(codigo:int,campoCambiar:str,Nvalor): #Nvalor no esta especificado porque en una fruta hay distintos tipos de datos
        vacio:bool = archivo_vacio("Fruta.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Fruta.txt","r") as archivo:
                lineas = archivo.readlines()        

        with open("Fruta.txt", "w") as archivo:
            codigoEncontrado:bool = False
            for linea in lineas:
                if linea.startswith(str(codigo) + " "):
                    frutaVieja = linea.strip().split(" - ") #El strip quita espcios antes y después de los datos, split pone - para diferecniar datos
                    
                    if(campoCambiar == "nombre"): #Van con comillas porque en el .txt se vuelven todos str
                        frutaVieja[1] = Nvalor
                    elif(campoCambiar == "precio"):
                        frutaVieja[2] = str(float(Nvalor))#Debe quedar en str para poder usar .join    
                    elif(campoCambiar == "stock"):
                        frutaVieja[3] = str(int(Nvalor))    
                    elif(campoCambiar == "vitaminas"):
                        frutaVieja[4] = Nvalor

                    linea = (" - ".join(frutaVieja) + "\n") #El join hace que cada dato quede separado por un -
                    codigoEncontrado = True        

                archivo.write(linea)  

        if codigoEncontrado:
            print(f"La fruta con código: {codigo} ha sido actualizada con éxito")
        else:
            print(f"La fruta con código: {codigo} no fue encontrada")           

class Verdura(Producto):
    def __init__(self,codigo:int,nombre:str,precio:float,stock:int,conservacion:str):
        super().__init__(codigo,nombre,precio,stock)
        self.conservacion = conservacion

    def __str__(self):
        return (f"Código: {self.codigo}, Nombre: {self.nombre}, Precio: {self.precio}, Stock: {self.stock}, Conservación: {self.conservacion}")
    
    @staticmethod
    def nueva_verdura(codigo:int,nombre:str,precio:float,stock,conservacion:str):
        Nverdura = Verdura(codigo,nombre,precio,stock,conservacion)

        with open("Verdura.txt","a") as archivo: #La a es de append (agrega la nueva información al final)
            archivo.write (str(Nverdura) + "\n")

            print (f"Nueva verdura: {Nverdura}")

    @staticmethod
    def eliminar_verdura(codigo:int):
        vacio:bool = archivo_vacio("Verdura.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Verdura.txt","r") as archivo: #La r es de read (para que lea y guarde en la variable lineas)
                lineas = archivo.readlines()        

            with open("Verdura.txt", "w") as archivo:
                codigoEncontrado:bool = False
                for linea in lineas:
                    if linea.startswith(str(codigo) + " "):
                        codigoEncontrado = True
                        continue #Hace que cuando se encuentra la línea salte a la siguiente iteración sin escribir la línea con el código
                    archivo.write (linea)

        if (codigoEncontrado == True):
            print(f"La verdura con código: {codigo} ha sido eliminada de manera exitosa")
        else:
            print(f"La verdura con código: {codigo} no fue encontrada")   

    @staticmethod
    def actualizar_verdura(codigo:int,campoCambiar:str,Nvalor): #Nvalor no esta especificado porque en una fruta hay distintos tipos de datos
        vacio:bool = archivo_vacio("Verdura.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Verdura.txt","r") as archivo:
                lineas = archivo.readlines()        

        with open("Verdura.txt", "w") as archivo:
            codigoEncontrado:bool = False
            for linea in lineas:
                if linea.startswith(str(codigo) + " "):
                    verduraVieja = linea.strip().split(" - ") #El strip quita espcios antes y después de los datos, split pone - para diferecniar datos
                    
                    if(campoCambiar == "nombre"): #Van con comillas porque en el .txt se vuelven todos str
                        verduraVieja[1] = Nvalor
                    elif(campoCambiar == "precio"):
                        verduraVieja[2] = str(float(Nvalor))#Debe quedar en str para poder usar .join    
                    elif(campoCambiar == "stock"):
                        verduraVieja[3] = str(int(Nvalor))    
                    elif(campoCambiar == "conservacion"):
                        verduraVieja[4] = Nvalor

                    linea = (" - ".join(verduraVieja) + "\n") #El join hace que cada dato quede separado por un -
                    codigoEncontrado = True        

                archivo.write(linea)  

        if codigoEncontrado:
            print(f"La verdura con código: {codigo} ha sido actualizada con éxito")
        else:
            print(f"La verdura con código: {codigo} no fue encontrada")    

class Carne(Producto):
    def __init__(self,codigo:int,nombre:str,precio:float,stock:int,animalProviene:str):
        super().__init__(codigo,nombre,precio,stock)
        self.animalProviene = animalProviene

    def __str__(self):
        return (f"Código: {self.codigo}, Nombre: {self.nombre}, Precio: {self.precio}, Stock: {self.stock}, Animal de procedencia: {self.animalProviene}")
    
    @staticmethod
    def nueva_carne(codigo:int,nombre:str,precio:float,stock:int,animalProviene:str):
        Ncarne = Carne(codigo,nombre,precio,stock,animalProviene)

        with open("Carne.txt","a") as archivo: #La a es de append (agrega la nueva información al final)
            archivo.write (str(Ncarne) + "\n")

            print (f"Nueva carne: {Ncarne}")

    @staticmethod
    def eliminar_carne(codigo:int):
        vacio:bool = archivo_vacio("Carne.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Carne.txt","r") as archivo: #La r es de read (para que lea y guarde en la variable lineas)
                lineas = archivo.readlines()        

            with open("Carne.txt", "w") as archivo:
                codigoEncontrado:bool = False
                for linea in lineas:
                    if linea.startswith(str(codigo) + " "):
                        codigoEncontrado = True
                        continue #Hace que cuando se encuentra la línea salte a la siguiente iteración sin escribir la línea con el código
                    archivo.write (linea)

        if (codigoEncontrado == True):
            print(f"La carne con código: {codigo} ha sido eliminada de manera exitosa")
        else:
            print(f"La carne con código: {codigo} no fue encontrada")   

    @staticmethod
    def actualizar_carne(codigo:int,campoCambiar:str,Nvalor):
        vacio:bool = archivo_vacio("Carne.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Carne.txt","r") as archivo:
                lineas = archivo.readlines()        

        with open("Carne.txt", "w") as archivo:
            codigoEncontrado:bool = False
            for linea in lineas: #Busca el código
                if linea.startswith(str(codigo) + " "):
                    carneVieja = linea.strip().split(" - ") #El strip quita espcios antes y después de los datos, split pone - para diferecniar datos
                    
                    if(campoCambiar == "nombre"): #Van con comillas porque en el .txt se vuelven todos str
                        carneVieja[1] = Nvalor
                    elif(campoCambiar == "precio"):
                        carneVieja[2] = str(float(Nvalor))#Debe quedar en str para poder usar .join    
                    elif(campoCambiar == "stock"):
                        carneVieja[3] = str(int(Nvalor))    
                    elif(campoCambiar == "animalProviene"):
                        carneVieja[4] = Nvalor

                    linea = (" - ".join(carneVieja) + "\n") #El join hace que cada dato quede separado por un -
                    codigoEncontrado = True        

                archivo.write(linea)  

        if codigoEncontrado:
            print(f"La carne con código: {codigo} ha sido actualizada con éxito")
        else:
            print(f"La carne con código: {codigo} no fue encontrada")
            
class Limpieza(Producto):
    def __init__(self,codigo:int,nombre:str,precio:float,stock:int,descripcion:str):
        super().__init__(codigo,nombre,precio,stock)
        self.descripcion = descripcion

    def __str__(self):
        return (f"Código: {self.codigo}, Nombre: {self.nombre}, Precio: {self.precio}, Stock: {self.stock}, Descripción: {self.descripcion}")
    
    @staticmethod
    def nuevo_limpieza(codigo:int,nombre:str,precio:float,stock:int,descripcion:str):
        Nlimpieza = Limpieza(codigo,nombre,precio,stock,descripcion)

        with open("Limpieza.txt","a") as archivo: #La a es de append (agrega la nueva información al final)
            archivo.write (str(Nlimpieza) + "\n")

            print (f"Nuevo producto de limpieza: {Nlimpieza}")

    @staticmethod
    def eliminar_limpieza(codigo:int):
        vacio:bool = archivo_vacio("Limpieza.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Limpieza.txt","r") as archivo: #La r es de read (para que lea y guarde en la variable lineas)
                lineas = archivo.readlines()        

            with open("Limpieza.txt", "w") as archivo:
                codigoEncontrado:bool = False
                for linea in lineas:
                    if linea.startswith(str(codigo) + " "):
                        codigoEncontrado = True
                        continue #Hace que cuando se encuentra la línea salte a la siguiente iteración sin escribir la línea con el código
                    archivo.write (linea)

        if (codigoEncontrado == True):
            print(f"El producto de limpieza con código: {codigo} ha sido eliminado de manera exitosa")
        else:
            print(f"El producto de limpieza con código: {codigo} no fue encontrado")   

    @staticmethod
    def actualizar_Limpieza(codigo:int,campoCambiar:str,Nvalor):
        vacio:bool = archivo_vacio("Limpieza.txt")
        if(vacio):
            print("El archivo no cuenta con ningun producto")
            return
        else:
            with open("Limpieza.txt","r") as archivo:
                lineas = archivo.readlines()        

        with open("Limpieza.txt", "w") as archivo:
            codigoEncontrado:bool = False
            for linea in lineas: #Busca el código
                if linea.startswith(str(codigo) + " "):
                    limpioViejo = linea.strip().split(" - ") #El strip quita espcios antes y después de los datos, split pone - para diferecniar datos
                    
                    if(campoCambiar == "nombre"): #Van con comillas porque en el .txt se vuelven todos str
                        limpioViejo[1] = Nvalor
                    elif(campoCambiar == "precio"):
                        limpioViejo[2] = str(float(Nvalor))#Debe quedar en str para poder usar .join    
                    elif(campoCambiar == "stock"):
                        limpioViejo[3] = str(int(Nvalor))    
                    elif(campoCambiar == "descripcion"):
                        limpioViejo[4] = Nvalor

                    linea = (" - ".join(limpioViejo) + "\n") #El join hace que cada dato quede separado por un -
                    codigoEncontrado = True        

                archivo.write(linea)  

        if codigoEncontrado:
            print(f"El objeto de limpieza con código: {codigo} ha sido actualizado con éxito")
        else:
            print(f"El objeto de limpieza con código: {codigo} no fue encontrado")   

def archivo_vacio(nombre_archivo)->bool:
     with open(nombre_archivo,"r") as archivo:
            lineas = archivo.readlines()        

            cont:int = 0
            for linea in lineas:
                cont = cont + 1
            if(cont == 0):
                return True    
            else:
                return False

def verFruta(fruta:str):
    vacio:bool = archivo_vacio(fruta)
    if(vacio):
        print("No hay productos en esta sección")
    else:
        with open(fruta, "r") as archivoF:
            print("°^° Frutas °^°")
            print(archivoF.read())  

def verVerdura(verdura:str):
    vacio:bool = archivo_vacio(verdura)
    if(vacio):
        print("No hay productos en esta sección")
    else:
        with open(verdura, "r") as archivoV:
            print("°^° Verduras °^°")
            print(archivoV.read())  

def verCarnes(carne:str):
    vacio:bool = archivo_vacio(carne)
    if(vacio):
        print("No hay productos en esta sección")
    else:
        with open(carne, "r") as archivoC:
            print("°^° Carne °^°")
            print(archivoC.read())  

def verLimpio(limpio:str):
    vacio:bool = archivo_vacio(limpio)
    if(vacio):
        print("No hay productos en esta sección")
    else:
        with open(limpio, "r") as archivoL:
            print("°^° Limpieza °^°")
            print(archivoL.read()) 

def verInventario(fruta:str, verdura:str, carne:str, limpieza:str):
    verFruta(fruta + ".txt")
    verVerdura(verdura + ".txt")
    verCarnes(carne + ".txt")
    verLimpio(limpieza + ".txt")             