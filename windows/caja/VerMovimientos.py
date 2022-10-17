from recursos.constantes import *
from windows.models.GenericSubWindow import GenericSubWindow
from windows.caja.BuscarCaja import BuscarCaja
from windows.caja.VerDetallesCaja import VerDetallesCaja
from windows.caja.NuevoCaja import NuevoCaja
from windows.caja.EditarCaja import EditarCaja
from windows.caja.EliminarCaja import EliminarCaja


class VerMovimientos(GenericSubWindow): 
    def __init__(self, user) -> None:
        try:
            super().__init__()
            # DATOS USUARIO
            self._user = user
            # CONFIGURACIONES GENERALES DE LA VENTANA
            # Título de la ventana
            self.setWindowTitle(f'Movimientos de caja')

            # MODELOS
            models = {
                'buscar_registro': BuscarCaja,
                'ver_detalles': VerDetallesCaja,
                'nuevo_registro': NuevoCaja,
                'editar_registro': EditarCaja,
                'eliminar_registro': EliminarCaja,
            }
            # CONTENIDO DE LA VENTANA
            # Toolbar de CRUD
            self._tabla = self._table_view()
            self._toolbar = self._crud_toolbar(self._user, self._tabla, models, SOLO_ICONO)
            # Tabla
            query = f"""
SELECT c.id, categoria, descripcion, transaccion, ingreso, egreso, observacion, dia, mes, año, cerrada, u.user_name
FROM caja c
JOIN usuarios u
ON c.id_user = u.id
ORDER BY c.id;
"""
            header_labels = [
                'ID',
                'CATEGORÍA',
                'DESCRIPCIÓN',
                'TRANSACCIÓN',
                'INGRESO',
                'EGRESO',
                'OBSERVACIONES',
                'DÍA',
                'MES',
                'AÑO',
                'CERRADA',
                'USUARIO',
            ]
            self._toolbar.set_refresh_query(query)
            self._toolbar.set_header_labels(header_labels)
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error(parent_error='VerMovimientos')
    
