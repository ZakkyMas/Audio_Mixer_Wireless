import json, socket, re
try:
    myHostName = socket.gethostname()
    myIP = socket.gethostbyname(myHostName)
    print("IP address of the localhost is {}".format(myIP))
except:
    pass

class WebServer:
    def __init__(self, system):
        self._call = system

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 80))
        self.s.listen(5)
        self._stat = [False, ""]

    def readFile(self, name):
        data = ""
        with open(name, 'r') as f:
            data = f.read()
            f.close()
        return data

    def Filter_Data(self, data):
        data = re.split('\s', data)
        m_mode = data[0][2:]
        data_l = re.split('\?', data[1])
        m_link = data_l[0]
        if len(data_l) > 1:
            data_l = re.split('&', data_l[1])
        else:
            data_l = []
        return [m_mode, m_link, data_l]

    def Filter_File(self, text):
        a = "\\r\\n\\r\\n"
        b = text.find(a)
        file = text[b+8:-1]
        file = file.replace('\\', "")
        return file

    def Filter_Json(self, file):
        if file['name'] == 'Audio':
            self._call.JSON_Main['audio']['inpu'] = self._call.JSON_Web['audio']['inpu'] = int(file['inpu'])
            self._call.JSON_Main['audio']['loud'] = self._call.JSON_Web['audio']['loud'] = int(file['loud'])
            self._call.JSON_Main['audio']['gain'] = self._call.JSON_Web['audio']['gain'] = int(file['gain'])
            self._call.JSON_Main['audio']['volu'] = self._call.JSON_Web['audio']['volu'] = int(file['volu'])
            self._call.JSON_Main['audio']['bass'] = self._call.JSON_Web['audio']['bass'] = int(file['bass'])
            self._call.JSON_Main['audio']['treb'] = self._call.JSON_Web['audio']['treb'] = int(file['treb'])
            self._call.JSON_Main['audio']['ba-r'] = self._call.JSON_Web['audio']['ba-r'] = int(file['ba-r'])
            self._call.JSON_Main['audio']['ba-l'] = self._call.JSON_Web['audio']['ba-l'] = int(file['ba-l'])
            self._call.Save()
            return
        if file['name'] == 'Wifi':
            self._call.JSON_Main['wifi']['mode'] = int(file['mode'])
            self._call.JSON_Main['wifi']['SSID'] = file['user']
            self._call.JSON_Main['wifi']['PASS'] = file['passA']
            self._call.JSON_Web['wifi']['SSID'] = self._call.JSON_Main['wifi']['SSID']
            self._call.Save()
            self._call.REBOOT()
            self._stat[0] = False
            self._stat[1] = None
            return
        if file['name'] == 'Profil':
            if self._call.JSON_Main['web']['USERNAME'] != file['userA']:
                return
            if self._call.JSON_Main['web']['PASSWORD'] != file['passA']:
                return

            self._call.JSON_Main['web']['USERNAME'] = file['userB']
            self._call.JSON_Main['web']['PASSWORD'] = file['passB']
            self._call.Save()
            self._stat[0] = False
            self._stat[1] = None
            return

    def Looping(self):
        Server, Address = self.s.accept()
        Address = Address[0]
        data_m = str(Server.recv(2048))
        m_mode, m_link, data_g = self.Filter_Data(data_m)
        data_dll = self.Filter_File(data_m)

        print("")
        # print(1, Address)
        # print(2, data_m)
        # print(3, m_mode)
        print(4, m_link)
        print(5, data_g)
        print(6, data_dll)

        data_p, data_t = ["", "text/html"]
        if m_mode == 'GET':
            if m_link == '/bootstrap.min.js':
                data_p = self.readFile('bootstrap.min.js')
                data_t = "text/javascript"

            elif m_link == '/b_login.js':
                data_p = self.readFile('b_login.js')
                data_t = "text/javascript"

            elif m_link == '/bootstrap.min.css':
                data_p = self.readFile('bootstrap.min.css')
                data_t = "text/css"

            elif self._stat[0] and self._stat[1] == Address:
                if m_link == '/audiomixer':
                    data_p = self.readFile('a_audiomixer.html')
                    data_t = "text/html"

                elif m_link == '/wifi':
                    data_p = self.readFile('a_wifi.html')
                    data_t = "text/html"

                elif m_link == '/profil':
                    data_p = self.readFile('a_profil.html')
                    data_t = "text/html"

                elif m_link == '/b_web.js':
                    data_p = self.readFile('b_web.js')
                    data_t = "text/javascript"

                elif m_link == '/b_web.json':
                    data_p = self.readFile('b_web.json')
                    data_t = "application/json"

                elif m_link == '/getJson':
                    if 'name=Login' in data_g:
                        data_p = json.dumps({"status":True})
                        data_t = "application/json"
                
                else:    
                    data_p = self.readFile('a_home.html')
                    data_t = "text/html"
            else:
                data_p = self.readFile('a_login.html')
                data_t = "text/html"
            
            Server.send('HTTP/1.1 200 OK\n'.encode())
            Server.send('Content-Type: {}\n'.format(data_t).encode())
            Server.send('Serverection: close\n\n'.encode())
            Server.sendall(data_p.encode())
            Server.close()

        elif m_mode == 'POST':
            if m_link == '/postJson':
                file = json.loads(data_dll[1:-1])
                if file['name'] == 'Login':
                    if file['user'] == self._call.JSON_Main['web']['USERNAME']:
                        if file['pass'] == self._call.JSON_Main['web']['PASSWORD']:
                            self._stat[0] = True
                            self._stat[1] = Address
                elif file['name'] == 'Keluar':
                    if file['status'] and self._stat[1] == Address:
                        self._stat[0] = False
                        self._stat[1] = None
                elif self._stat[0] and self._stat[1] == Address:
                    self.Filter_Json(file)
            
            Server.send('HTTP/1.1 200 OK\n'.encode())
            Server.close()

