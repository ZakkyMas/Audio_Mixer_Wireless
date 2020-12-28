import gc
gc.collect()

import machine
import utime as time
from machine import Pin, PWM, ADC, Timer

class Hardware:
    def __init__(self, system):
        self._call = system
        self._call.REBOOT = self.REBOOT
        self._call.LED = self.LED

        self._led = PWM(Pin(13), duty=0, freq=1)

        Pin(16).off()
        Pin(14).off()
        self._adc = ADC(0)
        gc.collect()

    def LED(self, val=0):
        if val == 0:
            self._led.duty(0)
        elif val == 1:
            self._led.duty(512)
            self._led.freq(1)
        elif val == 2:
            self._led.duty(512)
            self._led.freq(5)
        elif val == 3:
            self._led.duty(1023)
        elif val == 4:
            self._led.duty(512)
            self._led.freq(10)

    def REBOOT(self):
        machine.reset()

    def Inter1(self):
        self._call.JSON_Web['hardware']['volt'] = (self._adc.read()*(1.0/1024)*10)
        self._call.JSON_Web['hardware']['free'] = gc.mem_free()
        self._call.JSON_Web['hardware']['use']  = gc.mem_alloc()
        self._call.JSON_Web['hardware']['freq'] = machine.freq()
        self._call.Save()

    def Inter0(self):
        self._call.LED(4)
        self._call.RESET()
        time.sleep(3)

    def Looping(self):
        if(Pin(12, Pin.IN).value() == 0):
            self.Inter0()
        self.Inter1()

    def Exit(self):
        self._led, self._adc = [None, None]
