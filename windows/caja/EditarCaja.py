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


class EditarCaja(VerDetallesCaja):
    """
    Esta clase crea una ventana de edición para los registros de caja. Desde su llamada recibe los siguientes parámetros:
    
    > user: Es un diccionario con los datos del usuario que inició sesión. Las llaves del diccionario son 'id', 'nombre',
    'username' y 'privilegios'

    > id_reg: Es un número entero que representa el ID del registro
    """
    def __init__(self, user, id_reg) -> None:
        try:
            super().__init__(user, id_reg)
            # CONFIGURACIÓN DE LA VENTANA
            self.setWindowTitle('Editar Registro')
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
                    'No se pueden editar movimientos que se encuentran en una caja cerrada',
                    buttons=QMessageBox.Ok,
                    )
                self.setWindowTitle('No se puede editar el registro')
            else:
                # CONTENIDO DE LA VENTANA
                # Renglón 1
                # ID
                self._id_line.setReadOnly(True)
                # Fecha
                self._fecha_line.setReadOnly(True)
                # Renglón 2
                # Transacción
                self._transaccion_line.setReadOnly(False)
                # ¿Cerrada?
                self._cerrada_label.hide()
                self._cerrada_checkbox.hide()
                # Renglón 3
                # Categoría
                self._categoria_line.setText(str(self.datos[1]))
                # Descripción
                self._descripcion_line.setText(str(self.datos[2]))
                self._descripcion_line.setReadOnly(False)
                # Renglón 4
                # Ingreso
                if self.datos[4]:
                    self._ingreso_line.setText(str(self.datos[4]))
                    self._ingreso_line.setReadOnly(False)
                # Egreso
                if self.datos[5]:
                    self._egreso_line.setText(str(self.datos[5]))
                    self._egreso_line.setReadOnly(False)
                # Renglon 5
                # Observaciones
                self._observaciones_text.setText(self.datos[6])
                self._observaciones_text.setReadOnly(False)
                # Renglon 6
                # Usuario
                self._usuario_label.hide()
                # Botones
                self._boton_guardar.show()
                self._boton_guardar.clicked.connect(self.modificar_datos)

        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()
    
    def modificar_datos(self):
        """
        Esta función toma los datos volcados en la ventana de edición de registro de caja y los guarda en el registro correspondiente
        dentro de la base de datos, agregando a las observaciones una nota indicando que el registro fue modificado y el username del
        usuario que lo modificó. 
        
        También crea un registro en la tabla historial_caja de la base de datos, donde guarda los datos anteriores.
        
        Si no fueron indicados valores de ingreso o egreso, estos se exportan a la base de datos como valores NULL. 
        En caso de indicar valores NULL para ambos casos, el sistema arroja un error operacional.
        """
        try:
            error = 0
            # LECTURA DE LOS DATOS
            id_reg = self.datos[0]
            categoria = self._categoria_line.text()
            descripcion = self._descripcion_line.text()
            transaccion = self._transaccion_line.text()
            ingreso = self._ingreso_line.text()
            if ingreso == '' or ingreso == 0:
                ingreso = 'NULL'
            else:
                try:
                    float(ingreso)
                    error = False
                except ValueError:
                    error = True
                    QMessageBox.critical(
                    self,
                    'ERROR!',
                    f"El campo Ingreso debe ser completado con valores numéricos",
                    buttons=QMessageBox.Ok,
                    )
            egreso = self._egreso_line.text()
            if egreso == '' or egreso == 0:
                egreso = 'NULL'
            else:
                try:
                    float(egreso)
                    error = False
                except ValueError:
                    error = True
                    QMessageBox.critical(
                    self,
                    'ERROR!',
                    f"El campo Egreso debe ser completado con valores numéricos",
                    buttons=QMessageBox.Ok,
                    )
            if ingreso == 'NULL' and egreso == 'NULL':
                raise sql.OperationalError('El movimiento debe tener un valor de ingreso o egreso')
            observacion = self._observaciones_text.toPlainText()
            observacion_nueva = f'*[Registro modificado por {self._user["username"]}]* {self._observaciones_text.toPlainText()}'
            query_caja = f"""
    UPDATE caja 
    SET (categoria, descripcion, transaccion, ingreso, egreso, observacion)
    = 
    ('{categoria}', '{descripcion}', '{transaccion}', {ingreso}, {egreso}, '{observacion_nueva}')
    WHERE id = {id_reg};
    """
            query_historial = f"""
    INSERT INTO
    historial_caja (id, categoria, descripcion, transaccion, ingreso, egreso, observacion, id_user_m, fecha_y_hora_m)
    VALUES
    ({id_reg}, '{categoria}', '{descripcion}', '{transaccion}', {ingreso}, {egreso}, '{observacion}', {self._user['id']}, '{AHORA_STR}')
    ;"""
            run_query(DATABASE, query_caja)
            run_query(DATABASE, query_historial)
            QMessageBox.information(
                    self,
                    'Registro modificado',
                    'El registro fue modificado con éxito',
                    buttons=QMessageBox.Ok,
                    )
            self.close()
        except Exception as e:
            if error:
                pass
            else:
                QMessageBox.critical(
                        self,
                        'ERROR!',
                        f"""
    Surgió un error durante el proceso de edición. No se produjeron cambios en la base de datos.

    Para ver más detalles e informarlo diríjase a Ayuda -> Registro de errores en la barra de menú
                        """,
                        buttons=QMessageBox.Ok,
                        )
                log_error(parent_error='EditarCaja', dialog=0)