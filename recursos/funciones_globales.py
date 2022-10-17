import json
import psycopg2 as sql
from ctypes import windll
from traceback import format_exc
from datetime import datetime
from subprocess import Popen

def obtener_database():
    """
    Obtiene los parámetros de conexión a la base de datos de PostgreSQL del archivo respectivo y los retorna
    """
    try:
        with open("databases/database.ini", "r") as arch:
            db = arch.readline()
        return db
    except Exception as e:
            log_error()

def obtener_adm_ini():
    """
    Obtiene un diccionario con los datos de contacto del administrador del sistema y lo retorna
    """
    try:
        with open("databases/adm.json", "r") as arch:
            dicc = json.loads(arch.read())
        return dicc
    except Exception as e:
            log_error()

def calcular_relacion():
    """
    Obtiene la resolución de pantalla y retorna un string con la relación de aspecto redondeada en un número con un decimal
    """
    try:
        w = windll.user32.GetSystemMetrics(0)
        h = windll.user32.GetSystemMetrics(1)
        return f'{round(w/h, 1)}'
    except Exception as e:
            log_error()

def id_app():
    try:
        from ctypes import windll
        myappid = f'mfsolucionesinformaticas.morella'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass
    except Exception as e:
            log_error()

def run_query(database:str, query:str, select:int=0):
    """
    Esta función realiza una consulta a la base de datos.

    database: Cadena con el path de conexión a la base de datos

    query: Cadena con la consulta a la base de datos

    select (opcional): 0 -> No realiza fetch (valor por defecto)

                                1 -> Realiza fetchone (constante FETCHONE)

                                2 -> Realiza fetchall (constante FETCHALL)
    """
    with sql.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            if select == 1:
                dato = cursor.fetchone()
                return dato
            elif select == 2:
                datos = cursor.fetchall()
                return datos
            
def log_error(parent_error=None, dialog=1):
    """
    Esta función captura una excepción y la graba en el log de errores. 
    Si recibe el parámetro dialog=1 (valor por defecto), también se muestra un mensaje de error.
    """
    from recursos.constantes import ERROR_LOG_PATH
    from windows.models.LogError import LogError
    with open(ERROR_LOG_PATH, 'a') as log_error:
        exc = format_exc()
        log_error.write(
f"""
{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}:
{exc}

_________________________________________________


"""
                )
    if dialog == 1:
        error_dialog = LogError(parent_error)
        error_dialog.exec()

def acc_documentacion():
    """
    Esta función abre de manera externa el manual de instrucciones del sistema
    """
    from recursos.constantes import DOCUMENTATION_PATH
    path = DOCUMENTATION_PATH
    Popen([path], shell=True)

def obtener_categ_ing():
    """
    Esta función retorna una lista que contiene las categorías de ingreso
    """
    query =f"SELECT categoria FROM categorias_ingresos;"
    datos = run_query(obtener_database(), query, 2)
    categorias = []
    for i in datos:
        categorias.append(i[0])
    return categorias

def obtener_categ_egr():
    """
    Esta función retorna una lista que contiene las categorías de egreso
    """
    query =f"SELECT categoria FROM categorias_egresos;"
    datos = run_query(obtener_database(), query, 2)
    categorias = []
    for i in datos:
        categorias.append(i[0])
    return categorias

def obtener_categorias():
    ing = obtener_categ_ing()
    egr = obtener_categ_egr()
    return sorted(ing+egr)

def obtener_oficinas():
    """
    Esta función retorna una lista que contiene las oficinas
    """
    query =f"SELECT oficina FROM oficinas;"
    datos = run_query(obtener_database(), query, 2)
    oficinas = []
    for i in datos:
        oficinas.append(i[0])
    return oficinas



if __name__ == '__main__':
    for i in obtener_oficinas():
        print(i)