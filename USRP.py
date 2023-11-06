#!"C:/ProgramData/radioconda/python.exe
import sys

import time
import uhd
from zmq import device
import GBF
from gnuradio import gr
from gnuradio import blocks
from gnuradio import uhd
import osmosdr

class USRP(gr.top_block):
    AVAILABLE_BOARD = ['NI2900']
    def __init__(self,mode:str,ui):
        gr.top_block.__init__(self,"MAIN", catch_exceptions=True)
        if mode == 'TX' or 'TX' in mode:
            self.IsConnected = False
            self.UI = ui
            self.sample_rate = 64000
            #self.devices= osmosdr.device.find() # type: ignore
            #print(self.devices,'LIST AT START')
            self.data_tank = blocks.throttle( gr.sizeof_gr_complex*1, (self.sample_rate*12), True, 0 if "auto" == "auto" else max( int(float(0.1) * (self.sample_rate*12)) if "auto" == "time" else int(0.1), 1) ) # type: ignore
            self.converteur = blocks.float_to_complex(1) # type: ignore
            self.copy = blocks.copy(gr.sizeof_float*1)# type: ignore
            self.copy.set_enabled(False)
            self.Sink_Connection()
            """except RuntimeError:
                print("[ERROR] Aucun USRP trouver")
                from concurrent.futures import ThreadPoolExecutor
                executer = ThreadPoolExecutor(max_workers=1)
                executer.submit(self.reset_USRP_connection)
                return"""
        elif mode == 'RX' or 'RX' in mode:
            self.usrp_RX_info = self.usrp.get_usrp_rx_info() # type: ignore
        else:
            raise Exception("ERROR")
        

    def Config_USRP_TX(self):
        self.IsConnected = True
        self.usrp_TX_info = self.SINK.get_usrp_info(0) # type: ignore
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
                    self.SINK.set_antenna('TX Emetter TP6',self.TX_channel)# type: ignore
                    self.tx_antenna = self.SINK.get_usrp_info(self.TX_channel)['tx_antenna']# type: ignore
                #dev = osmosdr.device.find() # type: ignore
                """for i in dev:
                    if not i in self.devices:
                        self.dev = i"""
            
            #self.SignalConnection.closeApp.emit(True)
    def  Config_HackRF_TX(self):
        self.IsConnected = True
        self.board = 'Hack_RF'
        self.TX_channel = 0
        self.max_TX_gain = 89.75
        self.Freq_range = [1000000,6000000000]
        self.Samp_range = [64000,56000000]
        self.sample_rate = 64000
        self.SINK.set_antenna('TX Emetter TP6',self.TX_channel)# type: ignore
        self.tx_antenna = self.SINK.get_antenna(self.TX_channel)# type: ignore
        #dev = osmosdr.device.find() # type: ignore
        """for i in dev:
            if not i in self.devices:
                self.dev = i"""
        print('[INFO] HackRF Init Success')

    def SetupVar(self,name:str,value):
        self.__setattr__(name,value)

    def Sink_Connection(self):
            print('\n[INFO] Try Connection to USRP')
            try:
                aa = uhd.usrp_sink(",".join(("", '')),uhd.stream_args( # type: ignore
                                                                                cpu_format="fc32",
                                                                                args="",
                                                                                channels=list(range(0,1)),
                                                                                ),"",)
                self.SetupVar('SINK',aa)
                print("[INFO] New USRP found")
                self.Config_USRP_TX()
            except RuntimeError:
                print("[ERROR] Aucun USRP trouver")

            try:
                aa = osmosdr.sink(args="numchan=" + str(1) + " " + "") # type: ignore
                self.SetupVar('SINK',aa)
                print("[INFO] New HackRF found")
                self.Config_HackRF_TX()
            except RuntimeError:
                print("[ERROR] Aucun HackRF trouver")
        
    
    def set_TX_gain(self,gain):
        try:
            if gain > self.max_TX_gain:
                gain = self.max_TX_gain
            if self.board=='Hack_RF':
                self.SINK.set_gain(gain, self.TX_channel)# type: ignore
            elif self.board=='NI2900':
                self.SINK.set_gain(gain, self.TX_channel)# type: ignore
            print("[INFO] Setting gain to: {}".format(gain))
        except:
            self.IsConnected = False
            self.UI.Usrp_Reset()
    
    
    def set_TX_sample_rate(self,sample_rate):
        try:
            if sample_rate >= self.Samp_range[0] and sample_rate <= self.Samp_range[1]:
                sample_rate = float(sample_rate)
                if self.board=='Hack_RF':
                    self.SINK.set_sample_rate(sample_rate) # type: ignore
                elif self.board=='NI2900':
                    self.SINK.set_samp_rate(sample_rate)# type: ignore
                print("[INFO] Setting sample_rate to: {}".format(sample_rate))
            else:
                print("[WARNING] Sample_rate requested is out range")
        except:
            self.IsConnected = False
            self.UI.Usrp_Reset()  
    
    
    def set_TX_centre_freq(self,center_freq):
        if True: # type: ignore
            try:
                if center_freq >= self.Freq_range[0] and center_freq <= self.Freq_range[1]:
                    center_freq = int(center_freq)
                    if self.board=='Hack_RF':
                        self.SINK.set_center_freq(center_freq, self.TX_channel)# type: ignore
                    elif self.board=='NI2900':
                        self.SINK.set_center_freq(center_freq, self.TX_channel)# type: ignore
                    print("[INFO] Setting center_freq to: {}".format(center_freq))
                else:
                    print("[WARNING] Centre_Freq requested is out range")
            except RuntimeError:
                self.IsConnected = False
                self.UI.Usrp_Reset()

    def set_On_Off(self,state):
            self.copy.set_enabled(state)
    def is_connected(self)->bool: # type: ignore
        if self.board == "Hack_RF":
            if self.dev in osmosdr.device.find(): return True # type: ignore
            else: return False
        elif self.board == "NI2900":
            return True
        else: return False

    def init_connection(self):
        try:
            print("[INFO] Try connection for USRP")
            self.connect((self.data_tank,0),(self.SINK,0)) # type: ignore
            print("[INFO] Connection succesfull for USRP")
        except Exception:
            print("[ERROR] Connection error")
