import gc
gc.collect()

from m_Storage import Storage
from m_Audio import Audio
from m_Hardware import Hardware
from m_Wifi import Wifi
from m_Webserver import WebServer

class System:
    def __init__(self):
        gc.enable()
        #File
        self.Save = None
        self.JSON_Web = None
        self.JSON_Main = None

        #function
        self.AUDIO = None
        self.LED = None
        self.REBOOT = None
        self.RESET = None

        #data
        self._data = []
        try:
            gc.collect()
            print("Mem :", gc.mem_free(), gc.mem_alloc())
            print("Start....")
            self._data.append(Storage(self))
            print("function Storage Ready, Mem :", gc.mem_free(), gc.mem_alloc())
            self._data.append(Audio(self))
            print("function Audio Ready, Mem :", gc.mem_free(), gc.mem_alloc())
            self._data.append(Hardware(self))
            print("function Hardware Ready, Mem :", gc.mem_free(), gc.mem_alloc())
            self._data.append(Wifi(self))
            print("function Wifi Ready, Mem :", gc.mem_free(), gc.mem_alloc())
            self._data.append(WebServer(self))
            print("function WebServer Ready, Mem :", gc.mem_free(), gc.mem_alloc())
            gc.collect()
        except Exception as e:
            print("ERROR LIBRARY :", e)

    def Looping(self):
        gc.enable()
        gc.collect()
        while True:
            looping = 0
            for a in self._data:
                try:
                    looping += 1
                    gc.collect()
                    a.Looping()
                except Exception as e:
                    print("ERROR Loop :", e)
                    pass

    def Exit(self):
        for a in self._data:
            try:
                gc.collect()
                a.Exit()
            except:
                pass
        self.Save, self.JSON_Web, self.JSON_Main, self.AUDIO, self.LED, self.REBOOT, self.RESET = [None, None, None, None, None, None, None]
        del self._data
        gc.collect()
