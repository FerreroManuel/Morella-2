from recursos.constantes import *
from windows.models.GenericSubWindow import GenericSubWindow
from PySide6.QtWidgets import (QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QStackedLayout, QStatusBar,
QLabel, QLineEdit, QComboBox, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, )
from PySide6.QtCore import Qt
from PySide6.QtGui import (QIcon, QPixmap, QAction, )


class LogError(QMessageBox):
    

    def __init__(self, parent_error):
        super().__init__()
        self.setWindowIcon(QPixmap(MORELLA_ICON))
        self.setWindowTitle(f'ERROR!')
        text = f"""
Se produjo un error al intentar realizar la acción solicitada

Para ver más detalles e informarlo diríjase a Ayuda -> Registro de errores en la barra de menú

[{parent_error}]
        """
        self.setText(text)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIconPixmap(QPixmap(ERROR_ICON))
