from recursos.constantes import *
from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap


class About(QDialog):
    """
    Crea un cuadro de diálogo para mostrar la información acerca del programa
    """
    def __init__(self) -> None:
        try:
            super().__init__()
            # CONFIGURACIONES GENERALES DE LA VENTANA
            # Título de la ventana
            self.setWindowTitle(f'Acerca de...')
            # Ícono
            self.setWindowIcon(QIcon(MORELLA_ICON))
            # Tamaño de la ventana
            self.setFixedSize(300, 420)
            # CONTENIDO DE LA VENTANA
            # Logo morella
            self.imagen = QPixmap("docs/system/logo_con_nombre.png")
            # Se escala el logo
            self.imagen_escalada = self.imagen.scaledToHeight(250)
            # Se introduce dentro de un QLabel
            self.label_imagen = QLabel()
            self.label_imagen.setPixmap(self.imagen_escalada)
            self.label_imagen.setAlignment(Qt.AlignCenter)
            # Version del software
            self.label_version = QLabel()
            self.label_version.setText(f'''<b>Versión:</b> {VERSION}''')
            self.label_version.setTextFormat(Qt.RichText)
            # Tipo de versión
            self.label_type_version = QLabel()
            self.label_type_version.setText(f'''<b>Tipo:</b> {TYPE_VERSION}''')
            self.label_type_version.setTextFormat(Qt.RichText)
            # Fecha de lanzamiento
            self.label_release_date = QLabel()
            self.label_release_date.setText(f'''<b>Fecha de lanzamiento:</b> {RELEASE_DATE}''')
            self.label_release_date.setTextFormat(Qt.RichText)
            # Desarrollador
            self.label_developed_by = QLabel()
            self.label_developed_by.setText(f'''<b>Desarrollado por:</b> MF! Soluciones Informáticas''')
            self.label_developed_by.setTextFormat(Qt.RichText)
            # Teléfono de contacto
            self.label_contact_phone_str = QLabel()
            self.label_contact_phone_str.setText(f'''<b>Contacto:</b> {CONTACT_PHONE_STR}''')
            self.label_contact_phone_str.setTextFormat(Qt.RichText)
            # Email
            self.label_contact_mail = QLabel()
            self.label_contact_mail.setText(f'''<b>Email:</b> {CONTACT_EMAIL}''')
            self.label_contact_mail.setTextFormat(Qt.RichText)
            # Web
            self.label_adm_web = QLabel()        
            self.label_adm_web.setText(f'''<b>Web:</b> <a href='{ADM_WEB}'>{ADM_WEB}</a>''')
            self.label_adm_web.setTextFormat(Qt.RichText)
            self.label_adm_web.setTextInteractionFlags(Qt.TextBrowserInteraction)
            self.label_adm_web.setOpenExternalLinks(True)
            # Creación del layout principal
            layout_principal = QVBoxLayout()
            # Alinear al centro todo el layout principal
            layout_principal.setAlignment(Qt.AlignJustify)
            layout_principal.addWidget(self.label_imagen)
            layout_principal.addWidget(self.label_version)
            layout_principal.addWidget(self.label_type_version)
            layout_principal.addWidget(self.label_release_date)
            layout_principal.addWidget(self.label_developed_by)
            layout_principal.addWidget(self.label_contact_phone_str)
            layout_principal.addWidget(self.label_contact_mail)
            layout_principal.addWidget(self.label_adm_web)
            self.setLayout(layout_principal)
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()

