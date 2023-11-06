#!"C:\ProgramData\radioconda\python.exe"
import time
from gnuradio import filter
from gnuradio.filter import firdes # type: ignore
from gnuradio.filter import window  # type: ignore
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FILTRE():
    def __init__(self,GAIN=1,SAMPLE_RATE=32000,F_LOW=10,F_HIGH=100,file="") -> None:

        #*//// FORWARD \\\\*
        self.FORWARD_ON_OFF = 2
        self.FORWARD_TAPS = [1]
        self.FORWARD_GAIN = GAIN
        self.FORWARD_SAMPLE_RATE = SAMPLE_RATE
        self.FORWARD_F_LOW = F_LOW
        self.FORWARD_F_HIGH = F_HIGH
        self.FORWARD_F_TRANSI = SAMPLE_RATE/8
        self.FORWARD_WINDOW = window.WIN_RECTANGULAR    # type: ignore
        self.FORWARD_BETA = 6.76
        self.FORWARD_file = file
        self.FORWARD_mode = 'PASSE-BANDE'
        #*//// FEEDBACK \\\\*
        self.FEEDBACK_ON_OFF = 2
        self.FEEDBACK_TAPS = [1]
        self.FEEDBACK_GAIN = GAIN
        self.FEEDBACK_SAMPLE_RATE = SAMPLE_RATE
        self.FEEDBACK_F_LOW = F_LOW
        self.FEEDBACK_F_HIGH = F_HIGH
        self.FEEDBACK_F_TRANSI = SAMPLE_RATE/8
        self.FEEDBACK_WINDOW = window.WIN_RECTANGULAR    # type: ignore
        self.FEEDBACK_BETA = 6.76
        self.FEEDBACK_file = file
        self.FEEDBACK_mode = 'PASSE-BANDE'
        print('INIT FILTRE')
        self.FILTRE = filter.iir_filter_ffd(self.FORWARD_TAPS,self.FEEDBACK_TAPS,False) # type: ignore
        #self.FILTRE.name = 'FILTRE'

        self.Forward_plot_init()
        self.Feedback_plot_init()
        
    def Forward_update(self,mode=None,f_low=None,f_high=None,sample_rate=None,f_transi=None):
        if mode != None:
            self.FORWARD_mode = mode
        if f_low != None:
            self.FORWARD_F_LOW = f_low
        if f_high != None:
            self.FORWARD_F_HIGH = f_high
        if sample_rate != None:
            self.FORWARD_SAMPLE_RATE = sample_rate
        if f_transi != None:
            self.FORWARD_F_TRANSI = f_transi
        if self.FORWARD_ON_OFF == 2:
            self.FORWARD_TAPS = [1]
        else:
            self.FORWARD_TAPS = self.Forward_Current_Taps()
        self.FILTRE.set_taps(self.FORWARD_TAPS,self.FEEDBACK_TAPS)
        self.Forward_plot_update()

    def Feedback_update(self,mode=None,f_low=None,f_high=None,sample_rate=None,f_transi=None):
        if mode != None:
            self.FEEDBACK_mode = mode
        if f_low != None:
            self.FEEDBACK_F_LOW = f_low
        if f_high != None:
            self.FEEDBACK_F_HIGH = f_high
        if sample_rate != None:
            self.FEEDBACK_SAMPLE_RATE = sample_rate
        if f_transi != None:
            self.FEEDBACK_F_TRANSI = f_transi
        if self.FEEDBACK_ON_OFF == 2:
            self.FEEDBACK_TAPS = [1]
        else:
            self.FEEDBACK_TAPS = self.Feedback_Current_Taps()
        self.FILTRE.set_taps(self.FORWARD_TAPS,self.FEEDBACK_TAPS)
        self.Forward_plot_update()
        self.Feedback_plot_update()

    def Forward_Current_Taps(self):
        try:
            if self.FORWARD_mode == 'PASSE-BAS':
                return firdes.low_pass(self.FORWARD_GAIN,self.FORWARD_SAMPLE_RATE,
                                    self.FORWARD_F_HIGH,
                                    self.FORWARD_F_TRANSI,
                                    self.FORWARD_WINDOW,
                                    self.FORWARD_BETA)
            elif self.FORWARD_mode == 'PASSE-HAUT':
                return firdes.high_pass(self.FORWARD_GAIN,self.FORWARD_SAMPLE_RATE,self.FORWARD_F_HIGH,self.FORWARD_F_TRANSI,self.FORWARD_WINDOW,self.FORWARD_BETA)
            elif self.FORWARD_mode == 'PASSE-BANDE':
                return firdes.band_pass(self.FORWARD_GAIN,self.FORWARD_SAMPLE_RATE, self.FORWARD_F_HIGH,self.FORWARD_F_LOW,self.FORWARD_F_TRANSI,self.FORWARD_WINDOW,self.FORWARD_BETA)
            elif self.FORWARD_mode == 'COUPE-BANDE':
                return firdes.band_reject(self.FORWARD_GAIN,self.FORWARD_SAMPLE_RATE,self.FORWARD_F_HIGH,self.FORWARD_F_LOW, self.FORWARD_F_TRANSI,self.FORWARD_WINDOW,self.FORWARD_BETA)
            elif self.FEEDBACK_mode == 'FILE':
                return
            elif self.FORWARD_mode == 'FILE':
                txt = open(self.FORWARD_file,"r").read()
                if 'taps' in txt:
                    txt = txt.split('taps,')[2]
                    #print(txt)
                    out = []
                    for int in txt.split(','):
                        out.append(float(int))
                    return out
        except IndexError:
            time.sleep(0.5)
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setWindowTitle("TP Filtrage Numérique")
            msg.setText("""Impossible de mettre a jour le Filtre 1
    Verifiez les parametres """)
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()
            return self.FORWARD_TAPS
        
    def Feedback_Current_Taps(self):
        if self.FEEDBACK_mode == 'PASSE-BAS':
            return firdes.low_pass(self.FEEDBACK_GAIN,self.FEEDBACK_SAMPLE_RATE,self.FEEDBACK_F_HIGH,self.FEEDBACK_F_TRANSI,self.FEEDBACK_WINDOW,self.FEEDBACK_BETA)
        elif self.FEEDBACK_mode == 'PASSE-HAUT':
            return firdes.high_pass(self.FEEDBACK_GAIN,self.FEEDBACK_SAMPLE_RATE,self.FEEDBACK_F_HIGH,self.FEEDBACK_F_TRANSI,self.FEEDBACK_WINDOW,self.FEEDBACK_BETA)
        elif self.FEEDBACK_mode == 'PASSE-BANDE':
            return firdes.band_pass(self.FEEDBACK_GAIN,self.FEEDBACK_SAMPLE_RATE,self.FEEDBACK_F_HIGH, self.FEEDBACK_F_LOW,self.FEEDBACK_F_TRANSI,self.FEEDBACK_WINDOW,self.FEEDBACK_BETA)
        elif self.FEEDBACK_mode == 'COUPE-BANDE':
            return firdes.band_reject(self.FEEDBACK_GAIN,self.FEEDBACK_SAMPLE_RATE,self.FEEDBACK_F_HIGH, self.FEEDBACK_F_LOW,self.FEEDBACK_F_TRANSI,self.FEEDBACK_WINDOW,self.FEEDBACK_BETA)
        elif self.FEEDBACK_mode == 'FILE':
            txt = open(self.FEEDBACK_file,"r").read()
            if 'a' in txt:
                txt = txt.split('a,')[2]
                #print(txt)
                a = []
                for int in txt.split(','):
                    a.append(float(int))
                self.FORWARD_TAPS = a
            if 'b' in txt:
                txt = txt.split('b,')[2]
                #print(txt)
                b = []
                for int in txt.split(','):
                    b.append(float(int))
                return b 
    
    def Forward_plot_init(self):
        i = 1
        x =[]
        y=[]
        self.FORWARD_fig, self.FORWARD_ax = plt.subplots()#figsize=(3,2), constrained_layout=True
        self.FORWARD_ax.grid(True)
        self.FORWARD_fig.set_facecolor('None')
        self.FORWARD_fig.set_alpha(1)
        self.FORWARD_fig.set_edgecolor('black')
        self.FORWARD_fig.subplots_adjust(top=0.95, bottom=0.13, left=0.125, hspace=1.2,right=0.975)
        self.FORWARD_fig.set_linewidth(3.5)
        self.FORWARD_fig.set_edgecolor('black')
        size = len(self.FORWARD_TAPS) # type: ignore
        for i in range(size):
            x.append(i)
            y.append(self.FORWARD_TAPS[i]) # type: ignore
        self.FORWARD_ax.stem(x, y,linefmt='--')
    
    def Feedback_plot_init(self):
        i = 1
        x =[]
        y=[]
        self.FEEDBACK_fig, self.FEEDBACK_ax = plt.subplots()#figsize=(3,2), constrained_layout=True
        self.FEEDBACK_ax.grid(True)
        self.FEEDBACK_fig.set_facecolor('None')
        self.FEEDBACK_fig.set_alpha(1)
        self.FEEDBACK_fig.set_edgecolor('black')
        self.FEEDBACK_fig.subplots_adjust(top=0.95, bottom=0.13, left=0.125, hspace=1.2,right=0.975)
        self.FEEDBACK_fig.set_linewidth(3.5)
        self.FEEDBACK_fig.set_edgecolor('black')
        size = len(self.FEEDBACK_TAPS) # type: ignore
        for i in range(size):
            x.append(i)
            y.append(self.FEEDBACK_TAPS[i]) # type: ignore
        self.FEEDBACK_ax.stem(x, y,linefmt='--')
    
    def Forward_plot_update(self):
        i = 1
        x =[]
        y=[]
        size = len(self.FORWARD_TAPS)# type: ignore
        for i in range(size):
            x.append(i)
            y.append(self.FORWARD_TAPS[i]) # type: ignore
        #print('update forward plot')
        self.FORWARD_ax.clear()
        self.FORWARD_ax.grid(True)
        self.FORWARD_ax.stem(x, y,linefmt='--')

    def Feedback_plot_update(self):
        i = 1
        x =[]
        y=[]
        size = len(self.FEEDBACK_TAPS)# type: ignore
        for i in range(size):
            x.append(i)
            y.append(self.FEEDBACK_TAPS[i]) # type: ignore
        self.FEEDBACK_ax.clear()
        self.FEEDBACK_ax.grid(True)
        self.FEEDBACK_ax.stem(x, y,linefmt='--')

    def get_forward_widget(self):
        return FigureCanvas(self.FORWARD_fig)
    def get_feedback_widget(self):
        return FigureCanvas(self.FEEDBACK_fig)