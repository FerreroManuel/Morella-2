import psycopg2 as sql
from recursos.constantes import *
from recursos.funciones_globales import log_error, obtener_oficinas, run_query
from windows.caja.ViewModelCaja import ViewModelCaja
from windows.models.ViewModel import ViewModel
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


class NuevoCaja(ViewModel):
    """
    Esta clase crea una ventana dedicada al registro de un nuevo movimiento caja en la base de datos. Desde su llamada recibe 
    los siguientes parámetros:
    
    > user: Es un diccionario con los datos del usuario que inició sesión. Las llaves del diccionario son 'id', 'nombre',
    'username' y 'privilegios'
    """

    _tipos_movimiento = [
        'Gasto de oficina (-)',
        'Pago de alquiler (-)',
        'Pago de sueldo (-)',
        'Pago de comisión (-)',
        'Alivio de caja (-)',
        'Monto a rendir (-)',
        'Rendición adeudada (+)',
        'Ingreso extraordinario (+)',
    ]

    _oficinas = obtener_oficinas()


    def __init__(self, user:dict) -> None:
        super().__init__(user)
        self._user = user
        
        # CONTENIDO VENTANA
        # Renglón 1 - Categoría
        self._renglon1_label = QLabel('<b>Tipo de movimiento: </b>')
        self._renglon1_combo = QComboBox()
        self._renglon1_combo.addItem('Seleccione el tipo de movimiento')
        self._renglon1_combo.addItems(self._tipos_movimiento)
        self._renglon1_combo.setEditable(False)
        self._renglon1_combo.currentTextChanged.connect(self._crear_layout_tipo)
        # Renglón Of - Oficina
        self._renglonOf_label = QLabel('<b>Oficina: </b>')
        self._renglonOf_combo = QComboBox()
        self._renglonOf_combo.addItems(self._oficinas)
        self._renglonOf_combo.setEditable(False)
        # Renglón 2 - Transacción
        self._renglon2_label = QLabel('<b>Transacción: </b>')
        self._renglon2_line = QLineEdit()
        # Renglón 3 - Descripción
        self._renglon3_label = QLabel('<b>Descripción: </b>')
        self._renglon3_line = QLineEdit()
        # Renglón 4 - Ingreso/Egreso
        self._renglon4_label = QLabel('<b>Monto: </b>')
        self._renglon4_line = QLineEdit()
        # Renglón 5 - Observaciones
        self._renglon5_label = QLabel('<b>Observaciones: </b>')
        self._renglon5_text = QTextEdit()
        
        # ESQUELETO VENTANA
        # Form Layout - Formulario
        self._form_layout = QFormLayout()
        self._cuerpo.addLayout(self._form_layout)
        self._form_layout.addRow(self._renglon1_label, self._renglon1_combo)
        self._form_layout.addRow(self._renglonOf_label, self._renglonOf_combo)
        self._form_layout.addRow(self._renglon2_label, self._renglon2_line)
        self._form_layout.addRow(self._renglon3_label, self._renglon3_line)
        self._form_layout.addRow(self._renglon4_label, self._renglon4_line)
        self._form_layout.addRow(self._renglon5_label, self._renglon5_text)
        # Se oculta el renglón de oficina
        self._renglonOf_label.hide()
        self._renglonOf_combo.hide()

        # BOTONES
        self._boton_eliminar.hide()
        self._boton_guardar.clicked.connect(self._insertar_registro)


    def _crear_layout_tipo(self, tipo):
        """
        Esta función muestra distintos campos según el tipo de movimiento selecionado por el usuario
        """
        if tipo == 'Gasto de oficina (-)':
            # Renglón Of
            self._renglonOf_label.show()
            self._renglonOf_combo.show()
            # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Ticket: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Descripción: </b>')
            # Renglón 4 - Egreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Pago de alquiler (-)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
             # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Ticket: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Descripción: </b>')
            # Renglón 4 - Egreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Pago de sueldo (-)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
             # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Recibo: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Empleado: </b>')
            # Renglón 4 - Egreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Pago de comisión (-)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
             # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Recibo: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Empleado: </b>')
            # Renglón 4 - Egreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Alivio de caja (-)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
            # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Entrega: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Recibe: </b>')
            # Renglón 4 - Egreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Monto a rendir (-)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
            # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Rendición: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Cobrador: </b>')
            # Renglón 4 - Ingres
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Rendición adeudada (+)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
            # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Rendición: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Cobrador: </b>')
            # Renglón 4 - Ingres
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Ingreso extraordinario (+)':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
            # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Ticket / Recibo: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Descripción: </b>')
            # Renglón 4 - Ingreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')
        elif tipo == 'Seleccione el tipo de movimiento':
            # Renglón Of
            self._renglonOf_label.hide()
            self._renglonOf_combo.hide()
            # Renglón 2 - Transacción
            self._renglon2_label.setText('<b>Transacción: </b>')
            # Renglón 3 - Descripción
            self._renglon3_label.setText('<b>Descripción: </b>')
            # Renglón 4 - Egreso
            self._renglon4_label.setText('<b>Monto: </b>')
            # Renglón 5 - Observaciones
            self._renglon5_label.setText('<b>Observaciones: </b>')


    def _insertar_registro(self):
        """
        Esta función toma los datos volcados en la ventana de nuevo registro de caja y crea un registro dentro de la base de datos 
        con esos datos y el username del usuario que lo insertó.
        
        Si no fueron indicados valores de ingreso o egreso, estos se exportan a la base de datos como valores NULL. 
        En caso de indicar valores NULL para ambos casos, el sistema arroja un error operacional.
        """

        try:
            error = False
            
            # LECTURA DEL FORMULARIO
            # Generar valor de categoría según combobox
            if self._renglon1_combo.currentText() == 'Gasto de oficina (-)':
                oficina = self._renglonOf_combo.currentText()
                if oficina == 'Panteón NOB':
                    categoria = f'Gastos {oficina}'
                else:
                    categoria = f'Gastos oficina {oficina}'
            elif self._renglon1_combo.currentText() == 'Pago de alquiler (-)':
                categoria = 'Pago de alquileres'
            elif self._renglon1_combo.currentText() == 'Pago de sueldo (-)':
                categoria = 'Pago de sueldos'
            elif self._renglon1_combo.currentText() == 'Pago de comisión (-)':
                categoria = 'Pago de comisiones'
            elif self._renglon1_combo.currentText() == 'Alivio de caja (-)':
                categoria = 'Alivios de caja'
            elif self._renglon1_combo.currentText() == 'Monto a rendir (-)':
                categoria = 'A rendir'
            elif self._renglon1_combo.currentText() == 'Rendición adeudada (+)':
                categoria = 'Rendiciones adeudadas'
            elif self._renglon1_combo.currentText() == 'Ingreso extraordinario (+)':
                categoria = 'Ingresos extraordinarios'
            elif self._renglon1_combo.currentText() == 'Seleccione el tipo de movimiento':
                categoria = ''
            
            # Si se seleccionó alguna categoría:
            if categoria:
                # Leer el renglón 2
                transaccion = self._renglon2_line.text()
                # Validar que no haya quedado en blanco
                if transaccion:
                    pass
                else:
                    QMessageBox.critical(
                        self,
                        'ERROR!',
                        f"Los campos marcados con un asterisco son obligatorios.",
                        buttons=QMessageBox.Ok,
                        )
            
                # Leer el reglón 3
                descripcion = self._renglon3_line.text()
                # Validar que no haya quedado en blanco
                if descripcion:
                    pass
                else:
                    QMessageBox.critical(
                        self,
                        'ERROR!',
                        f"Los campos marcados con un asterisco son obligatorios.",
                        buttons=QMessageBox.Ok,
                        )

                # Verificar si se trata de un movimiento de ingreso o egreso y hacer NULL el valor opuesto     
                if self._renglon1_combo.currentText()[-2] == '-':
                    ingreso = 'NULL'
                    try:
                        egreso = float(self._renglon4_line.text())
                        error = False
                    except ValueError:
                        error = True
                        QMessageBox.critical(
                        self,
                        'ERROR!',
                        f"El campo Monto debe ser completado con valores numéricos",
                        buttons=QMessageBox.Ok,
                        )
                elif self._renglon1_combo.currentText()[-2] == '+':
                    egreso = 'NULL'
                    try:
                        ingreso = float(self._renglon4_line.text())
                        error = False
                    except ValueError:
                        error = True
                        QMessageBox.critical(
                        self,
                        'ERROR!',
                        f"El campo Monto debe ser completado con valores numéricos",
                        buttons=QMessageBox.Ok,
                        )
                
                # Leer el renglón 5
                observacion = self._renglon5_text.toPlainText()

                # Obtener la fecha
                dia = str(HOY.day).rjust(2, '0')
                mes = str(HOY.month).rjust(2,'0')
                año = str(HOY.year)

                # Consulta
                query = f"""
    INSERT INTO
    caja(categoria, descripcion, transaccion, ingreso, egreso, observacion, dia, mes, año, id_user)
    VALUES
    ('{categoria}', '{descripcion}', '{transaccion}', {ingreso}, {egreso}, '{observacion}', '{dia}', '{mes}', '{año}', {self._user['id']})
    """
                
                # Ejecutar la consulta
                run_query(DATABASE, query)
                
                # Mostrar un mensaje de confirmación y cerrar la ventana
                QMessageBox.information(
                        self,
                        'Registro ingresado',
                        'El registro fue ingresado con éxito',
                        buttons=QMessageBox.Ok,
                        )
                self.close()
            # Si no se seleccionó ninguna categoría lanzar error
            else:
                QMessageBox.critical(
                    self,
                    'ERROR!',
                    f"Debe seleccionar un tipo de movimiento.",
                    buttons=QMessageBox.Ok,
                    )
        except Exception as e:
            # Si ya se mostró un error seguir mostrar nada
            if error:
                pass
            # Sino mostrar un error genérico y grabarlo en el log
            else:
                QMessageBox.critical(
                        self,
                        'ERROR!',
                        f"""
Surgió un error durante el proceso de registro. No se produjeron cambios en la base de datos.

Para ver más detalles e informarlo diríjase a Ayuda -> Registro de errores en la barra de menú
                        """,
                        buttons=QMessageBox.Ok,
                        )
                log_error(parent_error='NuevoCaja', dialog=0)