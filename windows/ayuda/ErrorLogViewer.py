from recursos.constantes import *
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QDialog, QTextEdit
from PySide6.QtGui import QIcon, QPixmap



class ErrorLogViewer(QDialog):
    """
    Crea un cuadro de diálogo donde se vuelca el archivo donde se almacena el informe de errores del prograa y se le brinda al usuario la 
    opción de enviarlo por mail al administrador de sistema
    """
    def __init__(self) -> None:
        try:
            super().__init__()
            # CONFIGURACIONES GENERALES DE LA VENTANA
            # Título de la ventana
            self.setWindowTitle(f'Log de errores')
            # Ícono
            self.setWindowIcon(QIcon(MORELLA_ICON))
            # Tamaño de la ventana
            self.resize(600, 600)
            
            # CONTENIDO DE LA VENTANA
            layout_principal = QVBoxLayout()
            titulo = QLabel('Informe de errores: ')
            self.errores = QTextEdit()
            layout_botones = QHBoxLayout()
            boton_cerrar = QPushButton('Cerrar')
            boton_enviar = QPushButton('Enviar al administrador de sistemas')
            layout_principal.addWidget(titulo)
            layout_principal.addWidget(self.errores)
            layout_botones.addWidget(boton_cerrar)
            layout_botones.addWidget(boton_enviar)
            layout_principal.addLayout(layout_botones)
            self.setLayout(layout_principal)

            # CARGA DE ARCHIVO ERROR.LOG
            with open(ERROR_LOG_PATH, 'r') as arch:
                error_log = arch.readlines()
            lines = ''
            for line in error_log:
                lines += line
            self.errores.setText(lines)
            self.errores.setReadOnly(True)

            # ACCIONES DE BOTONES
            boton_cerrar.clicked.connect(self.close)
            boton_enviar.clicked.connect(self._send_email)
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()

    def _send_email(self):
        """
        Esta función envía el archivo error.log, que almacena el informe de los errores del programa, por mail y luego lo vacía
        
        NOTA: Por el momento sólo vacía el archivo.
        """

        # Creación de la ventana de diálogo
        self.confirmacion = QMessageBox()
        self.confirmacion.setWindowTitle(f'Email enviado con éxito')
        self.confirmacion.setWindowIcon(QIcon(MORELLA_ICON))
        self.confirmacion.setText('El email fue enviado correctamente. Gracias por informar los errores.')
        self.confirmacion.setIconPixmap(QPixmap("docs/system/icons/ok.png"))
        self.confirmacion.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.confirmacion.exec()
        # Vaciado del archivo error.log
        arch = open(ERROR_LOG_PATH, 'w')
        arch.close()
        self.errores.clear()