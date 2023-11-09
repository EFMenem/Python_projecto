import sys
import csv
import os
import re

#Comandos
AGREGAR = 'agregar'
MODIFICAR = 'modificar'
ELIMINAR = 'eliminar'
LISTAR = 'listar'
NOMBRE = 'nombre'
CANTIDAD = 'cant'
HORARIO = 'hora'
UBICACION = 'ubicacion'

#Indices de argumentos
ID = 0
INDICE_COMANDO = 1
INDICE_NOMBRE = 2
INDICE_PERSONAS = 3
INDICE_HORARIO = 4
INDICE_UBICACION = 5

#Indices en la reserva
ID_INICIAL = 1
RESERVA_NOMBRE = 1
RESERVA_PERSONAS = 2
RESERVA_HORARIO = 3
RESERVA_UBICACION = 4

#Longitudes
VACIO = ''
LARGO_UN_ARGUMENTO = 2
LARGO_DOS_ARGUMENTOS = 3
LARGO_TRES_ARGUMENTOS = 4
MAX_INDICE_RESERVA = 6

#Indices de acciones
SOLO_COMANDO = 1
LISTAR_DESDE = 2
LISTAR_HASTA = 3

#HORARIO
MAX_HORAS = 23
MAX_MINUTOS = 59
CARACTERES_HORARIO = 5
MIN_HORAS_Y_MINUTOS = 0
POSICION_DOS_PUNTOS_HORARIO = 2

#Indices para modificar o eliminar
INDICE_NUMERO = 0
COMANDO_MODIFICAR = 0
ARGUMENTO_A_MODIFICAR = 1
MODIFICAR_ELIMINAR = 2

#Delimitador y nombre de archivos
DELIMITADOR = ';'
AUXILIAR = 'aux.csv'
RESTAURANT = 'restoran.csv'


#Ubicaciones 
AFUERA = 'F'
ADENTRO = 'D'

# PRE: comando debe ser diferente de vacio.
# POST: imprime comando invalido si no es un comando correcto.
def validar_comando(comando):
    comandos_permitidos = [AGREGAR, MODIFICAR, ELIMINAR, LISTAR]
    if comando not in comandos_permitidos:
        print("Comando invalido")
        return False
    else:
        return True

# PRE: nombre debe ser diferente de vacio
# POST: dedevuelve verdadero si el nombre es correcto o falso en caso contrario
def validar_nombre(nombre):
    return nombre.isalnum()
       
# PRE: cantidad debe ser diferente de vacio
# POST: devuelve verdadero si la cantidad de personas es correcto o falso en caso contrario
def validar_personas(personas):
    return personas.isnumeric()
      
# PRE: horario no puede ser vacío.
# POST: devuelve verdadero si el horario es valido.
def validar_horario(horario):
    formato = r'^([0-1]\d|2[0-3]):([0-5]\d)$'    # ^ coincide con el comienzo de la cadena y $ con el final de la misma \d marca que el 2do digito puede ser cualquier numero.
    if re.fullmatch(formato,horario):
        return True
    else:
        return False
      
# PRE: ubicacion no puede ser vacío.
# POST: devuelve verdadero si la ubicacion es afuera o adentro
def validar_ubicacion(ubicacion):
    return ubicacion in  [ADENTRO,AFUERA]
    
# PRE: los parametros deben ser diferentes a vacio
# POST: devuelve la leyenda si hubo un error en alguna carga de datos especifica.
def error_carga_datos(personas,nombre,ubicacion,horario):
    if not validar_personas(personas):
        print("Error en la carga de la cantidad de las personas")
    if not validar_nombre(nombre):
           print("Error en la carga del nombre")
    if not validar_ubicacion(ubicacion):
         print("Error en la carga de la ubicacion")
    if not validar_horario(horario) :
        print("Error en la carga del horario")
       
# PRE: comando debe ser listar, desde y hasta deben ser enteros o None.
# POST: devuelve por pantalla todas las reservas hechas.
def listar( desde, hasta):
    try:
        archivo = open(RESTAURANT)
    except:
        print('El archivo restoran.csv no pudo abrirse')
        return
    encontrado = False
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    for fila in lector:
        if desde is None and hasta is None:
            print(f"ID: {fila[ID]}")
            print(f"Nombre: {fila[RESERVA_NOMBRE]}")
            print(f"Personas: {fila[RESERVA_PERSONAS]}")
            print(f"Horario: {fila[RESERVA_HORARIO]}")
            print(f"Ubicación: {fila[RESERVA_UBICACION]}")
            print()
            encontrado = True
        
        elif int(desde) <= int(fila[ID]) <= int(hasta) :
            print(f"ID: {fila[ID]}")
            print(f"Nombre: {fila[RESERVA_NOMBRE]}")
            print(f"Personas: {fila[RESERVA_PERSONAS]}")
            print(f"Horario: {fila[RESERVA_HORARIO]}")
            print(f"Ubicación: {fila[RESERVA_UBICACION]}")
            print()
            encontrado = True
    if not encontrado:
        print('No existen reservas en ese rango')
    else:
        print('Estas son las reservas del día')             
    archivo.close()

