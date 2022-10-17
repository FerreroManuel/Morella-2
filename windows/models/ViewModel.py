from recursos.constantes import *
from recursos.funciones_globales import run_query
from PySide6.QtWidgets import (
    QScrollArea, 
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
    QGridLayout,
)
from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import (QIcon, QPixmap, QAction, QColor, )


class ViewModel(QDialog):
    """
    Esta clase es un modelo para crear ventanas tipo modales dedicadas a la vista de detalles de un registro
    """
    def __init__(self, user:dict) -> None:
        super().__init__()
        # ID Usuario
        self._user = user

        # CONFIGURACIONES GENERALES DE LA VENTANA
        # Ícono
        self.setWindowIcon(QIcon(MORELLA_ICON))
        
        # CONTENIDO DE LA VENTANA
        # Layouts
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        self._cuerpo = QVBoxLayout()
        self._botones = QHBoxLayout()
        self._botones.setAlignment(Qt.AlignRight)
        # Botones
        self._boton_eliminar = QPushButton('Eliminar')
        self._boton_guardar = QPushButton('Guardar cambios')
        boton_cerrar = QPushButton('Cerrar')

        # CONEXIÓN DE EVENTOS
        # Botones
        boton_cerrar.clicked.connect(self.close)

        # PUBLICACIÓN DE CONTENIDO
        # Botones
        self._botones.addWidget(self._boton_eliminar)
        self._botones.addWidget(self._boton_guardar)
        self._botones.addWidget(boton_cerrar)
        # Layouts
        layout_principal.addLayout(self._cuerpo)
        layout_principal.addLayout(self._botones)