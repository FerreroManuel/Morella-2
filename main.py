import subprocess
from recursos.constantes import *
from recursos.funciones_globales import id_app, run_query, acc_documentacion
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QStatusBar, QLabel, QLineEdit, QMessageBox, QMdiArea, )
from PySide6.QtGui import (QIcon, QPixmap, QAction, QPalette, QColor, )
from PySide6.QtCore import Qt
from windows.caja.VerMovimientos import VerMovimientos
from windows.ayuda.About import About
from windows.ayuda.ErrorLogViewer import ErrorLogViewer

# Generación de un identificador de aplicación
id_app()


class mdiArea(QMdiArea):
    def __init__(self) -> None:
        try:
            super().__init__()
            # self.setBackground(QBrush(QPixmap('docs/system/bkg/bkg1.8.png')))
            self.setBackground(QColor(0, 0, 0, 0))
            # self.setBackground(QBrush(QPixmap(BACKGROUND_FILE)))
            # self.setFixedSize()
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()

class MainWindow(QMainWindow):
    """
    Esta clase crea la ventana principal del sistema. 
    Debe recibir obligatoriamente el ID del usuario que está operando con él.
    """

    _datos_usuario = {}

    def __init__(self, id_usuario) -> None:
        try:
            super().__init__()
            # CONFIGURACIONES GENERALES DE LA VENTANA
            self.setStyleSheet("QMainWindow{"+f"background-image: url('{BACKGROUND_DYNAMIC_FILE}'); background-repeat: no-repeat"+"}")
            # Título de la ventana
            self.setWindowTitle(f'Morella v{SHORT_VERSION}    |    MF! Soluciones Informáticas')
            # Ícono
            self.setWindowIcon(QIcon(MORELLA_ICON))
            # Barra de estado (color blanco)
            self.statusbar = QStatusBar(self)
            self.setStatusBar(self.statusbar)
            pal = QPalette()
            pal.setColor(QPalette.Window, Qt.GlobalColor.white)
            self.statusbar.setPalette(pal)
            self.statusbar.setAutoFillBackground(True)
            # Barra de menú
            self._barra_menu()

            # DATOS DEL USUARIO
            self._datos_usuario = self._obtener_datos_usuario(id_usuario)

            # CONTENIDO DE LA VENTANA
            # Área MDI
            self.area_mdi = mdiArea()
            self.setCentralWidget(self.area_mdi)
            
            # Mostrar la ventana maximizada por defecto
            self.showMaximized()
            # Mensaje de bienvenida <-------------------------- ACTIVAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """
            msj_bienvenida = QMessageBox()
            msj_bienvenida.setWindowTitle('Bienvenido/a!')
            msj_bienvenida.setText(f'Hola {self._datos_usuario["nombre"]}, bienvenido a Morella.\nQue tengas un buen día.')
            msj_bienvenida.setWindowIcon(QIcon(ICON))
            msj_bienvenida.exec()
            """
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error(parent_error='MainWindow')


    def _obtener_datos_usuario(self, id_usuario):
        """
        Esta función accede a la base de datos y, a partir del ID del usuario, obtiene ID, nombre, 
        username y nivel de privilegios del usuario y los retorna dentro de un diccionario
        """
        query = f"SELECT nombre, user_name, privilegios FROM usuarios WHERE id = {id_usuario}"
        datos = run_query(DATABASE, query, select=1)
        datos_usuario = {
            'id': id_usuario,
            'nombre': datos[0],
            'username': datos[1],
            'privilegios': datos[2],
        }
        return datos_usuario


    def _barra_menu(self):
        """
        Esta función crea la barra de menú de la ventana principal
        """
        # Creación de la barra de menú
        menu_bar = self.menuBar()

        # --------------------------------------------- Sub-menú Caja ---------------------------------------------
        menu_caja = menu_bar.addMenu('&Caja')
        # Creación de los botones
        ver_mov_caja = QAction('&Movimientos de caja', self)
        # reg_mov_caja = QAction('&Registrar un movimiento', self)
        # mod_mov_caja = QAction('&Modificar un movimiento', self)
        # eli_mov_caja = QAction('&Eliminar un movimiento', self)
        mensual_detallado = QAction('Caja mensual &detallada', self)
        mensual_comprimido = QAction('Caja mensual &comprimida', self)
        mensual_cobrador = QAction('Caja mensual &por cobrador', self)
        historial = QAction('&Movimientos modificados', self)
        debitos = QAction('&Débitos automáticos', self)
        cierre_caja = QAction('&Cierre de caja', self)
        # Adición de los botones al sub-menú
        menu_caja.addAction(ver_mov_caja)
        menu_caja.addSeparator()
        # menu_caja.addActions([reg_mov_caja, mod_mov_caja, eli_mov_caja])
        # menu_caja.addSeparator()
        sm_listados_caja = menu_caja.addMenu('&Listados')
        sm_listados_caja.addActions([mensual_detallado, mensual_comprimido, mensual_cobrador, historial, debitos])
        menu_caja.addSeparator()
        menu_caja.addAction(cierre_caja)
        # Mensaje en barra de estado
        ver_mov_caja.setStatusTip('Ver y realizar acciones sobre los movimientos de caja')
        mensual_detallado.setStatusTip('Imprimir un reporte detallado de caja mensual')
        mensual_comprimido.setStatusTip('Imprimir un reporte comprimido de caja mensual')
        mensual_cobrador.setStatusTip('Imprimir un reporte de caja mensual por cobrador')
        historial.setStatusTip('Generar un reporte de registros editados y eliminados')
        debitos.setStatusTip('Generar un reporte de débitos automáticos')
        cierre_caja.setStatusTip('Realizar el cierre de caja')
        # Asociación del evento Click
        ver_mov_caja.triggered.connect(self._acc_movimientos_caja)
        mensual_detallado.triggered.connect(self._acc_rep_mensual_det)
        mensual_comprimido.triggered.connect(self._acc_rep_mensual_comp)
        mensual_cobrador.triggered.connect(self._acc_rep_mensual_cob)
        historial.triggered.connect(self._acc_rep_historial)
        debitos.triggered.connect(self._acc_rep_debaut)
        cierre_caja.triggered.connect(self._acc_cerrar_caja)
        

        # --------------------------------------------- Sub-menú Ventas ---------------------------------------------
        menu_ventas = menu_bar.addMenu('&Ventas')
        # Creación de los botones
        venta = QAction('&Venta de nicho', self)
        socios = QAction('&Socios', self)
        operaciones = QAction('&Operaciones', self)
        # Adición de los botones al sub-menú
        menu_ventas.addActions([venta, socios, operaciones])
        # Mensaje en barra de estado
        venta.setStatusTip('Realizar la venta de un nicho')
        socios.setStatusTip('Ver y realizar acciones sobre el padrón de asociados')
        operaciones.setStatusTip('Ver y realizar acciones sobre las operaciones')
        # Asociación del evento Click
        venta.triggered.connect(self._acc_venta)
        socios.triggered.connect(self._acc_socios)
        operaciones.triggered.connect(self._acc_operaciones)

        # --------------------------------------------- Sub-menú Rendiciones ----------------------------------------
        menu_rendiciones = menu_bar.addMenu('&Rendiciones')
        # Creación de los botones
        emision = QAction('&Emitir recibos', self)
        reg_pago = QAction('Registrar &pagos', self)
        reimprimir_rec = QAction('&Reimprimir recibo actualizado', self)
        # Adición de los botones al sub-menú
        menu_rendiciones.addActions([emision, reg_pago, reimprimir_rec])
        # Mensaje en barra de estado
        emision.setStatusTip('Emitir recibos para cobradores')
        reg_pago.setStatusTip('Registrar pagos de recibos')
        reimprimir_rec.setStatusTip('Reimprimir un recibo con su respectivo importe actualizado a la fecha')
        # Asociación del evento Click
        emision.triggered.connect(self._acc_emitir_recibos)
        reg_pago.triggered.connect(self._acc_registrar_pagos)
        reimprimir_rec.triggered.connect(self._acc_reimprimir_recibo)

        # --------------------------------------------- Sub-menú Mantenimiento de tablas ----------------------------
        menu_mantenimiento= menu_bar.addMenu('&Mantenimiento de tablas')
        # Creación de los botones
        panteones = QAction('&Panteones', self)
        nichos = QAction('&Nichos', self)
        precios_venta = QAction('Precios de &venta', self)
        precios_mantenimiento = QAction('Precios de &mantenimiento', self)
        cobradores = QAction('&Cobradores', self)
        usuarios = QAction('&Usuarios', self)
        mail = QAction('Cuentas de &email', self)
        # Adición de los botones al sub-menú
        menu_mantenimiento.addActions([panteones, nichos])
        sm_precios = menu_mantenimiento.addMenu('P&recios')
        sm_precios.addActions([precios_venta, precios_mantenimiento])
        menu_mantenimiento.addSeparator()
        menu_mantenimiento.addActions([cobradores, usuarios])
        menu_mantenimiento.addSeparator()
        menu_mantenimiento.addAction(mail)
        # Mensaje en barra de estado
        panteones.setStatusTip('Ver y realizar acciones sobre los panteones')
        nichos.setStatusTip('Ver y realizar acciones sobre los nichos')
        precios_venta.setStatusTip('Ver y realizar acciones sobre los precios de venta')
        precios_mantenimiento.setStatusTip('Ver y realizar acciones sobre los precios del servicio de mantenimiento')
        cobradores.setStatusTip('Ver y realizar acciones sobre el padrón de cobradores')
        usuarios.setStatusTip('Ver y realizar acciones sobre los usuarios operadores del sistema')
        mail.setStatusTip('Ver y realizar acciones sobre las cuentas de email')
        # Asociación del evento Click
        panteones.triggered.connect(self._acc_panteones)
        nichos.triggered.connect(self._acc_nichos)
        precios_venta.triggered.connect(self._acc_precios_venta)
        precios_mantenimiento.triggered.connect(self._acc_precios_mantenimiento)
        cobradores.triggered.connect(self._acc_cobradores)
        usuarios.triggered.connect(self._acc_usuarios)
        mail.triggered.connect(self._acc_mail)

        # --------------------------------------------- Sub-menú Ayuda ----------------------------------------------
        menu_ayuda = menu_bar.addMenu('&Ayuda')
        # Creación de los botones
        documentacion = QAction('&Documentación', self)
        about = QAction('&Acerca de...', self)
        log_error = QAction('&Registro de errores', self)
        # Adición de los botones al sub-menú
        menu_ayuda.addActions([documentacion, about])
        menu_ayuda.addSeparator()
        menu_ayuda.addAction(log_error)
        # Mensaje en barra de estado
        documentacion.setStatusTip('Abrir el manual de usuario')
        about.setStatusTip('Ver la información acerca del programa')
        log_error.setStatusTip('Ver y realizar acciones sobre el registro de errores')
        # Asociación del evento Click
        documentacion.triggered.connect(acc_documentacion)
        about.triggered.connect(self._acc_about)
        log_error.triggered.connect(self._acc_log_error)

    # ACCIONES DE SUB-MENÚ CAJA
    def _acc_movimientos_caja(self):
        """
        Esta función crea una sub-ventana que permite ver y realizar diferentes operaciones sobre los movimientos de caja
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            self.sub_window = VerMovimientos(self._datos_usuario)
            self.area_mdi.addSubWindow(self.sub_window)
            self.sub_window.show()

    def _acc_rep_mensual_det(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    def _acc_rep_mensual_comp(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    def _acc_rep_mensual_cob(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    def _acc_rep_historial(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    def _acc_rep_debaut(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    def _acc_cerrar_caja(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    # ACCIONES DE SUB-MENÚ VENTAS
    def _acc_venta(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    def _acc_socios(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_operaciones(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    # ACCIONES DE SUB-MENÚ RENDICIONES
    def _acc_emitir_recibos(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_registrar_pagos(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_reimprimir_recibo(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    # ACCIONES DE SUB-MENÚ MANTENIMIENTO DE TABLAS
    def _acc_panteones(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_nichos(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_precios_venta(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_precios_mantenimiento(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_cobradores(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_usuarios(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass
    
    def _acc_mail(self):
        """
        Esta función 
        """
        if self.area_mdi.activeSubWindow():
            pass
        else:
            pass

    # ACCIONES DE SUB-MENÚ AYUDA
    def _acc_about(self):
        """
        Esta función crea un diálogo con la información del sistema y el desarrollador
        """
        self._about = About()
        self._about.exec()
    
    def _acc_log_error(self):
        """
        Esta función crea un diálogo donde se muestra el reporte de errores y permite el envío de éste al administrador del sistema
        """
        self._sub_window = ErrorLogViewer()
        self._sub_window.exec()

    def keyPressEvent(self, event):
        """
        Esta función detecta las teclas que se presionan mientras se permanece en la ventana

        F1 -> Muestra la documentación
        """
        if event.key() == Qt.Key_F1:
            acc_documentacion()

class LoginForm(QWidget):
    """
    Crea una ventana con un formulario de acceso para los usuarios del sistema. No se puede ingresar a éste sin poseer un usuario
    y una contraseña activos
    """
    _ult_username = ''
    _contador_pw = 0

    def __init__(self):
        try:
            super().__init__()
            # Título de la ventana
            self.setWindowTitle(f'Iniciar sesión    |    Morella v{SHORT_VERSION}')
            # Ícono
            self.setWindowIcon(QIcon(MORELLA_ICON))
            # Tamaño
            self.setFixedSize(300,300)
            # CUERPO

            # Logo Morella
            image = QPixmap('docs/system/logo_con_nombre.png')
            scaled_image = image.scaledToHeight(200)
            label_image = QLabel()
            label_image.setPixmap(scaled_image)
            label_image.setAlignment(Qt.AlignCenter)

            # Campo Usuario
            self._user_line = QLineEdit()
            self._user_line.setPlaceholderText('Usuario')
            self._user_line.setMaxLength(6)
            self._user_line.returnPressed.connect(self._login)

            # Campo Contraseña
            self._password_line = QLineEdit()
            self._password_line.setPlaceholderText('Contraseña')
            self._password_line.setEchoMode(QLineEdit.EchoMode.Password)
            self._password_line.returnPressed.connect(self._login)
            
            # Botón Iniciar sesión
            self._login_btn = QPushButton('Iniciar sesión')
            self._login_btn.clicked.connect(self._login)
            self._login_btn.setDefault(1)
            
            # Layout
            self._form_layout = QVBoxLayout()
            self._form_layout.addWidget(label_image)
            self._form_layout.addWidget(self._user_line)
            self._form_layout.addWidget(self._password_line)
            self._form_layout.addWidget(self._login_btn)
            self.setLayout(self._form_layout)
        except Exception as e:
            from recursos.funciones_globales import log_error
            log_error()
        

    def _login(self):
        """
        Esta función se encarga de obtener y procesar los datos ingresados en el formulario por el usuario y de informarle a éste de su estado
        y, si los datos son correctos y posee acceso, crea la ventana principal a la cual le retorna el ID del usuario.
        """
        # Lectura del nombre de usuario proporcionado (en minúsculas)
        username = self._user_line.text().lower()
        # Lectura del password proporcionado (case sensitive)
        password = self._password_line.text()
        # Envío de los datos proporcionados a la función check_user
        datos_usuario = self._check_user(username, password)
        # Procesamiento de la respuesta obtenida por parte de la función check_user
        if datos_usuario == 'inexistente':
            # Mensaje usuario inexistente
            QMessageBox.critical(
                self, 
                'ERROR!', 
                f'No existe el usuario {username}', 
                buttons=QMessageBox.Ok
                )
            # Vaciado de los campos de texto
            self._user_line.setText('')
            self._password_line.setText('')
            self._user_line.setFocus()
        elif datos_usuario == 'inactivo':
            # Mensaje usuario inactivo
            QMessageBox.critical(
                self, 
            'ERROR!', 
            f'El usuario {username} se encuentra inactivo. Comuníquese con un administrador.', 
            buttons=QMessageBox.Ok
            )
            # Vaciado de los campos de texto
            self._user_line.setText('')
            self._password_line.setText('')
            self._user_line.setFocus()
        elif datos_usuario == 'bloqueado':
            # Mensaje usuario bloqueado
            QMessageBox.critical(
                self, 
                'ERROR!', 
                f'El usuario {username} se encuentra bloqueado por demasiados intentos de ingreso fallidos. Comuníquese con un administrador.', 
                buttons=QMessageBox.Ok
                )
            # Vaciado de los campos de texto
            self._user_line.setText('')
            self._password_line.setText('')
            self._user_line.setFocus()
        elif datos_usuario == 'pw_incorrecta':
            # Mensaje contraseña incorrecta
            QMessageBox.critical(
                self, 
                'ERROR!', 
                f'La contraseña proporcionada es incorrecta.', 
                buttons=QMessageBox.Ok)
            # Vaciado del campo de contraseña
            self._password_line.setText('')
            self._password_line.setFocus()
            # Bloqueo de usuario luego de 3 intentos fallidos
            if self._contador_pw == 3:
                block_user = f"UPDATE usuarios SET activo = 2 WHERE user_name = '{username}'"
                run_query(DATABASE, block_user)
        else:
            # Si la respuesta de la función check_user es positiva, se crea la ventana principal y se oculta la de login
            self.main_window = MainWindow(datos_usuario)
            self.hide()
            self.main_window.show()


    def _check_user(self, username, password):
        """
        Esta función recibe los datos de login y compara con la información existente en la base de datos.
        -   Una vez que llega a una conclusión sobre la existencia y el estado del nombre de usuario recibido, ésta es retornada.
        -   En caso de recibir un nombre de usuario existente y activo y una contraseña inválida durante tres oportunidades consecutivas
            el usuario es bloqueado
        -   En caso de recibir nombre de usuario y contraseñas válidos para acceder al sistema, la función retorna el ID del usuario
        """
        # Consulta a la base de datos sobre el estado del usuario brindado
        select_activo = f"SELECT activo FROM usuarios WHERE user_name = '{username}'"
        activo = run_query(DATABASE, select_activo, select=1)
        # Si la base de datos no arroja resultados se retorna el estado [inexistente]
        if activo == None:
            return 'inexistente'
        # Si la base de datos arroja el valor 0 se retorna el estado [inactivo]
        elif activo[0] == 0:
            return 'inactivo'
        # Si la base de datos arroja el valor 2 se retorna el estado [bloqueado]
        elif activo[0] == 2:
            return 'bloqueado'
        # Si la base de datos arroja el valor 1 se procede a solicitar a la base de datos la contraseña
        elif activo[0] == 1:
            select_pw = f"SELECT pass FROM usuarios WHERE user_name = '{username}'"
            pw = run_query(DATABASE, select_pw, select=1)
            # Si la contraseña brindada coincide con la devuelta por la base de datos se retorna el ID de usuario
            if pw[0] == password:
                select_datos = f"SELECT id FROM usuarios WHERE user_name = '{username}'"
                id_usuario = run_query(DATABASE, select_datos, select=1)
                return id_usuario[0]
            # Si las contraseñas no coinciden
            else:
                # Si la variable ult_username está vacía: se suma 1 al contador y se graba el nombre de usuario a la variable ult_username
                if self._ult_username == '':
                    self._contador_pw += 1
                    self._ult_username = username
                # Si la variable ult_username es distinta al nombre de usuario brindado, se procede de la misma manera
                elif self._ult_username != username:
                    self._ult_username = username
                    self._contador_pw = 1
                # Si la variable ult_username coincide con el nombre de usuario brindado, se suma 1 al contador
                elif self._ult_username == username:
                    self._contador_pw += 1
                # Se retorna el estado 'pw_incorrecta'
                return 'pw_incorrecta'
            


        

if __name__ == '__main__':

    app = QApplication()
    # login_window = LoginForm()
    # login_window.show()
    main_window = MainWindow(1)
    main_window.show()
    app.exec()