class Wifi:
    def __init__(self, system):
        self._call = system
        self._wifi = None
        self._call.LED(1)
        try:
            import utime as time
            import network

            if self._call.JSON_Main['wifi']['mode']:
                self._wifi = network.WLAN(network.STA_IF)
                self._wifi.active(True)
                self._wifi.connect(self._call.JSON_Main['wifi']['SSID'], self._call.JSON_Main['wifi']['PASS'])
                if not self._wifi.isconnected():
                    for a in range(10):
                        time.sleep(1)
                        if self._wifi.isconnected():
                            self._call.LED(2)
                            self._call.wifi_connect = True
                            break
            else:
                self._wifi = network.WLAN(network.AP_IF)
                self._wifi.active(True)
                self._wifi.config(essid=self._call.JSON_Main['wifi']['SSID'], password=self._call.JSON_Main['wifi']['PASS'])
                self._call.LED(2)
                self._call.wifi_connect = True
            print("IP :", self._wifi.ifconfig()[0])
        except:
            self._call.wifi_connect = True

    def Looping(self):
        if self._call.JSON_Main['wifi']['mode']:
            if not self._wifi.isconnected():
                self._call.LED(1)
                self._call.wifi_connect = False
            else:
                self._call.LED(2)
                self._call.wifi_connect = True
        else:
            self._call.LED(2)
            self._call.wifi_connect = True

    def Exit(self):
        self._wifi = None

class Hardware:
    def __init__(self, system):
        self._call = system
        self._call.REBOOT = self.REBOOT
        self._call.LED = self.LED
        self._led, self._adc, self._int0, self._int1 = [None, None, None, None]

        try:
            from machine import Pin, PWM, ADC, Timer
            self._led = PWM(Pin(13), duty=0, freq=1)

            Pin(16).off()
            Pin(14).off()
            self._adc = ADC(0)

            self._int0 = Pin(12, Pin.IN)
            self._int0.irq(handler=self.Inter0, trigger=Pin.IRQ_LOW_LEVEL)
            self._int1 = Timer(1)
            self._int1.init(mode=Timer.ONE_SHOT, period=1000)
            self._int1.irq(handler=self.Inter1, trigger=Timer.TIMEOUT)
        except:
            pass

    def LED(self, val=0):
        try:
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
        except:
            pass

    def REBOOT(self):
        try:
            import machine 
            machine.reset()
        except:
            pass

    def Inter1(self):
        try:
            import gc, machine
            self._call.JSON_Main['hardware']['volt'] = (self._adc.read()*(1.0/1024)*10)
            self._call.JSON_Web['hardware']['volt'] = self._call.JSON_Main['hardware']['volt']
            self._call.JSON_Web['hardware']['free'] = gc.mem_free()
            self._call.JSON_Web['hardware']['use'] = gc.mem_alloc()
            self._call.JSON_Web['hardware']['freq'] = machine.freq()
            self._call.Save()
        except:
            pass

    def Inter0(self):
        try:
            import utime as time
            self._call.RESET()
            self._call.LED(4)
            time.sleep(3)
        except:
            pass

    def Exit(self):
        self._led, self._adc, self._int0, self._int1 = [None, None, None, None]

