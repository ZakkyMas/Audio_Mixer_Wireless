import gc
gc.collect()

from machine import Pin, I2C

class Audio:
    def __init__(self, system):
        self._call = system
        self._call.AUDIO = self.AUDIO
        self.twi = I2C(sda=Pin(5), scl=Pin(4), freq=400000)
        self._data = []
        self._data.append(('\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09', '\x0A', '\x0B', '\x0C', '\x0D', '\x0E', '\x0F'))
        self._data.append(('\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1A', '\x1B', '\x1C', '\x1D', '\x1E', '\x1F'))
        self._data.append(('\x20', '\x21', '\x22', '\x23', '\x24', '\x25', '\x26', '\x27', '\x28', '\x29', '\x2A', '\x2B', '\x2C', '\x2D', '\x2E', '\x2F'))
        self._data.append(('\x30', '\x31', '\x32', '\x33', '\x34', '\x35', '\x36', '\x37', '\x38', '\x39', '\x3A', '\x3B', '\x3C', '\x3D', '\x3E', '\x3F'))
        self._data.append(('\x40', '\x41', '\x42', '\x43', '\x44', '\x45', '\x46', '\x47', '\x48', '\x49', '\x4A', '\x4B', '\x4C', '\x4D', '\x4E', '\x4F'))
        self._data.append(('\x50', '\x51', '\x52', '\x53', '\x54', '\x55', '\x56', '\x57', '\x58', '\x59', '\x5A', '\x5B', '\x5C', '\x5D', '\x5E', '\x5F'))
        self._data.append(('\x60', '\x61', '\x62', '\x63', '\x64', '\x65', '\x66', '\x67', '\x68', '\x69', '\x6A', '\x6B', '\x6C', '\x6D', '\x6E', '\x6F'))
        self._data.append(('\x70', '\x71', '\x72', '\x73', '\x74', '\x75', '\x76', '\x77', '\x78', '\x79', '\x7A', '\x7B', '\x7C', '\x7D', '\x7E', '\x7F'))
        self._data.append(('\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8A', '\x8B', '\x8C', '\x8D', '\x8E', '\x8F'))
        self._data.append(('\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9A', '\x9B', '\x9C', '\x9D', '\x9E', '\x9F'))
        self._data.append(('\xA0', '\xA1', '\xA2', '\xA3', '\xA4', '\xA5', '\xA6', '\xA7', '\xA8', '\xA9', '\xAA', '\xAB', '\xAC', '\xAD', '\xAE', '\xAF'))
        self._data.append(('\xB0', '\xB1', '\xB2', '\xB3', '\xB4', '\xB5', '\xB6', '\xB7', '\xB8', '\xB9', '\xBA', '\xBB', '\xBC', '\xBD', '\xBE', '\xBF'))
        self._data.append(('\xC0', '\xC1', '\xC2', '\xC3', '\xC4', '\xC5', '\xC6', '\xC7', '\xC8', '\xC9', '\xCA', '\xCB', '\xCC', '\xCD', '\xCE', '\xCF'))
        self._data.append(('\xD0', '\xD1', '\xD2', '\xD3', '\xD4', '\xD5', '\xD6', '\xD7', '\xD8', '\xD9', '\xDA', '\xDB', '\xDC', '\xDD', '\xDE', '\xDF'))
        self._data.append(('\xE0', '\xE1', '\xE2', '\xE3', '\xE4', '\xE5', '\xE6', '\xE7', '\xE8', '\xE9', '\xEA', '\xEB', '\xEC', '\xED', '\xEE', '\xEF'))
        self._data.append(('\xF0', '\xF1', '\xF2', '\xF3', '\xF4', '\xF5', '\xF6', '\xF7', '\xF8', '\xF9', '\xFA', '\xFB', '\xFC', '\xFD', '\xFE', '\xFF'))
        self._call.AUDIO()
        gc.collect()

    def AUDIO(self):
        data = [0, 0, 0, 0, 0, 0]
        data[0] = 63-self._call.JSON_Main['audio']['volu']
        data[1] = (6 << 5) | (31-self._call.JSON_Main['audio']['ba-l'])
        data[2] = (7 << 5) | (31-self._call.JSON_Main['audio']['ba-r'])
        data[3] = (1 << 6) | self._call.JSON_Main['audio']['inpu']
        data[3] |= (self._call.JSON_Main['audio']['gain'] << 3) | (self._call.JSON_Main['audio']['loud'] << 2)

        a = self._call.JSON_Main['audio']['bass']
        if a > 7:
            a = 14-(a-8)
        data[4] = (6 << 4) | a
        
        a = self._call.JSON_Main['audio']['treb']
        if a > 7:
            a = 14-(a-8)
        data[5] = (7 << 4) | a

        data_a = []
        for a in data:
            data_a.append(self._data[(a>>4)&15][a&15])
        	
        try:
            for a in data_a:
                self.twi.writeto(68, a)
        except:
            print("ERROR AUDIO")
        gc.collect()
        
    def Exit(self):
        self.twi = None

    def Looping(self):
        pass