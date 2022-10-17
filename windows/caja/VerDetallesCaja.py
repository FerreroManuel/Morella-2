from recursos.constantes import *
from recursos.funciones_globales import run_query
from windows.caja.ViewModelCaja import ViewModelCaja
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class VerDetallesCaja(ViewModelCaja):
    """
    Esta clase crea una ventana donde se muestran los detalles de un registro de caja
    """
    def __init__(self, user:dict, id_reg:int) -> None:
        try:
            super().__init__(user, id_reg)
            # CONFIGURACIÓN DE LA VENTANA
            self.setWindowTitle('Ver detalles')
            self.setBaseSize(400, 600)
            # CONEXIÓN CON DB
            query = f"""
SELECT c.id, categoria, descripcion, transaccion, ingreso, egreso, observacion, dia, mes, año, cerrada, u.user_name
FROM caja c
JOIN usuarios u
ON c.id_user = u.id
WHERE c.id = {id_reg};
"""
            datos = run_query(DATABASE, query, FETCHONE)

            # CONTENIDO DE LA VENTANA
            # Renglón 1
            # ID
            self._id_line.setText(str(datos[0]))
            self._id_line.setReadOnly(True)
            # Fecha
            self._fecha_line.setText(f"{datos[7]}{datos[8]}{datos[9]}")
            self._fecha_line.setReadOnly(True)
            # Renglón 2
            # Transacción
            self._transaccion_line.setText(str(datos[3]))
            self._transaccion_line.setReadOnly(True)
            # ¿Cerrada?
            if datos[10] == 1:
                self._cerrada_checkbox.setChecked(True)
                self._cerrada_checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)
            elif datos[10] == 0:
                self._cerrada_checkbox.setChecked(False)
                self._cerrada_checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)
            # Renglón 3
            # Categoría
            self._categoria_line.setText(str(datos[1]))
            self._categoria_line.setReadOnly(True)
            # Descripción
            self._descripcion_line.setText(str(datos[2]))
            self._descripcion_line.setReadOnly(True)
            # Renglón 4
            # Ingreso
            if datos[4]:
                self._ingreso_line.setText(f"{datos[4]:.2f}")
                self._ingreso_line.setReadOnly(True)
            else:
                self._ingreso_label.hide()
                self._ingreso_line.hide()
            # Egreso
            if datos[5]:
                self._egreso_line.setText(f"{datos[5]:.2f}")
                self._egreso_line.setReadOnly(True)
            else:
                self._egreso_label.hide()
                self._egreso_line.hide()
            # Renglon 5
            # Observaciones
            self._observaciones_text.setText(datos[6])
            self._observaciones_text.setReadOnly(True)
            # Renglon 6
            # Usuario
            self._usuario_label = QLabel()
            self._usuario_label.setText(f'<b>Registrado por: {datos[11]}</b>')
            self._usuario_label.setAlignment(Qt.AlignRight)
            self._cuerpo.addWidget(self._usuario_label)
            # Botones
            self._boton_guardar.hide()
            self._boton_eliminar.hide()
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error(parent_error='VerDetallesCaja')