class Audio:
    def __init__(self, system):
        self._call = system
        self._call.AUDIO = self.AUDIO
        self.twi = None
        try: 
            from machine import Pin, I2C
            self.twi = I2C(sda=Pin(5), scl=Pin(4), freq=100000)
        except:
            pass
        self._call.AUDIO()

    def AUDIO(self):
        data = [0, 0, 0, 0, 0, 0]
        data[0] = self._call.JSON_Main['audio']['volu']
        data[1] = (6 << 5) | self._call.JSON_Main['audio']['ba-l']
        data[2] = (7 << 5) | self._call.JSON_Main['audio']['ba-r']
        data[3] = (1 << 6) | self._call.JSON_Main['audio']['inpu']
        data[3] |= (self._call.JSON_Main['audio']['gain'] << 3) | (self._call.JSON_Main['audio']['loud'] << 2)
        data[4] = (6 << 4) | self._call.JSON_Main['audio']['bass']
        data[5] = (7 << 4) | self._call.JSON_Main['audio']['treb']

        try:
            for a in data:
                self.twi.writeto(68, a)
        except:
            pass
        del data

    def Exit(self):
        self.twi = None

class Storage:
    def __init__(self, system):
        self._call = system
        self._call.Save = self.SAVE
        self._call.RESET = self.RESET

        with open('main.json') as f:
            self._call.JSON_Main = json.loads(f.read())
            f.close()
        with open('b_web.json') as f:
            self._call.JSON_Web = json.loads(f.read())
            f.close()

    def SAVE(self):
        with open('main.json', 'w') as f:
            f.write(json.dumps(self._call.JSON_Main))
            f.close()
        with open('b_web.json', 'w') as f:
            f.write(json.dumps(self._call.JSON_Web))
            f.close()

    def RESET(self):
        with open('reset_main.json') as f:
            with open('main.json', 'w') as ff:
                ff.write(f.read)
                ff.close()
            f.close()
        with open('reset_b_web.json') as f:
            with open('b_web.json', 'w') as ff:
                ff.write(f.read)
                ff.close()
            f.close()
        self._call.REBOOT()

class System:
    def __init__(self):
        #File
        self.Save = None
        self.JSON_Web = None
        self.JSON_Main = None

        #Variabel
        self.wifi_connect = False

        #function
        self.AUDIO = None
        self.LED = None
        self.REBOOT = None
        self.RESET = None

        #data   
        self._data = []
        self._data.append(Storage(self))
        self._data.append(Audio(self))
        self._data.append(Hardware(self))
        self._data.append(Wifi(self))
        self._data.append(WebServer(self))

    def Looping(self):
        import gc 
        gc.enable()
        gc.collect()
        while True:
            for a in self._data:
                try:
                    gc.collect()
                    a.Looping()
                    # if not self.wifi_connect:
                        # break
                except Exception as e:
                    # print(e)
                    pass

    def Exit(self):
        for a in self._data:
            try:
                a.Exit()
            except:
                pass
        self.Save, self.JSON_Web, self.JSON_Main, self.AUDIO, self.LED, self.REBOOT, self.RESET = [None, None, None, None, None, None, None]
        self.wifi_connect = False
        del self._data
        import gc 
        gc.collect()

Main = System()
Main.Looping()
