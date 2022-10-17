import psycopg2 as sql
from recursos.constantes import *
from recursos.funciones_globales import acc_documentacion
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
    
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import (QIcon, QPixmap, QAction, )
from windows.models.CRUDToolBar import CRUDToolBar
from windows.models.TableView import TableView


class GenericSubWindow(QWidget):
    """
    Esta clase genera una ventana modal genérica para utilizar en las distintas apps del sistema
    """
    def __init__(self) -> None:
        try:
            super().__init__()
            # CONFIGURACIONES GENERALES DE LA VENTANA
            # Tamaño
            self.setFixedSize(SCREEN_WIDHT-40, SCREEN_HEIGHT-110)

            # CONTENIDO DE LA VENTANA
            self._layout_principal = QVBoxLayout()
            self._layout_header = QHBoxLayout()
            self.setLayout(self._layout_principal)
            self._layout_principal.addLayout(self._layout_header)
            titulo = QLabel()
            titulo.setText('<b>Movimientos de caja: </b>')
            titulo.setTextFormat(Qt.RichText)
            self._layout_header.addWidget(titulo)
            self._toolbar = ""
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error(parent_error='GenericSubWindow')
            
    def _crud_toolbar(self, user, table, models, ButtonStyle):
        """
        Esta función crea una barra de herramientas con las opciones de CRUD
        """
        crud_toolbar = CRUDToolBar(user, table, models, ButtonStyle)
        self._layout_header.addWidget(crud_toolbar)
        return crud_toolbar
        
    def _table_view(self):
        """
        Esta función crea una tabla donde mostrar los datos de la base de datos
        """
        table_view = TableView()
        self._layout_principal.addWidget(table_view)
        return table_view
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_F1:
            acc_documentacion()
        elif event.key() == Qt.Key_F4:
            self._toolbar.buscar_registro()
        elif event.key() == Qt.Key_F5:
            self._toolbar.actualizar_tabla()
        elif event.key() == Qt.Key_F6:
            self._toolbar.ver_detalles()
        elif event.key() == Qt.Key_F7:
            self._toolbar.nuevo_registro()
        elif event.key() == Qt.Key_F8:
            self._toolbar.editar_registro()
        elif event.key() == Qt.Key_F9:
            self._toolbar.eliminar_registro()
        elif event.key() == Qt.Key_F10:
            self._toolbar.generar_pdf()
        elif event.key() == Qt.Key_F11:
            self._toolbar.generar_xls()
        else:
            pass