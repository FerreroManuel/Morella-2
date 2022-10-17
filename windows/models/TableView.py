from recursos.constantes import *
from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt, Slot


# class TableView(QTableWidget):
class TableView(QTableView):
    """
    Esta clase crea una vista de tabla donde pueden cargarse los datos de la base de datos
    """
    def __init__(self) -> None:
        try:
            super().__init__()
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()
        self.setStyleSheet("QHeaderView::section{background-color: lightGray;}")

    # Creación del slot para retornar el valor del item seleccionado
    @Slot('QItemSelection', 'QItemSelection')
    def _on_selection_changed(self, selected):
        self.selected_id = ""
        for i in selected.indexes():
            index = i
            break
        self.selected_id = index.siblingAtColumn(0).data()