# PRE: el archivo debe existir
# POST: devuelve verdadero si el ID esta en las reservas activas
def validar_id(indice):
    try:
        archivo = open(RESTAURANT)
    except:
        print('No pudo abrirse el archivo restoran.csv')
        return
    
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    encontrado = False
    for filas in lector:
        if indice == filas[ID]:
            encontrado = True
    archivo.close()
    return encontrado

# PRE: el archivo restoran.csv debe existir.
# POST: devuelve el id correspondiente a la reserva
def crear_id():
    try:
        archivo = open(RESTAURANT)
    except:
        print("Error al abrir el archivo restoran.csv")
        return 
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    ultimo_id = ID
    for fila in lector:
        if fila != VACIO:
            ultimo_id = max(ultimo_id, int(fila[ID]))
    id = ultimo_id + ID_INICIAL
    archivo.close()
    return id

# PRE: los parametros deben ser validos. Nombre y ubicacion deben ser de tipo caracter, cantidad de personas y horario debe ser de tipo enteros.
# POST: agrega la reserva al archivo        
def agregar(comando,nombre,personas,horario,ubicacion):
    try:
        archivo = open(RESTAURANT,"a")
    except:
        print('No pudo abrirse el archivo')
        return
    
    id = crear_id()
    reserva = [id,nombre, personas,horario,ubicacion]
    escritor = csv.writer(archivo, delimiter = DELIMITADOR)
    
    if comando == AGREGAR:
        escritor.writerow(reserva)
        archivo.close()
    print(f"Se agrego correctamente con el ID : {id}")
 
# PRE: indice debe estar entre los id de las reservas cargadas y debe ser numerico
# POST: elimina la reserva segun el ID de la misma
def eliminar(indice):
    try:
        archivo = open(RESTAURANT,"r")
    except:
        print("El archivo restoran.csv no pudo abrirse")
        return
    
    try:
        archivo_auxiliar = open(AUXILIAR,"w")
    except:
        archivo.close()
        print("El archivo aux.csv no pudo abrirse")
        return
    
    lector = csv.reader(archivo, delimiter = DELIMITADOR)
    escritor = csv.writer(archivo_auxiliar, delimiter = DELIMITADOR)
    encontrado = False
    for fila in lector:
        if fila[ID] != indice:
            escritor.writerow(fila)
        else:
            encontrado = True
            print(f"Se elimino correctamente el ID {fila[ID]}")
            
    archivo.close()
    archivo_auxiliar.close()
    os.rename(AUXILIAR, RESTAURANT)
    
    if not encontrado:
        print("El ID ingresado no existe")

# PRE: el vector debe existir para poder ser modificado.
# POST: modifica la cantidad de la reserva seleccionada
def modificar_cantidad(argumento,posicion_en_lista_que_voy_a_modificar, vector, lo_que_voy_a_modificar):
    modificado = False
    if validar_personas(argumento):
        vector[posicion_en_lista_que_voy_a_modificar] = lo_que_voy_a_modificar
        modificado = True
        return vector , modificado
    else:
        print("Error en la carga de la cantidad de personas")
 
# PRE: el vector debe existir para poder ser modificado.
# POST: modifica el nombre de la reserva seleccionada
def modificar_nombre(argumento,posicion_en_lista_que_voy_a_modificar, vector, lo_que_voy_a_modificar):
    modificado = False
    if validar_nombre(argumento):
        vector[posicion_en_lista_que_voy_a_modificar] = lo_que_voy_a_modificar
        modificado = True
        return vector , modificado
    else:
        print("Error en la carga del nombre")
        
# PRE: el vector debe existir para poder ser modificado.
# POST: modifica el horario de la reserva seleccionada
def modificar_horario(argumento,posicion_en_lista_que_voy_a_modificar, vector, lo_que_voy_a_modificar):
    modificado = False
    if validar_horario(argumento):
        vector[posicion_en_lista_que_voy_a_modificar] = lo_que_voy_a_modificar
        modificado = True
        return vector , modificado
    else:
        print("Error en la carga del horario")  

# PRE: el vector debe existir para poder ser modificado.
# POST: modifica la ubicacion de la reserva seleccionada
def modificar_ubicacion(argumento,posicion_en_lista_que_voy_a_modificar, vector, lo_que_voy_a_modificar):
    modificado = False
    if validar_ubicacion(argumento):
        vector[posicion_en_lista_que_voy_a_modificar] = lo_que_voy_a_modificar
        modificado = True
        return vector , modificado
    else:
        print("Error en la carga de la ubicacion")
              
