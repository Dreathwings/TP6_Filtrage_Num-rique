#!"C:\ProgramData\radioconda\python.exe"
# -*- coding: utf-8 -*-
import os
from unittest import skip
from PyQt5 import QtWidgets, uic, QtCore, Qt # type: ignore
from PyQt5.QtCore import pyqtSignal , QObject,pyqtSlot
import math
from FILTRE import FILTRE
from GBF import GBF
from GRAPH import GRAPH
from USRP import USRP
from gnuradio import blocks
from gnuradio import gr
import sys

from USRP import USRP

class Communicate(QObject):
    closeApp = pyqtSignal()

class Ui(QtWidgets.QMainWindow,gr.top_block):
    def __init__(self):
        super(Ui, self).__init__()
        """gr.top_block.__init__(self, "TP6", catch_exceptions=True)"""
        path_ui = os.path.abspath(__file__).replace('UI.py','app.ui')
        #print(path_ui)
        uic.loadUi(path_ui, self)
        self.setWindowTitle("TP6 Filtrage Numérique")
        self.ScreenState = 0
        self.GBF_FREQ_SIGNAL = 1000
        self.GBF_AMP_SIGNAL = 0.001
        self.GBF_FREQ_SCAN = 500000
        self.GBF_TYPE_SIGNAL="SINUS"
        self.GBF = GBF(self.GBF_TYPE_SIGNAL,self.GBF_FREQ_SIGNAL,self.GBF_AMP_SIGNAL,self.GBF_FREQ_SCAN)
        
        self.GBF_TIME_UI = GRAPH('SIGNAL/TIME')
        self.GBF_FREQ_UI = GRAPH('SIGNAL/FREQUENCE')
        self.FILTRE = FILTRE()

        self.USRP_TIME_UI = GRAPH('SIGNAL/TIME')
        self.USRP_FREQ_UI = GRAPH('SIGNAL/FREQUENCE')
        
        self.EMETTEUR = USRP('TX',self)
        self.Customer()
        
        self.stop()
        self.start()
        
        self.showMaximized()
        self.show()

    #### UI GETTER
    def getObjet(self,type,name:str):
        item = self.findChild(type, name)
        if item == None:
            raise Exception("[ERROR] Impossible de trouver l'objet voulu")
        out:type = item # type: ignore
        return out
    def getQWidget(self,name:str): return self.getObjet(QtWidgets.QWidget,name)
    def getQDoubleSpin(self,name:str): return self.getObjet(QtWidgets.QDoubleSpinBox,name)
    def getQLabel(self,name:str): return self.getObjet(QtWidgets.QLabel,name)
    def getQCheckBox(self,name:str):return self.getObjet(QtWidgets.QCheckBox,name)
    def getQComboBox(self, name:str):return self.getObjet(QtWidgets.QComboBox,name)
    def getQLineEdit(self, name:str):return self.getObjet(QtWidgets.QLineEdit,name)
    def getQGridLayout(self, name:str):return self.getObjet(QtWidgets.QGridLayout,name)
    def getQToolButton(self, name:str):return self.getObjet(QtWidgets.QToolButton,name)
    def getQHLayout(self, name:str):return self.getObjet(QtWidgets.QHBoxLayout,name)

    ##################
    @staticmethod
    def SPIN_X_COMBO(base,multiply):
        multiply=math.pow(1000,multiply)
        #print(base * multiply)
        return base * multiply
    
    def ON_OFF_Switch(self):
        if self.Item_ON_OFF_BTN.checkState() == 0:
            self.Item_ON_OFF_LBL.setText("ON")
            self.ON_OFF_FM_STATE = 1
        elif self.Item_ON_OFF_BTN.checkState() == 2:
            self.Item_ON_OFF_LBL.setText("OFF")
            self.ON_OFF_FM_STATE = 0

    def GBF_Freq_Signal(self):
        self.GBF_FREQ_SIGNAL = self.SPIN_X_COMBO(self.Item_GBF_FREQ_SIGNAL_BASE.value(),self.Item_GBF_FREQ_SIGNAL_MULTIPLY.currentIndex())
        self.GBF_FREQ_UI.setFreqCenter(self.GBF_FREQ_SIGNAL)
        self.USRP_FREQ_UI.setFreqCenter(self.GBF_FREQ_SIGNAL)
        self.GBF.update(FREQUENCE=self.GBF_FREQ_SIGNAL)
    def GBF_Amp_Signal(self): 
        self.GBF_AMP_SIGNAL = self.Item_GBF_AMP_SIGNAL.value()
        self.GBF.update(AMPLITUDE=self.GBF_AMP_SIGNAL)
    def GBF_Freq_Scan(self): 
        self.GBF_FREQ_SCAN = self.SPIN_X_COMBO(self.Item_GBF_SCAN_BASE.value(),self.Item_GBF_SCAN_MULTIPLY.currentIndex())
        self.GBF.update(SAMPLE_RATE=self.GBF_FREQ_SCAN)
        self.Usrp_Sample()
        self.GBF_TIME_UI.setSampleRate(self.GBF_FREQ_SCAN)
        self.GBF_FREQ_UI.setSampleRate(self.GBF_FREQ_SCAN)

    def GBF_Type_Signal(self): 
        self.GBF_TYPE_SIGNAL = self.Item_GBF_TYPE_SIGNAL.currentText().upper()
        self.GBF.update(SHAPE=self.GBF_TYPE_SIGNAL)
    
    
    
    def Filtre_Forward_On_Off(self):
        #print(self.Item_FILTRE_FORWARD_BTN.checkState())
        self.FILTRE.FORWARD_ON_OFF = self.Item_FILTRE_FORWARD_BTN.checkState()
        self.Filtre_Forward()

    def Filtre_Feedback_On_Off(self):
        #print(self.Item_FILTRE_FEEDBACK_BTN.checkState())
        self.FILTRE.FEEDBACK_ON_OFF = self.Item_FILTRE_FEEDBACK_BTN.checkState()
        self.Filtre_Feedback()

    def Filtre_Forward(self):
        if self.Item_FILTRE_FORWARD_MODE.currentIndex() == 1 and self.FILTRE.FORWARD_file !='':
            type ='FILE'
        else:
            type = self.Item_FILTRE_FORWARD_SHAPE.currentText().upper()
        self.FILTRE.Forward_update(type,
                                self.SPIN_X_COMBO(self.Item_FILTRE_FORWARD_FREQ_H.value(),self.Item_FILTRE_FORWARD_FREQ_H_Multiply.currentIndex()),
                                self.SPIN_X_COMBO(self.Item_FILTRE_FORWARD_FREQ_L.value(),self.Item_FILTRE_FORWARD_FREQ_L_Multiply.currentIndex()),
                                self.SPIN_X_COMBO(self.Item_GBF_SCAN_BASE.value(),self.Item_GBF_SCAN_MULTIPLY.currentIndex()),
                                self.SPIN_X_COMBO(self.Item_FILTRE_FORWARD_TRANSI.value(),self.Item_FILTRE_FORWARD_TRANSI_Multiply.currentIndex()))
        self.USRP_TIME_UI.GUI_SIGNAL.reset()
        self.PLOT_FORWARD.draw()
           
    def Filtre_Feedback(self):
        if self.Item_FILTRE_FEEDBACK_MODE.currentIndex() == 1 and self.FILTRE.FEEDBACK_file !='':
            type ='FILE'
        else:
            type = self.Item_FILTRE_FEEDBACK_SHAPE.currentText().upper()
        self.FILTRE.Feedback_update(type,
                                   self.SPIN_X_COMBO(self.Item_FILTRE_FEEDBACK_FREQ_H.value(),self.Item_FILTRE_FEEDBACK_FREQ_H_Multiply.currentIndex()),
                                   self.SPIN_X_COMBO(self.Item_FILTRE_FEEDBACK_FREQ_L.value(),self.Item_FILTRE_FEEDBACK_FREQ_L_Multiply.currentIndex()),
                                   self.SPIN_X_COMBO(self.Item_GBF_SCAN_BASE.value(),self.Item_GBF_SCAN_MULTIPLY.currentIndex()),
                                   self.SPIN_X_COMBO(self.Item_FILTRE_FEEDBACK_TRANSI.value(),self.Item_FILTRE_FEEDBACK_TRANSI_Multiply.currentIndex()))
        self.USRP_TIME_UI.GUI_SIGNAL.reset()
        self.PLOT_FEEDBACK.draw()

    def Filtre_Forward_FILE(self):
        url = QtCore.QUrl(os.path.dirname(os.path.realpath(__file__)))
        file , check = QtWidgets.QFileDialog().getOpenFileUrl(self, 'Open Filter Taps',url ,"Filter File (*.csv *.filter);;All Files (*)")
        if check:
            path = (str(file).removeprefix("PyQt5.QtCore.QUrl('file:///")).removesuffix("')")
            file = (path.split('/'))[-1]
            #print(path,file)
            out = 'Filtre Taps File: '+file
            self.Item_FILTRE_FORWARD_FILE_BTN.setText(out)
            self.FILTRE.FORWARD_file = path
            self.Filtre_Forward()

    def Filtre_Feedback_FILE(self):
        url = QtCore.QUrl(os.path.dirname(os.path.realpath(__file__)))
        file , check = QtWidgets.QFileDialog().getOpenFileUrl(self, 'Open Filter Taps',url ,"Filter File (*.csv *.filter);;All Files (*)")
        if check:
            path = (str(file).removeprefix("PyQt5.QtCore.QUrl('file:///")).removesuffix("')")
            file = (path.split('/'))[-1]
            #print(path,file)
            out = 'Filtre Taps File: '+file
            self.Item_FILTRE_FEEDBACK_FILE_BTN.setText(out)
            self.FILTRE.FEEDBACK_file = path
            self.Filtre_Feedback()

    def Usrp_Sample(self):
        if self.EMETTEUR.IsConnected:
            self.USRP_SAMPLE = self.SPIN_X_COMBO(self.Item_GBF_SCAN_BASE.value(),self.Item_GBF_SCAN_MULTIPLY.currentIndex())
            self.USRP_TIME_UI.setSampleRate(self.USRP_SAMPLE)
            self.USRP_FREQ_UI.setSampleRate(self.USRP_SAMPLE)
            self.EMETTEUR.set_TX_sample_rate(self.USRP_SAMPLE)

    def Usrp_Porteuse(self):
        if self.EMETTEUR.IsConnected:
            self.USRP_PORTEUSE = self.SPIN_X_COMBO(self.Item_USRP_PORTEUSE_BASE.value(),self.Item_USRP_PORTEUSE_MULTY.currentIndex())
            self.EMETTEUR.set_TX_centre_freq(self.USRP_PORTEUSE)

    def Usrp_Gain(self):
        if self.EMETTEUR.IsConnected:
            self.USRP_GAIN = self.Item_USRP_GAIN.value()
            self.EMETTEUR.set_TX_gain(self.USRP_GAIN)

    def Usrp_On_Off(self):
        if self.EMETTEUR.IsConnected:
            self.USRP_ON_OFF_STATE = self.Item_USRP_ON_OFF.checkState()
            if not self.USRP_ON_OFF_STATE:
                print("[INFO] Enabling USRP")
                self.EMETTEUR.set_On_Off(True)
                
            else:
                print("[INFO] Disabling USRP")
                self.EMETTEUR.set_On_Off(False)

    def Usrp_Reset(self):
        print("[INFO] Reseting USRP")
        print("[INFO] Disabling USRP")
        
        self.EMETTEUR.set_On_Off(False)
        #self.disconnect(self.EMETTEUR.data_tank)# type: ignore
        #del self.EMETTEUR.SINK # type: ignore
        Usrp_label=self.getQLabel('USRP_LABEL')
        Usrp_label.setStyleSheet("background: red;")

    #@pyqtSlot(name='USRP_Connect')
    def USRP_connect(self):
        self.EMETTEUR.Sink_Connection()
        self.connect((self.EMETTEUR.data_tank,0),(self.EMETTEUR.SINK,0)) # type: ignore
        Usrp_label=self.getQLabel('USRP_LABEL')
        Usrp_label.setStyleSheet("background:green;")
        self.Usrp_Sample()
        self.Usrp_Porteuse()
        self.Usrp_Gain()
        if self.EMETTEUR.board == 'NI2900':
            self.EMETTEUR.SINK.start()# type: ignore
            
            
    def Connection(self):
        self.connect((self.GBF.SIGNAL,0),(self.GBF.GBF_SELECTOR,0))
        self.connect((self.GBF.NOISE,0),(self.GBF.GBF_SELECTOR,1))

        self.connect((self.GBF.GBF_SELECTOR,0),(self.GBF_TIME_UI.GUI_SIGNAL,0))
        self.connect((self.GBF.GBF_SELECTOR,0),(self.GBF_FREQ_UI.GUI_SIGNAL,0))

        self.connect((self.GBF.GBF_SELECTOR,0),(self.FILTRE.FILTRE,0))

        self.connect((self.FILTRE.FILTRE,0),(self.COPY_USRP_SINK,0))
        self.connect((self.FILTRE.FILTRE,0),(self.EMETTEUR.copy,0))
        
        self.connect((self.COPY_USRP_SINK,0),(self.USRP_FREQ_UI.GUI_SIGNAL,0))
        self.connect((self.COPY_USRP_SINK,0),(self.USRP_TIME_UI.GUI_SIGNAL,0))
        self.connect((self.EMETTEUR.copy,0), (self.EMETTEUR.converteur, 0), (self.EMETTEUR.data_tank, 0)) # type: ignore

    def Customer(self):
        print('[INFO] INIT UI')
        #/// RECUP DES OBJETS TYPER
        self.Item_ON_OFF_BTN = self.getQCheckBox('ON_OFF_BTN')
        self.Item_ON_OFF_LBL = self.getQLabel('ON_OFF_LBL')
        ### GBF ###
        self.Item_GBF_TYPE_SIGNAL = self.getQComboBox('GBF_SHAPE')
        self.Item_GBF_FREQ_SIGNAL_BASE = self.getQDoubleSpin('GBF_FREQ_SIGNAL')
        self.Item_GBF_FREQ_SIGNAL_MULTIPLY = self.getQComboBox('GBF_FREQ_SIGNAL_MULTIPLY')
        self.Item_GBF_AMP_SIGNAL = self.getQDoubleSpin('GBF_AMP_SIGNAL')
        self.Item_GBF_SCAN_BASE = self.getQDoubleSpin('GBF_SCAN_BASE')
        self.Item_GBF_SCAN_MULTIPLY = self.getQComboBox('GBF_SCAN_MULTIPLY')

        self.Item_GBF_SIGNAL_REPR_TIME = self.getQGridLayout('GBF_TIME_LAYOUT')
        self.Item_GBF_SIGNAL_REPR_FREQ = self.getQGridLayout('GBF_FREQ_LAYOUT')
        
        self.Item_GBF_SIGNAL_REPR_TIME.addWidget(self.GBF_TIME_UI.getWidget())
        self.Item_GBF_SIGNAL_REPR_FREQ.addWidget(self.GBF_FREQ_UI.getWidget())
        #///FILTRE ITEM FIR///
        self.Item_FILTRE_FORWARD_BTN =self.getQCheckBox('FORWARD_BTN')
        
        self.Item_FILTRE_FORWARD_MODE = self.getQComboBox('FILTRE_FIR_MODE')
        self.Item_FILTRE_FORWARD_FILE_BTN = self.getQToolButton('FIR_FILE_BTN')
        self.Item_FILTRE_FORWARD_SHAPE = self.getQComboBox('FILTRE_FIR_SHAPE')
        self.Item_FILTRE_FORWARD_FREQ_H = self.getQDoubleSpin('FILTRE_FIR_FREQ_H')
        self.Item_FILTRE_FORWARD_FREQ_H_Multiply = self.getQComboBox('FILTRE_FIR_FREQ_H_Multiply')
        self.Item_FILTRE_FORWARD_FREQ_L = self.getQDoubleSpin('FILTRE_FIR_FREQ_L')
        self.Item_FILTRE_FORWARD_FREQ_L_Multiply = self.getQComboBox('FILTRE_FIR_FREQ_L_Multiply')
        self.Item_FILTRE_FORWARD_TRANSI = self.getQDoubleSpin('FILTRE_FIR_FREQ_TRANSI')
        self.Item_FILTRE_FORWARD_TRANSI_Multiply = self.getQComboBox('FILTRE_FIR_FREQ_TRANSI_Multiply')
        self.Item_FILTRE_FORWARD_PLOT = self.getQGridLayout('FILTRE_FIR_PLOT')
        self.PLOT_FORWARD = self.FILTRE.get_forward_widget()
        self.Item_FILTRE_FORWARD_PLOT.addWidget(self.PLOT_FORWARD)
        #///FILTRE ITEM IIR///
        self.Item_FILTRE_FEEDBACK_BTN =self.getQCheckBox('FEEDBACK_BTN')
        self.Item_FILTRE_FEEDBACK_MODE = self.getQComboBox('FILTRE_IIR_MODE')
        self.Item_FILTRE_FEEDBACK_FILE_BTN = self.getQToolButton('IIR_FILE_BTN')
        self.Item_FILTRE_FEEDBACK_SHAPE = self.getQComboBox('FILTRE_IIR_SHAPE')
        self.Item_FILTRE_FEEDBACK_FREQ_H = self.getQDoubleSpin('FILTRE_IIR_FREQ_H')
        self.Item_FILTRE_FEEDBACK_FREQ_H_Multiply = self.getQComboBox('FILTRE_IIR_FREQ_H_Multiply')
        self.Item_FILTRE_FEEDBACK_FREQ_L = self.getQDoubleSpin('FILTRE_IIR_FREQ_L')
        self.Item_FILTRE_FEEDBACK_FREQ_L_Multiply = self.getQComboBox('FILTRE_IIR_FREQ_L_Multiply')
        self.Item_FILTRE_FEEDBACK_TRANSI = self.getQDoubleSpin('FILTRE_IIR_FREQ_TRANSI')
        self.Item_FILTRE_FEEDBACK_TRANSI_Multiply = self.getQComboBox('FILTRE_IIR_FREQ_TRANSI_Multiply')
        self.Item_FILTRE_FEEDBACK_PLOT = self.getQGridLayout('FILTRE_IIR_PLOT')
        self.PLOT_FEEDBACK = self.FILTRE.get_feedback_widget()
        self.Item_FILTRE_FEEDBACK_PLOT.addWidget(self.PLOT_FEEDBACK)


        ###///USRP///###
        self.Item_USRP_PORTEUSE_BASE = self.getQDoubleSpin('USRP_PORTEUSE_BASE')
        self.Item_USRP_PORTEUSE_MULTY = self.getQComboBox('USRP_PORTEUSE_MULTY')

        self.Item_USRP_SAMPLE_BASE = self.getQDoubleSpin('USRP_SAMPLE_BASE')
        self.Item_USRP_SAMPLE_MULTY = self.getQComboBox('USRP_SAMPLE_MULTY')

        self.Item_USRP_GAIN = self.getQDoubleSpin('USRP_GAIN')

        self.Item_USRP_ON_OFF = self.getQCheckBox('ON_OFF_BTN')

        ###########
        #///USRP///
        self.Item_USRP_SIGNAL_REPR_TIME = self.getQGridLayout('USRP_TIME_LAYOUT')
        self.Item_USRP_SIGNAL_REPR_FREQ = self.getQGridLayout('USRP_FREQ_LAYOUT')

        self.Item_USRP_SIGNAL_REPR_TIME.addWidget(self.USRP_TIME_UI.getWidget())
        self.Item_USRP_SIGNAL_REPR_FREQ.addWidget(self.USRP_FREQ_UI.getWidget())
        #/// MISE EN PLACE DES SIGNAUX
        self.Item_ON_OFF_BTN.stateChanged.connect(self.ON_OFF_Switch)
        ### GBF ###
        self.Item_GBF_AMP_SIGNAL.editingFinished.connect(self.GBF_Amp_Signal)
        self.Item_GBF_FREQ_SIGNAL_BASE.valueChanged.connect(self.GBF_Freq_Signal)
        self.Item_GBF_FREQ_SIGNAL_MULTIPLY.currentIndexChanged.connect(self.GBF_Freq_Signal)
        self.Item_GBF_SCAN_BASE.valueChanged.connect(self.GBF_Freq_Scan)
        self.Item_GBF_SCAN_MULTIPLY.currentIndexChanged.connect(self.GBF_Freq_Scan)
        self.Item_GBF_TYPE_SIGNAL.currentIndexChanged.connect(self.GBF_Type_Signal)
        ###########
        self.Item_FILTRE_FORWARD_BTN.stateChanged.connect(self.Filtre_Forward_On_Off)

        self.Item_FILTRE_FORWARD_FILE_BTN.clicked.connect(self.Filtre_Forward_FILE)

        self.Item_FILTRE_FORWARD_MODE.currentIndexChanged.connect(self.Filtre_Forward)
        self.Item_FILTRE_FORWARD_SHAPE.currentIndexChanged.connect(self.Filtre_Forward)

        self.Item_FILTRE_FORWARD_FREQ_H.valueChanged.connect(self.Filtre_Forward)
        self.Item_FILTRE_FORWARD_FREQ_H_Multiply.currentIndexChanged.connect(self.Filtre_Forward)

        self.Item_FILTRE_FORWARD_FREQ_L.valueChanged.connect(self.Filtre_Forward)
        self.Item_FILTRE_FORWARD_FREQ_L_Multiply.currentIndexChanged.connect(self.Filtre_Forward)

        self.Item_FILTRE_FORWARD_TRANSI.valueChanged.connect(self.Filtre_Forward)
        self.Item_FILTRE_FORWARD_TRANSI_Multiply.currentIndexChanged.connect(self.Filtre_Forward)
        ###########
        ###########
        self.Item_FILTRE_FEEDBACK_BTN.stateChanged.connect(self.Filtre_Feedback_On_Off)
        self.Item_FILTRE_FEEDBACK_FILE_BTN.clicked.connect(self.Filtre_Feedback_FILE)
        
        self.Item_FILTRE_FEEDBACK_MODE.currentIndexChanged.connect(self.Filtre_Feedback)
        self.Item_FILTRE_FEEDBACK_SHAPE.currentIndexChanged.connect(self.Filtre_Feedback)

        self.Item_FILTRE_FEEDBACK_FREQ_H.valueChanged.connect(self.Filtre_Feedback)
        self.Item_FILTRE_FEEDBACK_FREQ_H_Multiply.currentIndexChanged.connect(self.Filtre_Feedback)

        self.Item_FILTRE_FEEDBACK_FREQ_L.valueChanged.connect(self.Filtre_Feedback)
        self.Item_FILTRE_FEEDBACK_FREQ_L_Multiply.currentIndexChanged.connect(self.Filtre_Feedback)

        self.Item_FILTRE_FEEDBACK_TRANSI.valueChanged.connect(self.Filtre_Feedback)
        self.Item_FILTRE_FEEDBACK_TRANSI_Multiply.currentIndexChanged.connect(self.Filtre_Feedback)
        ##########

        self.Item_USRP_PORTEUSE_BASE.valueChanged.connect(self.Usrp_Porteuse)
        self.Item_USRP_PORTEUSE_MULTY.currentIndexChanged.connect(self.Usrp_Porteuse)

        self.Item_USRP_SAMPLE_BASE.valueChanged.connect(self.Usrp_Sample)
        self.Item_USRP_SAMPLE_MULTY.currentIndexChanged.connect(self.Usrp_Sample)

        self.Item_USRP_GAIN.valueChanged.connect(self.Usrp_Gain)

        self.Item_USRP_ON_OFF.stateChanged.connect(self.Usrp_On_Off)

        a = Communicate()
        self.EMETTEUR.SetupVar("SignalConnection",a)
        #print(self.EMETTEUR.SignalConnection)
        self.EMETTEUR.SignalConnection.closeApp.connect(self.USRP_connect) # type: ignore

        self.GBF_TIME_UI.GUI_SIGNAL.enable_autoscale(True)# type: ignore
        
        self.USRP_TIME_UI.GUI_SIGNAL.enable_autoscale(True)# type: ignore

        self.GBF_FREQ_UI.GUI_SIGNAL.set_y_axis(-125,0)
        #self.GBF_TIME_UI.GUI_SIGNAL.set_y_axis(-100,0)
        
        self.USRP_FREQ_UI.GUI_SIGNAL.set_y_axis(-125,0)
        #self.USRP_TIME_UI.GUI_SIGNAL.set_y_axis(-100,0)

        ##########
        #/// VARIABLE ETAT UI
        self.ON_OFF_FM_STATE = self.ON_OFF_Switch()

        self.Filtre_Forward()
        self.Filtre_Feedback()
        self.Usrp_Sample()
        self.Usrp_Porteuse()
        self.Usrp_Gain()
        ###########
        ##################################################
        # Connections
        #################################################
        


        self.COPY_USRP_SINK = blocks.throttle( gr.sizeof_float*1, (6969696969), True, 0 if "auto" == "auto" else max( int(float(0.1) * (6969696969)) if "auto" == "time" else int(0.1), 1) ) # type: ignore


        self.Connection()
        
        if self.EMETTEUR.IsConnected:
            self.USRP_connect()
        
        self.EMETTEUR.IsConnected = True
        print("[INFO] Initialisation terminé")

    def keyPressEvent(self, event):
        Key = {16777233:'END',16777274:'MAXIMIZE',16777268:'REBOOT_USRP',16777220:'',16777251:'',16777249:"",16777221:""}
        Key.setdefault(0,'NULL')
        #print(event,event.key())
        if event.key() in Key.keys():
            if Key[event.key()] == 'END':#END
                print("[INFO] Killing ")
                self.destroy()
            elif Key[event.key()] == 'MAXIMIZE':#F11
                if self.ScreenState == 0:
                    print("[INFO] Set Screen to FULLSCREEN")
                    self.showFullScreen()
                    self.ScreenState = 1
                else:
                    print("[INFO] Set Screen to MAXIMIZED")
                    self.showMaximized()
                    self.ScreenState = 0
            elif Key[event.key()] == 'REBOOT_USRP':#F4
                self.USRP_connect()
            elif Key[event.key()] == '':#ALT / CTRL / ENTRER
                a=1
            event.accept()
        else:
            print("[WARNING] La clef {} n'a pas d'action liée".format(event.key()))
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = Ui()
    sys.exit(app.exec_())