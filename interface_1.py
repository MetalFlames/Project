import datetime
import os.path
import re
import sys
from ftplib import FTP

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QRadioButton, QHBoxLayout, QListWidget, \
    QGridLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox
import shutil


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        # ----------------------------------------- Ventana Principal --------------------------------------------------
        # Configuracion de la ventana principal (Titulo, Tamaño, Icono, etc)
        self.setWindowTitle('(STR) Dragon Limits Uploader V1.0.0')
        self.setFixedSize(450, 450)
        # self.setWindowIcon(QtGui.QIcon('shrek.png')) todo: Considerar Icono del programa

        # ------------------------------------------ Variables de Clase ------------------------------------------------

        self.seleccion = None           # <--- Guarda el path de la seleccion de plataforma
        self.plataforma = None          # <--- Guarda la plataforma seleccionada "DRG, RED, RDB"
        self.path = None                # <--- Contiene el path al que se le hara referencia para modificar los archivos
        self.limits_path = ''           # <--- Contiene el path para el reemplazo de limites en UNIX
        self.una_path = ''              # <--- Contiene el path para la modificacion del .una y creacion del .bak en UNIX
        self.limits_path_prod = None    # <--- Contiene el path de los limites nuevos de PROD
        self.limits_path_qa = None      # <--- Contiene el path de los limites nuevos de QA
        self.limits_path_reflow = None  # <--- Contiene el path de los limites nuevos de REFLOW
        self.numero_parte = None        # <--- Guarda el numero de parte para futuras comparaciones
        self.lista = []                 # <--- Guarda la lista de programas encontradas en el directorio
        self.host = 'm7rdb54'           # <--- Tester para conexion FTP
        self.user = 'drgoper'           # <--- Usuario FTP
        self.password = 'drgoper'       # <--- Pass FTP
        self.platform_validation = None # Variable para validar que se utiliza la misma plataforma (Porgrama vs Limites)

        # ========================================= Variables de Validacion ============================================
        self.bak = 0                            # <--- Bandera de la primera corrida
        self.numero_parte_validacion = 'XXXX'   # <--- Guarda el PN para evitar que se suban archivos a otro folder

        # ------------------------------------------ Layout y Etiqueta--------------------------------------------------
        # Creamos componente generico donde se publicaran los layouts
        self.componente = QWidget()
        # Creamos el layout principal
        self.layout_principal = QVBoxLayout()

        # Creacion de etiqueta y settings
        etiqueta_plataforma = QLabel('Select Platform')
        fuente_plataforma = etiqueta_plataforma.font()
        fuente_plataforma.setPointSize(10)
        etiqueta_plataforma.setFont(fuente_plataforma)
        etiqueta_plataforma.setFixedSize(100, 12)

        # Se agrega etiqueta al layout_principal
        self.layout_principal.addWidget(etiqueta_plataforma)

        # ---------------------------------------- Llamada de funciones ------------------------------------------------
        # Funcion Layout 1: Seleccion de Plataforma (DRG, RED, RDB) y Configuracion del layout
        self._layout1()
        # Funcion Layout 2: Despliegue de lista de Programas
        self._layout2()
        # Funcion Layout 3: Obtiene los archivos de limites
        self._layout3()
        # Funcion Layout 4: Accionar del boton
        self._layout4()

        # -------------------------------------- Publicacion Layout Principal ------------------------------------------
        # Agregamos el Layout principal al componente y publicamos
        self.componente.setLayout(self.layout_principal)
        self.setCentralWidget(self.componente)

        # ----------------------------- Termina el codigo de la clase Ventana Principal --------------------------------

    def _layout1(self):
        # ------------------------------------------ Layout Seleccion -------------------------------------------------#
        # Creamos el layout 1 para seleccion de programa (DRG, RED, RDB)
        self.layout1 = QHBoxLayout()
        self.layout1.setAlignment(Qt.AlignHCenter)
        self.layout1.setSpacing(100)

        # Creamos QRadioButton(s) para la seleccion de programa (DRG, RED, RDB)
        self.drg = QRadioButton('DRG')
        self.red = QRadioButton('RED')
        self.rdb = QRadioButton('RDB')

        # Conecta al evento de seleccion y se manda a la funcion seleccion_programa(self) utilizando una funcion lambda
        self.drg.toggled.connect(lambda: self._seleccion_plataforma('DRG'))
        self.red.toggled.connect(lambda: self._seleccion_plataforma('RED'))
        self.rdb.toggled.connect(lambda: self._seleccion_plataforma('RDB'))

        # Agregamos QRadioButton(s) para la seleccion de programa (DRG, RED, RDB)
        self.layout1.addWidget(self.drg)
        self.layout1.addWidget(self.red)
        self.layout1.addWidget(self.rdb)

        # Agregamos el layout1 al principal
        self.layout_principal.addLayout(self.layout1)
        # --------------------------------------- Fin Layout Seleccion ------------------------------------------------#

    def _seleccion_plataforma(self, s):
        # Filtramos la seleccion y retornamos el path de los programas a desplegar en la lista
        if s == 'DRG':
            print('DRG Seleccionado')
            self.seleccion = '/mnt/dragon/str/U442/'
            self.plataforma = 'DRG'

            try:
                # Realizamos la conexion FTP para extraer los elementos del directorio y guardarlos para ser desplegados (DRG)
                with FTP(host=self.host, timeout=5) as ftp:
                    ftp.login(user=self.user, passwd=self.password)
                    ftp.cwd(self.seleccion)
                    self.lista = ftp.nlst()
                    print(self.lista)

                    self._caja_seleccion()

            except Exception as e:
                dialogo = QMessageBox.warning(self,'Alert: Platform Selection',f'Error to connect to server: {e} \nContact Administrator')
                print(f'Error al conectar con el servidor: {e}')

        elif s == 'RED':
            # Filtramos la seleccion y retornamos el path de los programas a desplegar en la lista
            print('RED Seleccionado')
            self.seleccion = '/mnt/dragon/str/U1909/'
            self.plataforma = 'RED'

            try:
                # Realizamos la conexion FTP para extraer los elementos del directorio y guardarlos para ser desplegados (RED)
                with FTP(host=self.host, timeout=5) as ftp:
                    ftp.login(user=self.user, passwd=self.password)
                    ftp.cwd(self.seleccion)
                    self.lista = ftp.nlst()
                    print(self.lista)
                    # refrescamos la lista por medio del siguiente metodo
                    self._caja_seleccion()

            except Exception as e:
                dialogo = QMessageBox.warning(self,'Alert: Platform Selection',f'Error to connect to server: {e} \nContact Administrator')
                print(f'Error al conectar con el servidor: {e}')

        else:
            # Filtramos la seleccion y retornamos el path de los programas a desplegar en la lista
            print('RDB Seleccionado')
            self.seleccion = '/mnt/dragon/str/U1909DB/'
            self.plataforma = 'RDB'

            try:
                # Realizamos la conexion FTP para extraer los elementos del directorio y guardarlos para ser desplegados (RDB)
                with FTP(host=self.host, timeout=5) as ftp:
                    ftp.login(user=self.user, passwd=self.password)
                    ftp.cwd(self.seleccion)
                    self.lista = ftp.nlst()
                    print(self.lista)
                    # refrescamos la lista por medio del siguiente metodo
                    self._caja_seleccion()

            except Exception as e:
                dialogo = QMessageBox.warning(self,'Alert: Platform Selection',f'Error to connect to server: {e} \nContact Administrator')
                print(f'Error al conectar con el servidor: {e}')

    def _layout2(self):
        # ----------------------------------------- Layout 2 Lista Programa --------------------------------------------
        # Creamos el Layout 2 que despliega la self.qlista de programas
        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignHCenter)

        # Etiqueta Titulo Lista de Programa
        etiqueta_programa = QLabel('Select Program')
        fuente_programa = etiqueta_programa.font()
        fuente_programa.setPointSize(10)
        etiqueta_programa.setFont(fuente_programa)
        # etiqueta_programa.setAlignment(Qt.AlignTop)
        etiqueta_programa.setFixedSize(100, 12)
        self.layout2.addWidget(etiqueta_programa)

        # Creamos una lista con el Widget Qlist que sera llamada despues por un metodo (caja_seleccion)
        self.qlista = QListWidget()
        # Se le da el tamaño para mostrar
        self.qlista.setFixedSize(430, 150)

        self.layout_principal.addLayout(self.layout2)
        # ------------------------------------------- Fin Layout 2 -----------------------------------------------------

    def _caja_seleccion(self):
        # Se limpia el contenido de la lista
        self.qlista.clear()

        # Añadimos los elementos a la lista
        self.qlista.addItems(self.lista)

        # En la siguiente accion checa el elemento seleccinado por el usuario y lo manda a la funcion seleccion_programa
        self.qlista.currentItemChanged.connect(self._seleccion_programa)

        # Agregamos el Widget y Publicamos el layout 2 en el layout principal
        self.layout2.addWidget(self.qlista)

    def _seleccion_programa(self, elemento):
        # Se concatena y guarda el string en la variable de clase self.path
        self.path = self.seleccion + elemento.text()
        # Se guarda el nombre programa para utilizarse en validacion (Que coincida el PN de Programa/limites/.una)
        programa = elemento.text()

        # Guardamos la plataforma seleccionada
        self.platform_validation = programa[0:4]

        if programa[5] == 'A':
            self.numero_parte = programa[4:10]
        elif 'SKY' in programa:
            self.numero_parte = programa[7:15]
        else:
            self.numero_parte = programa[4:12]

        # --------------- For DEBUG ------------------#
        print(f'Programa: {programa}')
        print(f'Numero de Parte: {self.numero_parte}')
        print(f'Path: {self.path}')
        # --------------- For DEBUG ------------------#

    def _layout3(self):
        # --------------------------------------- Layout 3 botones de limites ------------------------------------------
        # Creamos el Layout 3 que recibe los limites
        self.layout3 = QGridLayout()
        self.layout3.setAlignment(Qt.AlignHCenter)
        self.layout3.setHorizontalSpacing(10)

        # Etiqueta de Limites
        etiqueta_botones = QLabel('Select Limit Files')
        fuente_etiqueta_botones = etiqueta_botones.font()
        fuente_etiqueta_botones.setPointSize(10)
        etiqueta_botones.setFont(fuente_etiqueta_botones)
        etiqueta_botones.setAlignment(Qt.AlignVCenter)
        etiqueta_botones.setFixedSize(100, 12)
        self.layout3.addWidget(etiqueta_botones, 0, 0)

        # Creamos los botones para elegir los archivos de limites (PROD, QA, REFLOW)
        self.prod = QPushButton('PROD')
        self.qa = QPushButton('QA')
        self.reflow = QPushButton('REFLOW')

        # Añadimos los botones al layout3
        self.layout3.addWidget(self.prod, 1, 0)
        self.layout3.addWidget(self.qa, 2, 0)
        self.layout3.addWidget(self.reflow, 3, 0)

        # Se agrega la activacion del boton
        self.prod.clicked.connect(lambda: self._seleccion_archivos_limites('PROD'))
        self.qa.clicked.connect(lambda: self._seleccion_archivos_limites('QA'))
        self.reflow.clicked.connect(lambda: self._seleccion_archivos_limites('REFLOW'))

        # Creamos el cuadro de texto para display del path del archivo
        self.prod_textbox = QLineEdit()
        self.qa_textbox = QLineEdit()
        self.reflow_textbox = QLineEdit()

        # Se hacen de solo lectura
        self.prod_textbox.setReadOnly(True)
        self.qa_textbox.setReadOnly(True)
        self.reflow_textbox.setReadOnly(True)

        # Añadimos el cuadro de texto al Layout3
        self.layout3.addWidget(self.prod_textbox, 1, 1)
        self.layout3.addWidget(self.qa_textbox, 2, 1)
        self.layout3.addWidget(self.reflow_textbox, 3, 1)

        # Publicamos Layout3 en layout_principal
        self.layout_principal.addLayout(self.layout3)
        # --------------------------------------------- Fin Layout 3  -------------------------------------------------#

    def _seleccion_archivos_limites(self, a):
        # [Metodo] Se recibe la señal del boton para subir los limites y se filtra para realizar la accion de cada boton

        try:
            #Guardamos el numero de parte en la variable programa para
            programa = self.numero_parte[0:5]
            print(programa)

        except Exception as e:
            dialogo = QMessageBox.warning(self, 'Alert: Limit Selection Method',
                                          f'Please Select Program\n'
                                          f'ErrorType {e}')

        if a == 'PROD':
            print('Abriendo ventana para PROD')
            # Selecciona el archivo de limites y guarda el path en la variable
            try:
                fileProd = QFileDialog.getOpenFileName(self, self.tr("PROD Limits"), "",
                                                       self.tr(f"Limit Files (*{self.platform_validation}*PROD*{programa}*.csv)"))

                # --------------- For DEBUG ------------------#
                print(fileProd[0])
                path_prod = fileProd[0]
                file_name = os.path.basename(path_prod)
                print(file_name)
                # --------------- For DEBUG ------------------#

                # Se guarda el path de los archivos nuevos para uso posterior
                self.limits_path_prod = path_prod

                # Validacion por nombre incorrecto en archivo (Vacio)
                if self.limits_path_qa == '':
                    self.limits_path_qa = None

                # Se manda a imprimir el path en la caja de texto respectiva
                self.prod_textbox.setText(path_prod)

                # DEBUG
                self.path_to_work = os.path.dirname(self.limits_path_prod) + '/'
                print(f'Path to work on: {self.path_to_work}')

                # todo [Variable de validacion] Se guarda para comparacion archivo limites vs path del programa
                file_name_prod = os.path.basename(self.limits_path_prod)
                if 'SKY' in file_name_prod:
                    self.numero_parte_validacion = file_name_prod[12:17]
                    print(f'Numero de validacion: {self.numero_parte_validacion}')
                else:
                    self.numero_parte_validacion = file_name_prod[9:14] # Checar SKY
                    print(f'Numero de validacion: {self.numero_parte_validacion}')

            except Exception as e:
                dialogo = QMessageBox.warning(self,'Alert: Limit Selection Method',f'Failed to open file: {e}')

        elif a == 'QA':
            print('Abriendo ventana para QA ')

            try:
                # Selecciona el archivo de limites y guarda el path en la variable
                fileQA = QFileDialog.getOpenFileName(self, self.tr("QA Limits"), "",
                                                     self.tr(f"Limit Files (*{self.platform_validation}*QA*{programa}*.csv)"))
                # --------------- For DEBUG ------------------#
                print(fileQA[0])
                # --------------- For DEBUG ------------------#

                path_qa = fileQA[0]
                # Se guarda el path de los archivos nuevos para uso posterior
                self.limits_path_qa = path_qa

                # Validacion por nombre incorrecto en archivo (Vacio)
                if self.limits_path_qa == '' :
                    self.limits_path_qa = None

                # Se manda a imprimir el path en la caja de texto respectiva
                self.qa_textbox.setText(path_qa)

            except Exception as e:
                dialogo = QMessageBox.warning(self,'Alert: Limit Selection Method',f'Failed to open file: {e}')

        else:
            print('Abriendo ventana para REFLOW ')
            try:
                # Selecciona el archivo de limites y guarda el path en la variable
                fileReflow = QFileDialog.getOpenFileName(self, self.tr("3XREFLOW Limits"), "",
                                                         self.tr(f"Limit Files (*{self.platform_validation}*REFLOW*{programa}*.csv)"))
                # --------------- For DEBUG ------------------#
                print(fileReflow[0])
                # --------------- For DEBUG ------------------#

                path_reflow = fileReflow[0]
                # Se guarda el path de los archivos nuevos para uso posterior
                self.limits_path_reflow = path_reflow

                # Validacion por nombre incorrecto en archivo (Vacio)
                if self.limits_path_reflow == '':
                    self.limits_path_reflow = None

                # Se manda a imprimir el path en la caja de texto respectiva
                self.reflow_textbox.setText(path_reflow)

            except Exception as e:
                dialogo = QMessageBox.warning(self,'Alert: Limit Selection Method',f'Failed to open file: {e}')

    def _layout4(self):
        # Creamos layout para el boton de accion y su configuracion
        self.layout4 = QHBoxLayout()
        self.boton = QPushButton('Start')
        self.boton.setFixedSize(50, 25)

        # Conectamos la activacion del boton para realizar una accion a traves de la funcion _boton_accion
        self.boton.clicked.connect(lambda: self._boton_accion())

        # Agregamos el boton y publicamos el layout
        self.layout4.addWidget(self.boton)
        self.layout_principal.addLayout(self.layout4)

    def _boton_accion(self):
        # todo [Validacion] Validamos que los limites sean seleccionados antes de proceder a mover los archivos
        if self.limits_path_qa is not None and self.limits_path_prod is not None and self.limits_path_reflow is not None:
            if self.platform_validation in self.limits_path_prod and self.limits_path_qa and self.limits_path_reflow:
                # todo [Validacion] Se valida que no se cambio el path del programa por accidente
                if self.numero_parte_validacion in self.path:
                    print('Se acciono boton')
                    self.una_extract()
                    self.reemplazo_archivos_limites()
                    self.reemplazo_archivo_una()
                    self._una_send()
                    dialogo = QMessageBox.information(self, 'Information',
                                                  f'Limits Uploaded')
                    sys.exit(1)
                else:
                    dialogo = QMessageBox.warning(self, 'Alert: Button Action', f'Part Number for Program and Limits does not match')
            else:
                dialogo = QMessageBox.warning(self, 'Alert: Button Action',
                                              f'Limits doesnt correspond for the platform selected')
        else:
            dialogo = QMessageBox.warning(self,'Alert: Button Action',f'Limits not selected')

    def reemplazo_archivos_limites(self):

        # --------------- For DEBUG ------------------#
        print('Se copiaron los limites')
        print(f'Path source PROD: {self.limits_path_prod}')
        print(f'Path source QA: {self.limits_path_qa}')
        print(f'Path source REFLOW: {self.limits_path_reflow}')
        # --------------- For DEBUG ------------------#

        dst_path = self.path + '/Limits/'
        print(f'Path de limites: {dst_path}') # <-- For Debug

        # Guardamos el path de donde tomaremos los limites y agregamos el destino de los limites
        src_prod = self.limits_path_prod
        src_qa = self.limits_path_qa
        src_reflow = self.limits_path_reflow

        # Se realiza el cambio de los archivos en las siguientes 3 lineas
        # shutil.copy(src_prod, dst_path)
        # shutil.copy(src_qa, dst_path)
        # shutil.copy(src_reflow, dst_path)

        # ---------------------------------------------------- For Debug -----------------------------------------------
        print('Comienza Debug')
        destination_path = '/mnt/dragon/engineering/German/Python_App/Limit_Changer/RED_53924_11_QUAD_DUMMY/Limits'
        source_path_prod = src_prod
        source_path_qa = src_qa
        source_path_reflow = src_reflow

        file_name_prod = os.path.basename(self.limits_path_prod)
        file_name_qa = os.path.basename(self.limits_path_qa)
        file_name_reflow = os.path.basename(self.limits_path_reflow)

        # Realiza la conexion FTP y manda los archivos de limites al servidor
        try:
            with FTP(host=self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                ftp.cwd(destination_path)
                with open(source_path_prod,'rb') as file:
                    ftp.storbinary(f'STOR {file_name_prod}', file)

        except Exception as e:
            dialogo = QMessageBox.warning(self,'Alert: Replace File Method',f' Failed to open file: {e} \nContact Administrator')

        try:
            with FTP(host=self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                ftp.cwd(destination_path)
                with open(source_path_qa,'rb') as file:
                    ftp.storbinary(f'STOR {file_name_qa}', file)

        except Exception as e:
            dialogo = QMessageBox.warning(self,'Alert: Replace File Method',f' Failed to open file: {e} \nContact Administrator')

        try:
            with FTP(host=self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                ftp.cwd(destination_path)
                with open(source_path_reflow,'rb') as file:
                    ftp.storbinary(f'STOR {file_name_reflow}', file)

        except Exception as e:
            dialogo = QMessageBox.warning(self,'Alert: Replace File Method',f' Failed to open file: {e} \nContact Administrator')

        print('Termina Debug')
        # ---------------------------------------------------- For Debug -----------------------------------------------

    def reemplazo_archivo_una(self):
        # [Metodo] Reemplaza en el .una el nombre con los nuevos archivos de limites, con ayuda de 2 metodos auxiliares
        print('Se modifico el .una')

        # self.una_extract()

        # Asignamos el patron de busqueda para reemplazar en el .una
        pattern = r'    __CSVFile = "../Limits/'                            # <----  El patron base
        search_pattern_prod = pattern + self.plataforma + '_PROD'           # <----  agregamos 'prod' al patron base
        search_pattern_qa = pattern + self.plataforma + '_QA'               # <----  agregamos 'qa' al patron base
        search_pattern_reflow = pattern + self.plataforma + '_3XREFLOW'     # <----  El patron 'reflow' al patron base

        # Guardamos el File Name para agregar al patron de busqueda
        file_name_prod = os.path.basename(self.limits_path_prod)
        file_name_qa = os.path.basename(self.limits_path_qa)
        file_name_reflow = os.path.basename(self.limits_path_reflow)

        # Creamos el string de reemplazo
        replace_pattern_prod = pattern + file_name_prod + '";' + '\n'
        replace_pattern_qa = pattern + file_name_qa + '";' + '\n'
        replace_pattern_reflow = pattern + file_name_reflow + '";' + '\n'

        # ------------------------------------------------ DEBUG -------------------------------------------------------
        print(f'Pattern prod: {search_pattern_prod}')
        print(f'Pattern qa: {search_pattern_qa}')
        print(f'Pattern reflow: {search_pattern_reflow}')

        print(f'File name prod: {file_name_prod}')
        print(f'File name qa: {file_name_qa}')
        print(f'File name reflow: {file_name_reflow}')

        print(f'String Final PROD: {replace_pattern_prod}')
        print(f'String Final QA: {replace_pattern_qa}')
        print(f'String Final REFLOW: {replace_pattern_reflow}')
        # ----------------------------------------------- END DEBUG ----------------------------------------------------



        # ------------------------------------------------ DEBUG -------------------------------------------------------
        una = self.path_to_work + self.numero_parte +'.una'

        # Regresa la lista de elementos en el directorio
        # files = [f for f in os.listdir(path)]
        # print(files)
        # ----------------------------------------------- END DEBUG ----------------------------------------------------

        # Obtenemos el tiempo actual para agregarlo al .una.bak
        current_time = datetime.datetime.now()
        time_stamp = str(int(current_time.timestamp()))

        # Valida si es la primera vez que se ha corrido el programa para generar el .bak
        if self.bak == 0:
            backup_path = una + '.' + time_stamp + '.bak'
            shutil.copyfile(una, backup_path)
            self.bak = 1

        # Llamamos al metodo para buscar la linea que se reemplazara
        line_2_replace_prod = self.buscar_pattern(search_pattern_prod, una)
        line_2_replace_qa = self.buscar_pattern(search_pattern_qa, una)
        line_2_replace_reflow = self.buscar_pattern(search_pattern_reflow, una)

        # Usamos el metodo para modificar las lineas en el .una
        print('Metodo buscar dentro del archivo')
        self.reemplazar_pattern(una, line_2_replace_prod, replace_pattern_prod)
        self.reemplazar_pattern(una, line_2_replace_qa, replace_pattern_qa)
        self.reemplazar_pattern(una, line_2_replace_reflow, replace_pattern_reflow)

    def buscar_pattern(self, search_pattern, una):
        # [Metodo] Recibe el patron a buscar y el path del .una

        # ----------------------------------------------- END DEBUG ----------------------------------------------------
        una = self.path_to_work + self.numero_parte +'.una'
        # ----------------------------------------------- END DEBUG ----------------------------------------------------

        # Abre el archivo y lee en busca del patron
        try:
            with open(una, 'r') as file:
                for l_no, line in enumerate(file):
                    if search_pattern in line:
                        line_to_replace = line
            # Mandamos de regreso la linea que sera reemplazada
            return line_to_replace

        except Exception as e:
            dialogo = QMessageBox.warning(self,'Alert: Search Pattern Method',f' Failed to open file: {e} \nContact Administrator')

    def reemplazar_pattern(self, file_path, search_pattern, replace_pattern):
        # [Metodo] encuentra el patron deseado y lo reemplaza

        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                updated_contents = re.sub(search_pattern, replace_pattern, file_contents)

            with open(file_path, 'w') as file:
                file.write(updated_contents)

        except Exception as e:
            dialogo = QMessageBox.warning(self, 'Alert: Pattern Replace Method', f'Failed to open file: {e} \nContact Administrator')


    def una_extract(self):
        # ---------------------------------------------- .UNA Extraction ----------------------------------------------#
        # Creamos el nombre del archivo .una de manera dinamica
        una = self.path + '/Programs/' + self.numero_parte + '.una'
        file_name_una = self.numero_parte + '.una'

        print('Creamos conexion para extraer UNA')

        try:
            with FTP(host=self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                # ftp.cwd(una)

                # For Debug
                ftp.cwd('/mnt/dragon/engineering/German/Python_App/Limit_Changer/RED_53924_11_QUAD_DUMMY/Program/')

                print(f'Abrimos archivo el archivo: {file_name_una}, para escribir en el folder {una}\n'
                      f'Limits path prod: {self.limits_path_prod}')
                with open(file_name_una, 'wb') as file:
                    ftp.retrbinary(f'RETR {file_name_una}',
                                   open(self.path_to_work + file_name_una,'wb').write)
                print('Se descargo archivo')

        except Exception as e:
            dialogo = QMessageBox.warning(self,'Alert',f'Error to connect to server: {e} \nContact Administrator')
        # ---------------------------------------------- .UNA Extraction ----------------------------------------------#

    def _una_send(self):
        dst_path = self.path + '/Program/'
        destination_path = '/mnt/dragon/engineering/German/Python_App/Limit_Changer/RED_53924_11_QUAD_DUMMY/Program/'
        source_path = self.path_to_work
        file_name = self.numero_parte

        try:
            with FTP(host=self.host) as ftp:
                ftp.login(user=self.user, passwd=self.password)
                ftp.cwd(destination_path)

                for filename in os.listdir(self.path_to_work):
                    if filename.endswith('.una') or filename.endswith('.bak'):
                        local_path = os.path.join(source_path, filename)

                        with open(local_path,'rb') as file:
                            ftp.storbinary(f'STOR {filename}', file)

        except Exception as e:
            dialogo = QMessageBox.warning(self,'Alert',f'Error to connect to server: {e} \nContact Administrator')

if __name__ == '__main__':
    app = QApplication()
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
