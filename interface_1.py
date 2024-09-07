from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QRadioButton, QHBoxLayout, QListWidget, \
    QGridLayout, QPushButton, QLineEdit, QLabel, QFileDialog


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        #----------------------------------------- Ventana Principal --------------------------------------------------#
        # Configuracion de la ventana principal (Titulo, Tamaño, Icono, etc)
        self.setWindowTitle('(STR) Dragon Limit Changer V1.0.0')
        self.setFixedSize(450, 450)
        # self.setWindowIcon(QtGui.QIcon('shrek.png')) todo: Considerar Icono del programa

        #------------------------------------------ Variables de Clase ------------------------------------------------#
        self.seleccion = ''             #<--- Guarda la seleccion del programa a modificar
        self.path = None                #<--- Contiene el path al que se le hara referencia para modificar los archivos
        self.limits_path = ''           #<--- Contiene el path para el reemplazo de limites en UNIX
        self.una_path = ''              #<--- Contiene el path para la modificacion del .una y creacion del .bak en UNIX
        self.limits_path_prod = ''      #<--- Contiene el path de los limites nuevos de PROD
        self.limits_path_qa = ''        #<--- Contiene el path de los limites nuevos de QA
        self.limits_path_reflow = ''    #<--- Contiene el path de los limites nuevos de REFLOW

        #------------------------------------------ Layout y Etiqueta--------------------------------------------------#
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

        #---------------------------------------- Llamada de funciones ------------------------------------------------#
        # Funcion Layout 1: Seleccion de Plataforma (DRG, RED, RDB) y Configuracion del layout
        self._layout1()
        # Funcion Layout 2: Despliegue de lista de Programas
        self._layout2()
        # Funcion Layout 3: Obtiene los archivos de limites
        self._layout3()
        # Funcion Layout 4: Accionar del boton
        self._layout4()

        #-------------------------------------- Publicacion Layout Principal ------------------------------------------#
        # Agregamos el Layout principal al componente y publicamos
        self.componente.setLayout(self.layout_principal)
        self.setCentralWidget(self.componente)

        # ----------------------------- Termina el codigo de la clase Ventana Principal -------------------------------#

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
            self.seleccion = 'mnt/dragon/str/U442/'


        elif s == 'RED':
            print('RED Seleccionado')
            self.seleccion = 'mnt/dragon/str/U1909/'
        else:
            print('RDB Seleccionado')
            self.seleccion = 'mnt/dragon/str/U1909DB/'

    def _layout2(self):
        #----------------------------------------- Layout 2 Lista Programa --------------------------------------------#
        # Creamos el Layout 2 que despliega la lista de programas
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

        # Creamos una lista con el Widget Qlist
        lista = QListWidget()
        # Se le da el tamaño para mostrar
        lista.setFixedSize(430, 150)

        # for i in range(1,16):
        #     lista.addItem(str(i))
        lista.addItems(['RED_53924_11_QUAD_C','RED_53925_11_QUAD_B','RED_53921_16_QUAD_A','RED_53920_18_QUAD_A3','RED_53926_17_QUAD_A2',
                        'RED_53923_11_QUAD_A4','RED_53747_11_QUAD_B3','RED_53748_11_QUAD_B1','RED_53759_11_QUAD_A5', 'RED_53761_11_QUAD_C1'])
        # En la siguiente accion checa el elemento seleccinado por el usuario y lo manda a la funcion _seleccion_programa
        lista.currentItemChanged.connect(self._seleccion_programa)

        # Agregamos el Widget y Publicamos el layout 2 en el layout principal
        self.layout2.addWidget(lista)
        self.layout_principal.addLayout(self.layout2)
        #------------------------------------------- Fin Layout 2 -----------------------------------------------------#

    def _seleccion_programa(self, elemento):
        # Se concatena y guarda el string en la variable de clase self.path
        self.path = self.seleccion + elemento.text()
        print(f' path: {self.seleccion + elemento.text()}')

    def _layout3(self):
        #--------------------------------------- Layout 3 botones de limites ------------------------------------------#
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
        etiqueta_botones.setFixedSize(100,12)
        self.layout3.addWidget(etiqueta_botones,0,0)

        # Creamos los botones para elegir los archivos de limites (PROD, QA, REFLOW)
        self.prod = QPushButton('PROD')
        self.qa = QPushButton('QA')
        self.reflow = QPushButton('REFLOW')

        # Añadimos los botones al layout3
        self.layout3.addWidget(self.prod,1,0)
        self.layout3.addWidget(self.qa,2,0)
        self.layout3.addWidget(self.reflow,3,0)

        # Se agrega la activacion del boton
        self.prod.clicked.connect(lambda: self._archivos_limites('PROD'))
        self.qa.clicked.connect(lambda: self._archivos_limites('QA'))
        self.reflow.clicked.connect(lambda: self._archivos_limites('REFLOW'))

        # Creamos el cuadro de texto para display del path del archivo
        self.prod_textbox = QLineEdit()
        self.qa_textbox = QLineEdit()
        self.reflow_textbox = QLineEdit()

        # Se hacen de solo lectura
        self.prod_textbox.setReadOnly(True)
        self.qa_textbox.setReadOnly(True)
        self.reflow_textbox.setReadOnly(True)

        # Añadimos el cuadro de texto al Layout3
        self.layout3.addWidget(self.prod_textbox,1,1)
        self.layout3.addWidget(self.qa_textbox,2,1)
        self.layout3.addWidget(self.reflow_textbox,3,1)



        # Publicamos Layout3 en layout_principal
        self.layout_principal.addLayout(self.layout3)
        # --------------------------------------------- Fin Layout 3  -------------------------------------------------#
