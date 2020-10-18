#importamos nuestro nuestra libreria Pathlib y nuestros archivos .py 
from pathlib import Path    
import prodCol
import ventCol
import vendCol
#--------------------------------------------------------------------------------------------
#Sirve para cargar nuestros archivos y devolvernos una matriz con el contenido del archivo
def load_products(fileName):
    productos_file = open( Path.cwd() / fileName)
    productos = productos_file.readlines()[1:]
    productos_file.close()

    matriz_productos = []

    for producto in productos:
        producto = producto.strip()
        matriz_productos.append(producto.split(","))
    
    return matriz_productos

#-------------------------------------------------------------------------------------------------
#Esta variable guarda todos nuestros archivos una vez que los manipulamos

def guardar_datos(productos, vendedores, ventas):
    archivos= ["Productos(prueba3).csv","Vendedores(prueba3).csv", "Ventas(prueba3).csv"]
    for i in range(3):
        if i == 0:
            string = prodCol.NAMES + "\n"
            matriz = productos
        elif i == 1:
            string = vendCol.NAMES + "\n" 
            matriz = vendedores
        else:
            string = ventCol.NAMES + "\n"
            matriz = ventas
    
        for fila in matriz:
            for columna in fila:
                string = string + str(columna) + ","
            string = string [:-1] + "\n"
            
        string = string [:-1]
        
        item_archivos = open (Path.cwd() / archivos[i], 'w')
        item_archivos.write(string)
        item_archivos.close()
#------------------------------------------------------------------------------------------------------        
#Esta función nos ayuda a imprimir nuestra matriz ordenada con tabulaciones específicas 

def print_matriz(matriz):
    bigger_size = []
    biggest = 0
    for columna in range(len(matriz[0])):
        for fila in range(len(matriz)):
            if len(matriz[fila][columna]) > biggest:
                biggest = len(matriz[fila][columna])
        bigger_size.append(biggest)
        biggest = 0
        
    for fila in matriz:
        for columna, value in enumerate(fila):
            print(value.ljust(bigger_size[columna] + 3), end = "")
        print()
                           
#----------------------------------------------------------------------------------------------                           
#obtiene un dato dándole como entrada una lista y una columnas, para que te retorne dicho valor                         
def obten_atributo(objeto, columna):
    return objeto[columna]
#----------------------------------------------------------------------------------------------
#Esta función sirve para "filtrar" los datos que tu quieres, dandoles como entrada una matriz
# y una columna de algun archivo importado

def obten_todo(objetos, columna):
    result = []
    for objeto in objetos:
        if columna == prodCol.NOMBRE or columna == vendCol.NOMBRE:
            result.append(objeto[columna].upper())
        else:
            result.append(objeto[columna])
    return result

#---------------------------------------------------------------------------------------------
#Esta función filtra lo filtrado, se le da como entrada una matriz, una columna declaradas en nuestros archivos.py
# y por último un valor específico el cuál va a buscar 


def obten_objetos(objetos, columna, valor):
    result = []
    if columna == prodCol.NOMBRE or columna == vendCol.NOMBRE:
        valor = valor.upper()
    valores = obten_todo(objetos, columna)
    if valor in valores:
        for indx, value in enumerate(valores):
            if value == valor:
                result.append(objetos[indx])
    return result
#------------------------------------------------------------------------------------------------
#Esta función nos ayuda a actualizar todo lo manipulado en nuentra opción 1 del menú 
def actualizar_venta(ventas,producto_id,vendedor_id, cantidad):
    for indx, fila in enumerate(ventas):
        if int(fila[ventCol.VENDEDOR_ID]) == vendedor_id and \
           int(fila[ventCol.PRODUCTO_ID]) == producto_id:
            ventas[indx][ventCol.CANTIDAD] = int(ventas[indx][ventCol.CANTIDAD]) + cantidad
            break
# -------------------------------------------------------------------------------------------------
#Esta función nos ayuda a llevar a cabo el registro de las ventas que estan en nuestra opción 1 del menú

