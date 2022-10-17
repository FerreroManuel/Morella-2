import psycopg2 as sql
from recursos.constantes import *
from recursos.funciones_globales import log_error, run_query
from windows.caja.VerDetallesCaja import VerDetallesCaja
from PySide6.QtWidgets import (
    QCheckBox,
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
    QTextEdit,
)
from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import (QIcon, QPixmap, QAction, QColor, )


class EliminarCaja(VerDetallesCaja):
    """
    Esta clase crea una ventana donde se muestran los detalles del registro de caja y da la posibilidad de eliminarlo.
    Desde su llamada recibe los siguientes parámetros:
    
    > user: Es un diccionario con los datos del usuario que inició sesión. Las llaves del diccionario son 'id', 'nombre',
    'username' y 'privilegios'

    > id_reg: Es un número entero que representa el ID del registro
    """
    def __init__(self, user, id_reg) -> None:
        try:
            super().__init__(user, id_reg)
            # CONFIGURACIÓN DE LA VENTANA
            self.setWindowTitle('Eliminar Registro')
            self.setBaseSize(400, 600)
            
            # CONEXIÓN CON DB
            query = f"""
SELECT c.id, categoria, descripcion, transaccion, ingreso, egreso, observacion, dia, mes, año, cerrada, u.user_name
FROM caja c
JOIN usuarios u
ON c.id_user = u.id
WHERE c.id = {id_reg}
ORDER BY c.id;
"""
            self.datos = run_query(DATABASE, query, FETCHONE)
                        
            # Verificación de caja cerrada
            if self.datos[10] == 1:
                QMessageBox.critical(
                    self,
                    'ERROR!',
                    'No se pueden eliminar movimientos que se encuentran en una caja cerrada',
                    buttons=QMessageBox.Ok,
                    )
                self.setWindowTitle('No se puede eliminar el registro')
            else:
                # CONTENIDO DE LA VENTANA
                # Renglón 2
                # ¿Cerrada?
                self._cerrada_label.hide()
                self._cerrada_checkbox.hide()
                # Botones
                self._boton_eliminar.show()
                self._boton_eliminar.clicked.connect(self.eliminar_registro)

        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()
    
    def eliminar_registro(self):
        """
        Esta función elimina el registro seleccionado de la base de datos 

        También crea un registro en la tabla historial_caja de la base de datos, donde guarda los datos anteriores.
        """
        try:
            # LECTURA DE LOS DATOS
            id_reg = self.datos[0]
            categoria = self._categoria_line.text()
            descripcion = self._descripcion_line.text()
            transaccion = self._transaccion_line.text()
            ingreso = self._ingreso_line.text()
            if ingreso == '' or ingreso == 0:
                ingreso = 'NULL'
            egreso = self._egreso_line.text()
            if egreso == '' or egreso == 0:
                egreso = 'NULL'
            observacion_nueva = f'*[Registro eliminado por {self._user["username"]}]* {self._observaciones_text.toPlainText()}'
            query_caja = f"""
    DELETE FROM caja WHERE id = {id_reg}
    """
            query_historial = f"""
    INSERT INTO
    historial_caja (id, categoria, descripcion, transaccion, ingreso, egreso, observacion, id_user_m, fecha_y_hora_m)
    VALUES
    ({id_reg}, '{categoria}', '{descripcion}', '{transaccion}', {ingreso}, {egreso}, '{observacion_nueva}', {self._user['id']}, '{AHORA_STR}')
    ;"""
            run_query(DATABASE, query_caja)
            run_query(DATABASE, query_historial)
            QMessageBox.information(
                    self,
                    'Registro eliminado',
                    'El registro fue eliminado con éxito',
                    buttons=QMessageBox.Ok,
                    )
        except Exception as e:
            QMessageBox.critical(
                    self,
                    'ERROR!',
                    f"""
Surgió un error durante el proceso de eliminación. No se produjeron cambios en la base de datos.

Para ver más detalles e informarlo diríjase a Ayuda -> Registro de errores en la barra de menú
                    """,
                    buttons=QMessageBox.Ok,
                    )
            log_error(parent_error='EliminarCaja', dialog=0)
        finally:
            self.close()