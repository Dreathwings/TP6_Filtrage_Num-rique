#!"C:/ProgramData/radioconda/python.exe
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
import random
class GBF(gr.top_block):
    __SHAPE = {'SINUS':analog.GR_SIN_WAVE,'COSINUS':analog.GR_COS_WAVE,'CARRE':analog.GR_SQR_WAVE,'TRIANGLE':analog.GR_TRI_WAVE,'DENT DE SCIE':analog.GR_SAW_WAVE,}# type: ignore
    def __init__(self,Forme:str,Freq:float,Amp:float,Rate:float,origine:float=0,phase:float=0) -> None:
        gr.top_block.__init__(self,"MAIN", catch_exceptions=True)
        
        self.SHAPE = Forme
        self.FREQUENCE = Freq
        self.AMPLITUDE = Amp
        self.SAMPLE_RATE = Rate
        self.ORIGINE = origine
        self.PHASE = phase
        self.SEED = random.randint(0,999999999)
        self.CHOOSE = 0
        self.start()
    def start(self):
        self.NOISE = analog.fastnoise_source_f(analog.GR_UNIFORM, self.AMPLITUDE, self.SEED, self.SAMPLE_RATE)# type: ignore
        self.GBF_SELECTOR = blocks.selector(4,self.CHOOSE,0)    # type: ignore
        self.GBF_SELECTOR.set_enabled(True)
        self.SIGNAL =  analog.sig_source_f(self.SAMPLE_RATE, self.SHAPE_TAGGEUR(), self.FREQUENCE, self.AMPLITUDE, self.ORIGINE, self.PHASE) # type: ignore
    def update(self,**kwargs):
        for tag in kwargs.keys():
            if tag == 'SHAPE':
                if kwargs[tag] != None:
                    self.SHAPE = kwargs[tag]
                    if self.SHAPE == 'BRUIT':
                        self.CHOOSE = 1
                        self.GBF_SELECTOR.set_input_index(self.CHOOSE)
                    else:
                        self.CHOOSE=0
                        self.GBF_SELECTOR.set_input_index(self.CHOOSE)
                        self.SetWaveForm(self.SHAPE_TAGGEUR())
            elif tag == 'FREQUENCE':
                self.FREQUENCE = kwargs.get(tag)
                self.SetFrequency(self.FREQUENCE)
            elif tag == 'AMPLITUDE':
                self.AMPLITUDE = kwargs.get(tag)
                self.SetAmplitude(self.AMPLITUDE)
            elif tag == 'SAMPLE_RATE':
                self.SAMPLE_RATE = kwargs.get(tag)
                self.SetSampleRate(self.SAMPLE_RATE)
    def SHAPE_TAGGEUR(self):
        return GBF.__SHAPE[self.SHAPE]
    def SetFrequency(self,value):
        self.FREQUENCE = value
        self.SIGNAL.set_frequency(value)
    def SetWaveForm(self,value):
        if self.SHAPE == 'CARRE':
            self.SIGNAL.set_offset((-self.AMPLITUDE)/2)
        else:
            self.SIGNAL.set_offset(0)
        self.SIGNAL.set_waveform(value)
    def SetAmplitude(self,value):
        if self.SHAPE == 'CARRE':
            self.SIGNAL.set_offset(-value/2)
        else:
            self.SIGNAL.set_offset(0)
        self.AMPLITUDE = value
        self.SIGNAL.set_amplitude(value)
        self.NOISE.set_amplitude(value)
    def SetSampleRate(self,value):
        self.SAMPLE_RATE = value
        self.SIGNAL.set_sampling_freq(value)