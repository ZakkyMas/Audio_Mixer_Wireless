
import gc
gc.collect()

import network
import utime as time

class Wifi:
    def __init__(self, system):
        self._call = system
        self._wifi = None
        self._call.LED(1)

        self._wifi = network.WLAN(network.AP_IF)
        self._wifi.active(True)
        self._wifi.config(essid=self._call.JSON_Main['wifi']['SSID'])
        self._wifi.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.0.10', '8.8.8.8'))
        self._call.wifi_connect = True
        self._call.LED(2)
        print("WiFi IP/Link :", self._wifi.ifconfig()[0])

    def Looping(self):
        pass

    def Exit(self):
        self._wifi = None