def registar_ventas(productos, vendedores,ventas):
    print("Nombre del vendedor")
    nombre_vendedor = input()
    print("¿Cuál es el producto?")
    nombre_producto = input()
    print("Unidades")
    cantidad = int(input())
    
    producto = obten_objetos(productos, prodCol.NOMBRE, nombre_producto)[0]
    if int(obten_atributo(producto, prodCol.EXISTENCIA)) < cantidad:
        print(f"No es posible completar la venta")
        print(f"""Solo tenemos {producto[prodCol.EXISTENCIA]} {producto[prodCol.NOMBRE]} en el almacen.
¡El próximo martes llegarán las {producto[prodCol.NOMBRE]} que necesita!""")
    else:
        product_id =int(obten_atributo(producto, prodCol.PRODUCTO_ID))
        productos[product_id][prodCol.EXISTENCIA] = (
            int(productos[product_id][prodCol.EXISTENCIA]) - cantidad)
        vendedor = obten_objetos(vendedores, vendCol.NOMBRE,nombre_vendedor)[0]
        vendedor_id = int(obten_atributo(vendedor, vendCol.VENDEDOR_ID))
        actualizar_venta(ventas, product_id, vendedor_id, cantidad)
        print("!La venta fue registrada exitosamente, vuelva pronto!")
#-----------------------------------------------------------------------------------------------------
#Esta función nos permite saber la cantidad de un producto específico vendido por cierto vendedor 

def Consultar_datos_ventas(productos, vendedores, ventas):
    print("¿Cuál es el nombre del vendedor")
    nombre_vendedor = input()
    print("¿Cual es el nombre del producto")
    nombre_producto = input()
    producto =  obten_objetos(productos, prodCol.NOMBRE, nombre_producto)[0]
    print(producto)
#----------------------------------------------------------------------------------------------------   
#Esta función nos ayuda a saber a cantidad y los artículos que ha vendido dicho vendedor, al igual que
#su monto total generado 

def ventas_por_vendedor(productos, vendedores, ventas):
    print("Nombre del vendedor")
    nombre = input()
    vendedor = obten_objetos(vendedores, vendCol.NOMBRE, nombre) [0]
    vendedor_id = obten_atributo(vendedor, vendCol.VENDEDOR_ID)
    
    ventas_vendedor = obten_objetos(ventas, ventCol.VENDEDOR_ID, vendedor_id)
    
    total = 0
    matriz = []
    for f in ventas_vendedor:
        lista = []
        if int(obten_atributo(f,ventCol.CANTIDAD)) > 0:
            producto = obten_objetos(productos, prodCol.PRODUCTO_ID, obten_atributo(f, ventCol.PRODUCTO_ID )) [0]
            nombre_prod = obten_atributo(producto, prodCol.NOMBRE)
            lista.append(nombre_prod)
            precio = obten_atributo(producto, prodCol.PRECIO)
            unidades = obten_atributo(f,ventCol.CANTIDAD)
            lista.append(str(unidades))
            venta_t = int(precio) * int(unidades)
            v = f"${venta_t}"
            lista.append(v)
            total+= venta_t
            matriz.append(lista)
            
        
    respuesta = print_matriz(matriz)
    print(respuesta)
    print(f'Total: ${total}')
    
#-----------------------------------------------------------------------------------


def consultar_datos(productos, vendedores, ventas):
    print("Nombre del vendedor")
    vendedor_nombre = input()
    print("Dime el nombre del artículo")
    nombre_articulo = input()
    vendedor = obten_objetos(vendedores, vendCol.NOMBRE, vendedor_nombre )[0]
    vendedor_id = int(obten_atributo(vendedor,vendCol.VENDEDOR_ID))
    producto = obten_objetos(productos, prodCol.NOMBRE, nombre_articulo) [0]
    producto_id = obten_atributo(producto, prodCol.PRODUCTO_ID)
    nombre = vendedor[vendCol.NOMBRE]
    articulo = producto[prodCol.NOMBRE]
    
    for venta in ventas:
        unidades = venta[ventCol.CANTIDAD]
        if int(venta[ventCol.VENDEDOR_ID]) == vendedor_id and \
           int(venta[ventCol.PRODUCTO_ID]) == int(producto_id):
            print(f'{nombre} ha vendido {unidades} {articulo}')
