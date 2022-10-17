from recursos.constantes import *
from windows.models.ViewModel import ViewModel
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QFormLayout,
    QTextEdit,
)
from PySide6.QtCore import Qt


class ViewModelCaja(ViewModel):
    """
    Esta clase es un modelo para crear ventanas tipo modales dedicadas a la vista de detalles de un registro
    """
    def __init__(self, user:dict, id_reg:int=None) -> None:
        super().__init__(user)
        # CONFIGURACIÓN DE LA VENTANA
        self.setBaseSize(400, 600)

        # CONTENIDO DE LA VENTANA
        self._col1_layout = QFormLayout()
        self._col2_layout = QFormLayout()
        self._forms = QHBoxLayout()
        self._forms.addLayout(self._col1_layout)
        self._forms.addLayout(self._col2_layout)
        self._cuerpo.addLayout(self._forms)
        # Renglón 1
        # ID
        self._id_label = QLabel('<b>ID: </b>')
        self._id_line = QLineEdit()
        self._id_line.setAlignment(Qt.AlignRight)
        self._id_line.setFixedWidth(70)
        self._col1_layout.addRow(self._id_label, self._id_line)
        # Fecha
        self._col2_layout.setAlignment(Qt.AlignRight)
        self._fecha_label = QLabel('<b>Fecha: </b>')
        self._fecha_line = QLineEdit()
        self._fecha_line.setInputMask('99/99/9999')
        self._fecha_line.setAlignment(Qt.AlignRight)
        self._fecha_line.setFixedWidth(70)
        self._col2_layout.addRow(self._fecha_label, self._fecha_line)
        # Renglón 2
        # Transacción
        self._transaccion_label = QLabel('<b>Nro. Transacción: </b>')
        self._transaccion_line = QLineEdit()
        self._transaccion_line.setAlignment(Qt.AlignRight)
        self._transaccion_line.setFixedWidth(70)
        self._col1_layout.addRow(self._transaccion_label, self._transaccion_line)
        # ¿Cerrada?
        self._cerrada_label = QLabel('<b>¿Está cerrada?: </b>')
        self._cerrada_checkbox = QCheckBox()
        self._cerrada_checkbox.setFixedSize(20,20)
        self._col2_layout.addRow(self._cerrada_label, self._cerrada_checkbox)
        # Renglón 3
        # Categoría
        self._categoria_label = QLabel('<b>Categoría: </b>')
        self._categoria_line = QLineEdit()
        self._categoria_line.setAlignment(Qt.AlignLeft)
        self._categoria_line.setFixedWidth(200)
        self._col1_layout.addRow(self._categoria_label, self._categoria_line)
        # Descripción
        self._descripcion_label = QLabel('<b>Descripción: </b>')
        self._descripcion_line = QLineEdit()
        self._descripcion_line.setAlignment(Qt.AlignLeft)
        self._descripcion_line.setFixedWidth(250)
        self._col2_layout.addRow(self._descripcion_label, self._descripcion_line)
        # Renglón 4
        # Ingreso
        self._ingreso_label = QLabel('<b>Ingreso: </b>')
        self._ingreso_line = QLineEdit()
        self._ingreso_line.setAlignment(Qt.AlignRight)
        self._ingreso_line.setFixedWidth(100)
        self._col1_layout.addRow(self._ingreso_label, self._ingreso_line)
        # Egreso
        self._egreso_label = QLabel('<b>Egreso: </b>')
        self._egreso_line = QLineEdit()
        self._egreso_line.setAlignment(Qt.AlignRight)
        self._egreso_line.setFixedWidth(100)
        self._col2_layout.addRow(self._egreso_label, self._egreso_line)
        # Renglon 5
        # Observaciones
        self._observaciones_label = QLabel('<b>Observaciones: </b>')
        self._observaciones_text = QTextEdit()
        self._cuerpo.addWidget(self._observaciones_label)
        self._cuerpo.addWidget(self._observaciones_text)
        # Renglon 6
        # Usuario
        self._usuario_label = QLabel()
        self._usuario_label.setAlignment(Qt.AlignRight)
        self._cuerpo.addWidget(self._usuario_label)