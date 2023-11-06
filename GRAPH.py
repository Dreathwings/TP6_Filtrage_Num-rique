#!"C:/ProgramData/radioconda/python.exe
from flask.scaffold import F
from gnuradio import qtgui
from gnuradio import analog
from PyQt5 import Qt # type: ignore
import sip # type: ignore
from gnuradio import gr
from gnuradio import fft

class GRAPH(gr.top_block):
    availble_type = ['SIGNAL/TIME','SIGNAL/FREQUENCE']
    def __init__(self, TYPE:str,BUFFER_SIZE:int=1024,SAMPLE_RATE:float = 32000,NAME:str = "",INPUTed:int = 1,CentreFreq:int=0) -> None:
        if TYPE == None or TYPE not in GRAPH.availble_type:
            raise Exception('[ERROR] La géneration de graphique est impossible sans selectionné un TYPE compatible: SIGNAL/TIME ou SIGNAL/FREQUENCE')
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.BUFFER_SIZE = BUFFER_SIZE
        self.SAMPLE_RATE = SAMPLE_RATE
        self.NAME = NAME
        self.INPUTed = INPUTed
        self.CENTRE_FREQ = CentreFreq
        if TYPE == 'SIGNAL/TIME':
            self.TYPE = TYPE
            self.TIME_GRAPH_init()
        elif TYPE == 'SIGNAL/FREQUENCE':
            self.TYPE = TYPE
            self.FREQ_GRAPH_init()
        self.WIDGET_GUI_SIGNAL.setStyleSheet('QwtPlotCanvas { background-color: white; border: 1.5px solid black; border-radius: 10px }')

    def FREQ_GRAPH_init(self):
        self.GUI_SIGNAL = qtgui.freq_sink_f( # type: ignore
            self.BUFFER_SIZE,
            fft.window.WIN_RECTANGULAR,# type: ignore
            self.CENTRE_FREQ, #size
            self.SAMPLE_RATE, #samp_rate
            self.NAME, #name
            self.INPUTed, #number of inputs
            None # parent
        )
        self.GUI_SIGNAL.set_update_time(0.10)
        self.GUI_SIGNAL.set_y_axis((-100), 10)
        self.GUI_SIGNAL.set_y_label('Relative Gain', 'dB')
        self.GUI_SIGNAL.set_trigger_mode(qtgui.TRIG_MODE_AUTO, 0.0, 0, "") # type: ignore
        self.GUI_SIGNAL.enable_autoscale(False)
        self.GUI_SIGNAL.enable_grid(True)
        self.GUI_SIGNAL.set_fft_average(1.0)
        self.GUI_SIGNAL.enable_axis_labels(True)
        self.GUI_SIGNAL.enable_control_panel(False)
        self.GUI_SIGNAL.set_fft_window_normalized(True)

        self.GUI_SIGNAL.disable_legend()

        self.GUI_SIGNAL.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.GUI_SIGNAL.set_line_label(i, "Data {0}".format(i))
            else:
                self.GUI_SIGNAL.set_line_label(i, labels[i])
            self.GUI_SIGNAL.set_line_width(i, widths[i])
            self.GUI_SIGNAL.set_line_color(i, colors[i])
            self.GUI_SIGNAL.set_line_alpha(i, alphas[i])
        self.WIDGET_GUI_SIGNAL = sip.wrapinstance(self.GUI_SIGNAL.qwidget(), Qt.QWidget)
        #self.WIDGET_GUI_SIGNAL.setStyleSheet("background:#FFF;")
        self.WIDGET_GUI_SIGNAL.setFixedSize(450,200)
    def TIME_GRAPH_init(self):
        self.GUI_SIGNAL = qtgui.time_sink_f( # type: ignore
            self.BUFFER_SIZE, #size
            self.SAMPLE_RATE, #samp_rate
            self.NAME, #name
            self.INPUTed, #number of inputs
            None, # parent
        )
        self.GUI_SIGNAL.set_update_time(0.10)
        self.GUI_SIGNAL.set_y_axis(-0.1, 1.1)

        self.GUI_SIGNAL.set_y_label('Amplitude', "")

        self.GUI_SIGNAL.enable_tags(False)
        self.GUI_SIGNAL.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "") # type: ignore
        self.GUI_SIGNAL.enable_autoscale(True)
        self.GUI_SIGNAL.enable_grid(True)
        self.GUI_SIGNAL.enable_axis_labels(True)
        self.GUI_SIGNAL.enable_control_panel(False)
        self.GUI_SIGNAL.enable_stem_plot(False)

        self.GUI_SIGNAL.disable_legend()

        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.GUI_SIGNAL.set_line_label(i, "Data {0}".format(i))
            else:
                self.GUI_SIGNAL.set_line_label(i, labels[i])
            self.GUI_SIGNAL.set_line_width(i, widths[i])
            self.GUI_SIGNAL.set_line_color(i, colors[i])
            self.GUI_SIGNAL.set_line_style(i, styles[i])
            self.GUI_SIGNAL.set_line_marker(i, markers[i])
            self.GUI_SIGNAL.set_line_alpha(i, alphas[i])

        self.WIDGET_GUI_SIGNAL = sip.wrapinstance(self.GUI_SIGNAL.qwidget(), Qt.QWidget)
        #self.WIDGET_GUI_SIGNAL.setStyleSheet("background:#FFF;")
        self.WIDGET_GUI_SIGNAL.setFixedSize(450,200)

    def getWidget(self):
        return self.WIDGET_GUI_SIGNAL
    def autoscale(self,state:bool):
        self.GUI_SIGNAL.enable_autoscale(state)
    def connecting(self,signal,ID=0):
        self.connect((signal,ID),(self.GUI_SIGNAL,ID))
    def starting(self):
        self.start()
    def setFreqCenter(self, freq):
        self.CENTRE_FREQ = freq
        self.GUI_SIGNAL.set_frequency_range(self.CENTRE_FREQ,self.CENTRE_FREQ/2)
    def setSampleRate(self,freq):
        self.SAMPLE_RATE = freq
        if self.TYPE == 'SIGNAL/TIME':
            self.GUI_SIGNAL.set_samp_rate(self.SAMPLE_RATE)
        elif self.TYPE == 'SIGNAL/FREQUENCE':
            self.GUI_SIGNAL.set_frequency_range(self.CENTRE_FREQ,self.SAMPLE_RATE*2)