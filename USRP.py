#!"C:/ProgramData/radioconda/python.exe
import sys

import time
import uhd
import GBF
from gnuradio import gr
from gnuradio import blocks
from gnuradio import uhd
class USRP(gr.top_block):
    AVAILABLE_BOARD = ['NI2900']
    def __init__(self,mode:str):
        gr.top_block.__init__(self,"MAIN", catch_exceptions=True)
        if mode == 'TX' or 'TX' in mode:
            self.IsConnected = False
            self.sample_rate = 64000
            self.data_tank = blocks.throttle( gr.sizeof_gr_complex*1, (self.sample_rate*12), True, 0 if "auto" == "auto" else max( int(float(0.1) * (self.sample_rate*12)) if "auto" == "time" else int(0.1), 1) ) # type: ignore
            self.converteur = blocks.float_to_complex(1) # type: ignore
            self.copy = blocks.copy(gr.sizeof_float*1)# type: ignore
            self.copy.set_enabled(False)
            try:
                    aa = uhd.usrp_sink(",".join(("", '')),uhd.stream_args( # type: ignore
                                                                                cpu_format="fc32",
                                                                                args="",
                                                                                channels=list(range(0,1)),
                                                                                ),"",)
                    self.SetupVar('USRP_TX',aa)
                    self.Config_USRP_TX()
            except RuntimeError:
                print("[ERROR] Aucun Appareil trouver")
                from concurrent.futures import ThreadPoolExecutor
                executer = ThreadPoolExecutor(max_workers=1)
                executer.submit(self.reset_USRP_connection)
                return
        elif mode == 'RX' or 'RX' in mode:
            self.usrp_RX_info = self.usrp.get_usrp_rx_info() # type: ignore
        else:
            raise Exception("ERROR")
    def Config_USRP_TX(self):
        self.IsConnected = True
        self.usrp_TX_info = self.USRP_TX.get_usrp_info(0) # type: ignore
        print(self.usrp_TX_info)
        if self.usrp_TX_info['mboard_name'] in USRP.AVAILABLE_BOARD:
                self.board = self.usrp_TX_info['mboard_name']
                if self.board == 'NI2900':
                    self.TX_channel = 0
                    self.max_TX_gain = 89.75
                    self.Freq_range = [70000000,6000000000]
                    self.Samp_range = [64000,56000000]
                    self.sample_rate = 64000
                if self.usrp_TX_info['tx_antenna'] != 'TX Emetter TP6':
                    self.USRP_TX.set_antenna('TX Emetter TP6',self.TX_channel)# type: ignore
                    self.tx_antenna = self.USRP_TX.get_usrp_info(self.TX_channel)['tx_antenna']# type: ignore
            
            #self.SignalConnection.closeApp.emit(True)
        print('[INFO] USRP Init Success')
    def SetupVar(self,name:str,value):
        self.__setattr__(name,value)
    def reset_USRP_connection(self):
        while not self.IsConnected:
            print('[INFO] Retry Connection to USRP')
            try:
                aa = uhd.usrp_sink(",".join(("", '')),uhd.stream_args( # type: ignore
                                                                                cpu_format="fc32",
                                                                                args="",
                                                                                channels=list(range(0,1)),
                                                                                ),"",)
                self.SetupVar('USRP_TX',aa)
                print("[INFO] New USRP found")
                self.Config_USRP_TX()
                self.SignalConnection.closeApp.emit()# type: ignore
                 
            except RuntimeError:
                print("[ERROR] Aucun Appareil trouver")
                time.sleep(5)
            except KeyboardInterrupt:
                a = 1
    
    def set_TX_gain(self,gain):
        if gain > self.max_TX_gain:
            gain = self.max_TX_gain
        self.USRP_TX.set_gain(gain, self.TX_channel)# type: ignore
        print("[INFO] Setting gain to: {}".format(gain))
    
    
    def set_TX_sample_rate(self,sample_rate):
        if sample_rate >= self.Samp_range[0] and sample_rate <= self.Samp_range[1]:
            sample_rate = float(sample_rate)
            self.USRP_TX.set_samp_rate(sample_rate)# type: ignore
            print("[INFO] Setting sample_rate to: {}".format(sample_rate))
        else:
            print("[IWARNING] Sample_rate requested is out range")    
    
    
    def set_TX_centre_freq(self,center_freq):
        
        if center_freq >= self.Freq_range[0] and center_freq <= self.Freq_range[1]:
            center_freq = int(center_freq)
            self.USRP_TX.set_center_freq(center_freq, self.TX_channel)# type: ignore
            print("[INFO] Setting center_freq to: {}".format(center_freq))
        else:
            print("[IWARNING] Centre_Freq requested is out range")
    def set_On_Off(self,state):
        self.copy.set_enabled(state)
    def init_connection(self,data_input):
        try:
            print("[INFO] Try connection to [{}]".format(data_input.name()))
            self.connect((data_input,0),(self.copy,0))
            self.INPUT = data_input
            print("[INFO] Connection succesfull to [{}]".format(data_input.name()))
        except Exception:
            print("[ERROR] Connection error")
    def dump_connection(self):
        self.disconnect(self.INPUT,self.converteur)

def main():
    GBF_signal = GBF.GBF('SINUS',10000,5,32000)
    uu = USRP('TX')
    uu.init_connection(GBF_signal.SIGNAL)
    GBF_signal.start()
    uu.set_TX_gain(100)
    uu.set_TX_centre_freq(433000000)
    uu.run()

if __name__ == '__main__':
    main()