#--------------------------------------------------------------------------------------------------------    
#Esta función nos ayuda a saber la cantidad de cierto producto en existencia 
def consultar_inventario(productos):
    print("Nombre del artículo")
    articulo = input()
    
    nombre = obten_objetos(productos, prodCol.NOMBRE, articulo) [0]
    filtrar_nombre = obten_atributo(nombre, prodCol.NOMBRE)
    filtrar = obten_atributo(nombre, prodCol.EXISTENCIA)
    
    print(f' Hay {filtrar} {filtrar_nombre} en existencia')
# -------------------------------------------------------------------------------------------------------
# Esta función nos ayuda a saber que vendedores han vendido cierto artículo, las unidades y el monto generado 

def reportes_ventas_articulo(productos, vendedores, ventas):
    print("Dime el nombre del artículo")
    nombre_articulo = input()
    articulo = obten_objetos(productos, prodCol.NOMBRE, nombre_articulo) [0]
    articulo_id = obten_atributo(articulo, prodCol.PRODUCTO_ID)
    cantidad = (obten_atributo(articulo,prodCol.PRECIO))
    ventas_articulo = obten_objetos(ventas, ventCol.PRODUCTO_ID , articulo_id)
    
    t = 0
    matriz = []
    for i in ventas_articulo:
        lista = []
        if int(obten_atributo(i, ventCol.CANTIDAD)) >0:
            vendedor = obten_objetos(vendedores, vendCol.VENDEDOR_ID , obten_atributo(i, ventCol.VENDEDOR_ID)) [0]
            nombre_vendedor = obten_atributo(vendedor, vendCol.NOMBRE)
            lista.append(nombre_vendedor)
            unidades = (obten_atributo(i, ventCol.CANTIDAD))
            lista.append((unidades))
            venta_t = int(cantidad) * int(unidades)
            t+=venta_t
            v = f'${venta_t}'
            lista.append(v)
         
            matriz.append(lista)
    respuesta = print_matriz(matriz)
    print(respuesta)
    print(f' Total: ${t}')
#-----------------------------------------------------------------------------------------------------
#Esta funcion nos ayuda a meter más artículos en la exitencia de dicho producto
def articulos_almacen(productos):
    print("Nombre del artículo")
    nombre_producto = input()
    print("¿Cuántas unidades son?")
    cantidad_productos = int(input())
    producto = obten_objetos(productos, prodCol.NOMBRE, nombre_producto)[0]
    suma = int(producto[prodCol.EXISTENCIA]) + cantidad_productos
    producto[prodCol.EXISTENCIA] = suma
    print("!Registrado en almacén correctamente!")


#----------------------------------------------------------------------------------------------------------    
#matrices de mis archivos, las cuales nos ayudan a la ejecución de todo nuestro programa
productos = load_products("Productos(prueba3).csv")
vendedores =load_products("Vendedores(prueba3).csv")
ventas = load_products("Ventas(prueba3).csv")

#---------------------------------------------------------------------------------------------------------
#Se despliega nuestro menú y las condiciónes de cada sección 
print("¡Bienvenido a Sport shop!")
respuesta = "."
while respuesta != "7":
    print("""¿Qué desea realizar?
1) Registrar ventas
2) Registrar llegada de artículos al almancén
3) Consultar datos del inventario
4) Consultar datos de ventas
5) Mostrar reporte de ventas por vendedor
6) Mostrar reporte de ventas por artículo
7) Cerrar y guardar""")
    respuesta = input("Introduzca su respuesta")
    if respuesta == "1":
        registar_ventas(productos, vendedores, ventas)
    elif respuesta == "2": 
        articulos_almacen(productos)
    elif respuesta == "3":
        consultar_inventario(productos)
    elif respuesta == "4":
        consultar_datos(productos, vendedores, ventas)       
    elif respuesta == "5":
        ventas_por_vendedor(productos, vendedores, ventas)
    elif respuesta == "6":
        reportes_ventas_articulo(productos, vendedores, ventas)
    elif respuesta != "7":
        print("Esta opción no existe en el menú, vuelva a intentarlo")
#Esta función guarda todos nuestros archivos la seleccionar nuestra opción 7 del menú     
    guardar_datos(productos,vendedores, ventas)
print("""Guardado correctamente
¡Que tenga un excelente día!""")

        

        