# PRE: debe existir la reserva a modificar
# POST: modifica el campo de la reserva elegida.
def modificar(indice):
    comandos = [NOMBRE, CANTIDAD, HORARIO, UBICACION]
    try:
        archivo = open(RESTAURANT)
    except:
        print("El archivo restoran.csv no pudo abrirse")
        return
    
    try:
        archivo_auxiliar = open(AUXILIAR,"w")
    except:
        archivo.close()
        print("El archivo aux.csv no pudo abrirse")
        return
    
    lector = csv.reader(archivo, delimiter= DELIMITADOR)
    escritor = csv.writer(archivo_auxiliar, delimiter= DELIMITADOR)
    modificado = False
    for fila in lector:
        if fila[ID] == indice:
            datos_modificados = fila
            concepto = input("¿Que desea modificar? nombre [nombre], cant [cantidad], hora [horario] or ubicacion [ubicacion] : ")
            concepto_lista = concepto.split(" ")
            while concepto_lista[INDICE_NUMERO] not in comandos or len(concepto_lista) < LARGO_UN_ARGUMENTO:
                if concepto_lista[INDICE_NUMERO] not in comandos:
                    print('Ingresó un comando invalido ')
                else:
                    print('Falta el argumento a modificar')
                    
                concepto =  input("¿Que desea modificar? nombre [nombre], cant [cantidad], hora [horario] or ubicacion [ubicacion] : ")
                concepto_lista = concepto.split(' ')

            if concepto_lista[INDICE_NUMERO] == NOMBRE:
               modificado = modificar_nombre(concepto_lista[ARGUMENTO_A_MODIFICAR],RESERVA_NOMBRE,datos_modificados,concepto_lista[ARGUMENTO_A_MODIFICAR])
            elif concepto_lista[INDICE_NUMERO] == CANTIDAD:
                modificado = modificar_cantidad(concepto_lista[ARGUMENTO_A_MODIFICAR],RESERVA_PERSONAS,datos_modificados,concepto_lista[ARGUMENTO_A_MODIFICAR])        
            elif concepto_lista[INDICE_NUMERO] == HORARIO:
                modificado = modificar_horario(concepto_lista[ARGUMENTO_A_MODIFICAR],RESERVA_HORARIO,datos_modificados,concepto_lista[ARGUMENTO_A_MODIFICAR])
            elif concepto_lista[INDICE_NUMERO] == UBICACION:
                modificado = modificar_ubicacion(concepto_lista[ARGUMENTO_A_MODIFICAR],RESERVA_UBICACION,datos_modificados,concepto_lista[ARGUMENTO_A_MODIFICAR])
            else:
                print("Comando invalido")
            escritor.writerow(datos_modificados)
            
        else:
            escritor.writerow(fila)
    
    archivo.close()
    archivo_auxiliar.close()
    os.rename(AUXILIAR,RESTAURANT)
    if not validar_id(indice):
        print('No existe reserva con ese id')
        return
    if not modificado:
        print("No se pudo modificar la reserva")
    else:
        print(f"La reserva se modifico correctamente")    

def un_argumento():
    comandos = [LISTAR, MODIFICAR, AGREGAR, ELIMINAR]
    if len(sys.argv) == LARGO_UN_ARGUMENTO:
        comando = sys.argv[INDICE_COMANDO]
        if comando == LISTAR:
            listar(None, None)
        elif (comando != LISTAR and comando in comandos):
            print('Argumento incompleto')
        else:
            print("Comando invalido")

def dos_argumentos():
    if len(sys.argv) == LARGO_DOS_ARGUMENTOS:
        comando = sys.argv[INDICE_COMANDO]
        indice_eliminar_modificar = sys.argv[MODIFICAR_ELIMINAR]
        
        if indice_eliminar_modificar.isnumeric():
            if comando == ELIMINAR:
                eliminar(indice_eliminar_modificar)
            elif comando == MODIFICAR:
                modificar(indice_eliminar_modificar)
            elif comando == LISTAR:
                print('Indice incompleto')
        else:
            print("Indice es erroneo")      

def tres_argumentos():
    if LARGO_DOS_ARGUMENTOS < len(sys.argv) <= LARGO_TRES_ARGUMENTOS:
        comando = sys.argv[INDICE_COMANDO]
        desde = sys.argv[LISTAR_DESDE] 
        hasta = sys.argv[LISTAR_HASTA]
        if comando == LISTAR and desde.isnumeric() and hasta.isnumeric():
           listar(desde,hasta) 
        else:
            print("Los rangos deben ser en numero")       
            
def argumentos_completos():            
    if len(sys.argv) == MAX_INDICE_RESERVA:
        comando = sys.argv[INDICE_COMANDO]
        nombre = sys.argv[INDICE_NOMBRE]
        personas = sys.argv[INDICE_PERSONAS]
        horario = sys.argv[INDICE_HORARIO]
        ubicacion = sys.argv[INDICE_UBICACION]
        if (validar_comando(comando) and validar_nombre(nombre) and validar_personas(personas) and validar_horario(horario) and validar_ubicacion(ubicacion)):
            agregar(comando,nombre,personas,horario,ubicacion)
        else:
            error_carga_datos(personas,nombre,ubicacion,horario)
            
def main():
    
    un_argumento()
    dos_argumentos()
    tres_argumentos()
    argumentos_completos()
        
    
if __name__ == "__main__":
    main()