#https://www.geeksforgeeks.org/copy-and-replace-files-in-python/
#https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QFileDialog.html#PySide2.QtWidgets.PySide2.QtWidgets.QFileDialog.getOpenFileName
    def _archivos_limites(self, a):
        # Hacemos la seleccion de archivos
        if a == 'PROD':
            print('Abriendo ventana para PROD')
            # Selecciona el archivo de limites y guarda el path en la variable
            fileProd = QFileDialog.getOpenFileName(self,self.tr("PROD Limits"), "", self.tr("Limit Files (*PROD*.csv)"))
            print(fileProd[0])
            path_prod = fileProd[0]
            # Se guarda el path de los archivos nuevos para uso posterior
            self.limits_path_prod = path_prod
            # Se manda a imprimir el path en la caja de texto respectiva
            self.prod_textbox.setText(path_prod)

        elif a == 'QA':
            print('Abriendo ventana para QA ')
            # Selecciona el archivo de limites y guarda el path en la variable
            fileQA = QFileDialog.getOpenFileName(self, self.tr("QA Limits"), "",self.tr("Limit Files (*QA*.csv)"))
            print(fileQA[0])
            path_qa = fileQA[0]
            # Se guarda el path de los archivos nuevos para uso posterior
            self.limits_path_qa = path_qa
            # Se manda a imprimir el path en la caja de texto respectiva
            self.qa_textbox.setText(path_qa)


        else:
            print('Abriendo ventana para REFLOW ')
            # Selecciona el archivo de limites y guarda el path en la variable
            fileReflow = QFileDialog.getOpenFileName(self, self.tr("REFLOW Limits"), "",self.tr("Limit Files (*REFLOW*.csv)"))
            print(fileReflow[0])
            path_reflow = fileReflow[0]
            # Se guarda el path de los archivos nuevos para uso posterior
            self.limits_path_reflow = path_reflow
            # Se manda a imprimir el path en la caja de texto respectiva
            self.reflow_textbox.setText(path_reflow)

    def _layout4(self):
        # Creamos layout para el boton de accion y su configuracion
        self.layout4 = QHBoxLayout()
        self.boton = QPushButton('Start')
        self.boton.setFixedSize(50,25)
        # Conectamos la activacion del boton para realizar un accion a traves de la funcion _boton_accion
        self.boton.clicked.connect(self._boton_accion)

        # Agregamos el boton y publicamos el layout
        self.layout4.addWidget(self.boton)
        self.layout_principal.addLayout(self.layout4)

    def _boton_accion(self):
        print('Se acciono boton')

    def reemplazo_archivo_una(self):
        pass

    def reemplazo_archivos_limites(self):
        pass

if __name__ == '__main__':
    app = QApplication()
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
