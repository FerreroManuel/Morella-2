from datetime import datetime, date
from ctypes import windll
from recursos.funciones_globales import obtener_database, calcular_relacion, obtener_adm_ini

# CONSTANTES GENERALES DE LA APP
RELEASE_DATE = f'01/08/2022'
SHORT_VERSION = f'2.0.0'
VERSION = f'{SHORT_VERSION}.{RELEASE_DATE[8:10]}{RELEASE_DATE[3:5]}'
TYPE_VERSION = f'ALPHA'

# CONSTANTES DE CONTACTO ADMIN
CONTACT_DICT = obtener_adm_ini()
CONTACT_PHONE = CONTACT_DICT['phone']
CONTACT_PHONE_STR = CONTACT_DICT['phone-str']
CONTACT_EMAIL = CONTACT_DICT['email']
ADM_WEB = CONTACT_DICT['web']

# CONSTANTES DE BASE DE DATOS
DATABASE = str(obtener_database())
DATABASE_PUBLIC_INFO = f"{DATABASE.split(' ')[0].split('=')[1]}:{DATABASE.split(' ')[4].split('=')[1]} ({DATABASE.split(' ')[1].split('=')[1]})"

# CONSTANTES DE FECHA
AHORA = datetime.now()
AHORA_STR = f'{AHORA.day}/{str(AHORA.month).rjust(2, "0")}/{AHORA.year} {AHORA.hour}:{AHORA.minute}:{AHORA.second}'
HOY = datetime.now().date()
HOY_STR = f'{HOY.day}/{str(HOY.month).rjust(2, "0")}/{HOY.year}'

# CONSTANTES DE GUI
# Fondos
BACKGROUND_DYNAMIC_FILE = f'docs/system/bkg/bkg{calcular_relacion()}.png'
BACKGROUND_BLUE_GRADIENT = "QMainWindow{background-color: qlineargradient(spread:reflect, x1:1, y1:0, x2:1, y2:0.489, stop:0 rgba(0, 0, 15, 255), stop:1 rgba(0, 0, 90, 255));}"
BACKGROUND_FILE = f'docs/system/bkg/bkg_solo_logo.png'
# Íconos
MORELLA_ICON = f'docs/system/icons/icono.png'
OK_ICON = f'docs/system/icons/ok.png'
ERROR_ICON = f'docs/system/icons/error.png'
ADD_ICON = f'docs/system/icons/add.png'
VIEW_ICON = f'docs/system/icons/view.png'
EDIT_ICON = f'docs/system/icons/edit.png'
DELETE_ICON = f'docs/system/icons/delete.png'
REFRESH_ICON = f'docs/system/icons/refresh.png'
PRINT_ICON = f'docs/system/icons/print.png'
EXCEL_ICON = f'docs/system/icons/excel.png'
SEARCH_ICON = f'docs/system/icons/search.png'
# Tamaños
SCREEN_WIDHT = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1)
# Botones
SOLO_ICONO = 1
SOLO_TEXTO = 2
ICONO_Y_TEXTO = 3

# PATHS DE ARCHIVOS 
"""
Usar barra invertida para la separación de carpetas
"""
DOCUMENTATION_PATH = f'docs\Documentacion.pdf'
ERROR_LOG_PATH = f'error.log'

# CONSTANTES DE QUERYS
FETCHONE = 1
FETCHALL = 2
