from recursos.constantes import *
from recursos.funciones_globales import run_query
from recursos.DataModel import DataModel
from PySide6.QtWidgets import (
    QMdiSubWindow,
    QBoxLayout,
    QToolBar,
    QApplication,
    QWidget,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QStatusBar,
    QLabel,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QMdiArea,
    QTableView,   
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import (QIcon, QPixmap, QAction, )


class CRUDToolBar(QWidget):
    """
Esta clase crea un widget compuesto por botones, simulando ser una barra de herramientas, con las funciones necesarias para hacer
CRUD (Create, Read, Update, Delete), buscar registros y exportar la información ya sea a PDF o a Excel

Recibe los siguientes parámetros:

    - user: <class 'dict'> Diccionario con los datos del usuario que inició sesión. Las llaves del diccionario son 'id', 'nombre',
    'username' y 'privilegios'

    - table: <class 'PySide6.QtWidgets.QTableView'> Tabla donde se muestran los registros

    - models: <class 'dict'> Diccionario con los nombres de clase que invoca cada botón. Las llaves del diccionario son 'buscar_registro',
    'ver_detalles', 'nuevo_registro', 'editar_registro' y 'eliminar_registro'

    - ButtonStyle: <class 'int'> Determina el estilo de botones que se van a visualizar en el widget:
        - 1: Sólo los íconos (Ref.: constante SOLO_ICONO)
        - 2: Sólo las etiquetas (Ref.: constante SOLO_TEXTO)
        - 3: Ambos íconos y etiquetas (Ref.: constante ICONO_Y_TEXTO)
    """

    _refresh_query = ""
    _header_labels = []
    _query = ""

    def __init__(self, user:dict, table:QTableView, models:dict, ButtonStyle:int) -> None:
        try:
            super().__init__()
            # VARIABLES DE CLASE
            self._table = table
            self._models = models
            self._user = user

            # CREACIÓN DE TOOLBAR
            # Creación del layout
            self.toolbar_layout = QHBoxLayout()
            self.adjustSize()
            self.toolbar_layout.setAlignment(Qt.AlignRight)
            self.setLayout(self.toolbar_layout)
            
            self._crear_botones(ButtonStyle)
            self._publicar_botones()
            self._status_tip_botones()
            self._conectar_eventos()
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error(parent_error='CRUDToolBar')
        
    def _crear_botones(self, ButtonStyle):
        """
        Esta función crea los botones para el CRUD
        """
        if ButtonStyle == ICONO_Y_TEXTO:
            self.boton_buscar = QPushButton(QIcon(SEARCH_ICON), 'Buscar un registro', self)
            self.boton_actualizar = QPushButton(QIcon(REFRESH_ICON), 'Actualizar', self)
            self.boton_ver = QPushButton(QIcon(VIEW_ICON),'Ver detalles', self)
            self.boton_nuevo = QPushButton(QIcon(ADD_ICON),'Nuevo registro', self)
            self.boton_editar = QPushButton(QIcon(EDIT_ICON),'Editar registro', self)
            self.boton_eliminar = QPushButton(QIcon(DELETE_ICON),'Eliminar registro', self)
            self.boton_imprimir = QPushButton(QIcon(PRINT_ICON), 'Generar reporte en PDF', self)
            self.boton_excel = QPushButton(QIcon(EXCEL_ICON), 'Generar un reporte en Excel', self)

        elif ButtonStyle == SOLO_TEXTO:
            self.boton_buscar = QPushButton('Buscar un registro', self)
            self.boton_actualizar = QPushButton('Actualizar', self)
            self.boton_ver = QPushButton('Ver detalles', self)
            self.boton_nuevo = QPushButton('Nuevo registro', self)
            self.boton_editar = QPushButton('Editar registro', self)
            self.boton_eliminar = QPushButton('Eliminar registro', self)
            self.boton_imprimir = QPushButton('Generar reporte en PDF', self)
            self.boton_excel = QPushButton('Generar un reporte en Excel', self)

        elif ButtonStyle == SOLO_ICONO:
            self.boton_buscar = QPushButton(QIcon(SEARCH_ICON), '', self)
            self.boton_buscar.setIconSize(QSize(25, 25))
            self.boton_actualizar = QPushButton(QIcon(REFRESH_ICON), '', self)
            self.boton_actualizar.setIconSize(QSize(25, 25))
            self.boton_ver = QPushButton(QIcon(VIEW_ICON),'', self)
            self.boton_ver.setIconSize(QSize(25, 25))
            self.boton_nuevo = QPushButton(QIcon(ADD_ICON),'', self)
            self.boton_nuevo.setIconSize(QSize(25, 25))
            self.boton_editar = QPushButton(QIcon(EDIT_ICON),'', self)
            self.boton_editar.setIconSize(QSize(25, 25))
            self.boton_eliminar = QPushButton(QIcon(DELETE_ICON),'', self)
            self.boton_eliminar.setIconSize(QSize(25, 25))
            self.boton_imprimir = QPushButton(QIcon(PRINT_ICON), '', self)
            self.boton_imprimir.setIconSize(QSize(25, 25))
            self.boton_excel = QPushButton(QIcon(EXCEL_ICON), '', self)
            self.boton_excel.setIconSize(QSize(25, 25))
            
    def _publicar_botones(self):
        """
        Esta función publica los botones para el CRUD dentro del layout
        """
        self.toolbar_layout.addWidget(self.boton_buscar)
        self.toolbar_layout.addWidget(self.boton_actualizar)
        self.toolbar_layout.addWidget(QLabel('  |  '))
        self.toolbar_layout.addWidget(self.boton_ver)
        self.toolbar_layout.addWidget(QLabel('  |  '))
        self.toolbar_layout.addWidget(self.boton_nuevo)
        self.toolbar_layout.addWidget(self.boton_editar)
        self.toolbar_layout.addWidget(self.boton_eliminar)
        self.toolbar_layout.addWidget(QLabel('  |  '))
        self.toolbar_layout.addWidget(self.boton_imprimir)
        self.toolbar_layout.addWidget(self.boton_excel)

    def _status_tip_botones(self):
        """
        Esta función muestra un mensaje en la barra de estado para cada botón
        """
        self.boton_buscar.setStatusTip('Buscar un registro (F4)')
        self.boton_actualizar.setStatusTip('Actualizar tabla (F5)')
        self.boton_ver.setStatusTip('Ver detalles del registro (F6)')
        self.boton_nuevo.setStatusTip('Insertar nuevo registro (F7)')
        self.boton_editar.setStatusTip('Editar registro (F8)')
        self.boton_eliminar.setStatusTip('Eliminar registro (F9)')
        self.boton_imprimir.setStatusTip('Generar un reporte en PDF (F10)')
        self.boton_excel.setStatusTip('Generar un reporte en Excel (F11)')

    def _conectar_eventos(self):
        """
        Esta función conecta las señales de los botones con sus respectivos slot
        """
        self.boton_buscar.clicked.connect(self.buscar_registro)
        self.boton_actualizar.clicked.connect(self.actualizar_tabla)
        self.boton_ver.clicked.connect(self.ver_detalles)
        self.boton_nuevo.clicked.connect(self.nuevo_registro)
        self.boton_editar.clicked.connect(self.editar_registro)
        self.boton_eliminar.clicked.connect(self.eliminar_registro)
        self.boton_imprimir.clicked.connect(self.generar_pdf)
        self.boton_excel.clicked.connect(self.generar_xls)

    def set_refresh_query(self, query):
        """
        Esta función obtiene el query que utilizará la función actualizar_tabla para seleccionar los datos de la base de datos
        """
        self._refresh_query = query

    def set_header_labels(self, header_labels):
        """
        Esta función obtiene las cabeceras de la tabla
        """
        if type(header_labels) != list:
            raise ReferenceError('El argumento debe ser de tipo list')
        self._header_labels = header_labels

    def buscar_registro(self, query):
        """
        Esta función abre una ventana donde se muestran los datos del registro seleccionado y permite editarlos, siempre y cuando éste
        no pertenezca a una caja que se encuentre cerrada
        """
        # self._editar_registro = self._models['buscaar_registro'](self._user, self._table.selected_id)
        # self._editar_registro.exec()
        pass
    
    def actualizar_tabla(self):
        """
        Esta función actualiza la tabla cargando todos los items de la consulta

        ATENCIÓN: Antes de llamar la función se debe llamar a la función set_refresh_query y set_header_labels
        """
        datos_tabla = []
        if not self._refresh_query:
            raise ReferenceError('No se indicó ninguna consulta [_refresh_query]')
        if not self._header_labels:
            raise ReferenceError('No se indicaron nombres de columnas [_header_labels]')
        if self._refresh_query:
            datos_tabla = run_query(DATABASE, self._refresh_query, FETCHALL)
        if datos_tabla:
            # for n,i in enumerate(datos_tabla):
            #     if i == None:
            #         datos_tabla[n] = ''
            self._model = DataModel(datos_tabla, self._header_labels)
            self._table.setModel(self._model)
            self._table.resizeColumnsToContents()
            selection_model = self._table.selectionModel()
            self._selected_row = selection_model.selectionChanged.connect(self._table._on_selection_changed)
            self._table.doubleClicked.connect(self.double_clicked_table)
        else:
            raise ReferenceError('No se encontraron datos en la tabla solicitada')
            
    def ver_detalles(self):
        """
        Esta función abre una ventana donde se muestran los datos del registro seleccionado
        """        
        self._ver_detalles = self._models['ver_detalles'](self._user, self._table.selected_id)
        self._ver_detalles.exec()

    def nuevo_registro(self):
        """
        Esta función abre una ventana donde se le permite al usuario registrar un nuevo movimiento de caja
        """
        self._nuevo_registro = self._models['nuevo_registro'](self._user)
        self._nuevo_registro.exec()

    def editar_registro(self):
        """
        Esta función abre una ventana donde se muestran los datos del registro seleccionado y permite editarlos, siempre y cuando éste
        no pertenezca a una caja que se encuentre cerrada
        """
        self._editar_registro = self._models['editar_registro'](self._user, self._table.selected_id)
        self._editar_registro.exec()

    def eliminar_registro(self):
        """
        Esta función abre una ventana donde se muestran los datos del registro seleccionado y permite eliminarlo, siempre y cuando éste
        no pertenezca a una caja que se encuentre cerrada
        """
        self._eliminar_registro = self._models['eliminar_registro'](self._user, self._table.selected_id)
        self._eliminar_registro.exec()

    def generar_pdf(self):
        """
        Esta función 
        """
        pass
    
    def generar_xls(self):
        """
        Esta función 
        """
        pass

    def double_clicked_table(self):
        """
        Esta función selecciona el valor de la primer columna del renglón donde el usuario hace doble click y llama a la función ver_detalles
        """
        index = self._table.selectedIndexes()[0]
        self._table.selected_id = index.siblingAtColumn(0).data()
        self.ver_detalles()

