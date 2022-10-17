if __name__ != '__main__':
    from recursos.constantes import *
    from recursos.funciones_globales import run_query
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
from PySide6.QtCore import Qt, QSize ,QAbstractTableModel
from PySide6.QtGui import (QIcon, QPixmap, QAction, )




class DataModel(QAbstractTableModel):
    def __init__(self, data, header_labels):
        super().__init__()
        self._data = data
        self._header_labels = header_labels

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        # Todas las listas interiores deben ser del mismo largo
        return len(self._data[0])
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header_labels[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return '>'
        return super().headerData(section, orientation, role)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                if value == None:
                    value = ''
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled