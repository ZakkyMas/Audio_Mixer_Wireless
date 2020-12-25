import gc

#PC only 
import json, socket, re, time
import random, psutil

myHostName = socket.gethostname()
myIP = socket.gethostbyname(myHostName)
print("IP address of the localhost is {}".format(myIP))

gc.enable()
gc.collect()

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
        return re.split(r"\\r\\n", text)[-1][:-1]

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
        data_m = Server.recv(2048)
        
        if not data_m:
            Server.send('HTTP/1.1 200 OK\n')
            Server.send('Serverection: close\n\n')
            Server.close()
            return 
            
        Address = Address[0]
        data_m = str(data_m)
        m_mode, m_link, data_g = self.Filter_Data(data_m)
        data_dll = self.Filter_File(data_m)

        # print("")
        # print(1, Address)
        # print(2, data_m)
        # print(3, m_mode)
        # print(4, m_link)
        # print(5, data_g)
        # print(6, data_dll)

        data_p, data_t = ["", "text/html"]
        if m_mode == 'GET':
            if m_link == '/bootstrap.min.js':
                data_p = self.readFile('bootstrap.min.js')
                data_t = "text/javascript"

            elif m_link == '/bootstrap.min.css':
                data_p = self.readFile('bootstrap.min.css')
                data_t = "text/css"

            elif m_link == '/b_login.js':
                data_p = self.readFile('b_login.js')
                data_t = "text/javascript"

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
                file = json.loads('{}'.format(data_dll).replace('\\', '')[1:-1])
                if file['name'] == 'Login':
                    if self._stat[0] and self._stat[1] != Address:
                        pass
                    elif file['user'] == self._call.JSON_Main['web']['USERNAME']:
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
        self._call.wifi_connect = True

    def Looping(self):
        pass

    def Exit(self):
        self._wifi = None

class Hardware:
    def __init__(self, system):
        self._call = system
        self._call.REBOOT = self.REBOOT
        self._call.LED = self.LED
        self._led, self._adc, self._int0, self._int1 = [None, None, None, None]

    def LED(self, val=0):
        pass

    def REBOOT(self):
        pass

    def Looping(self):
        self._call.JSON_Main['hardware']['volt'] = 6.0 + psutil.sensors_battery()[0] / 24
        self._call.JSON_Web['hardware']['volt'] = self._call.JSON_Main['hardware']['volt']
        self._call.JSON_Web['hardware']['free'] = psutil.virtual_memory()[4]
        self._call.JSON_Web['hardware']['use'] = psutil.virtual_memory()[3]
        self._call.JSON_Web['hardware']['freq'] = int("{}000".format(int(psutil.cpu_freq()[0])))
        self._call.Save()

    def Exit(self):
        self._led, self._adc, self._int0, self._int1 = [None, None, None, None]

class Audio:
    def __init__(self, system):
        self._call = system
        self._call.AUDIO = self.AUDIO
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
 
    def Looping(self):
        pass

    def Exit(self):
        pass

class Storage:
    def __init__(self, system):
        self._call = system
        self._call.Save = self.SAVE
        self._call.RESET = self.RESET

        with open('main.json') as f:
            a = f.read()
            self._call.JSON_Main = json.loads(a)
            f.close()
        with open('b_web.json') as f:
            a = f.read()
            self._call.JSON_Web = json.loads(a)
            f.close()

    def SAVE(self):
        with open('main.json', 'w') as f:
            json.dump(self._call.JSON_Main, f)
            f.close()
        with open('b_web.json', 'w') as f:
            json.dump(self._call.JSON_Web, f)
            f.close()

    def RESET(self):
        with open('reset_main.json') as f:
            with open('main.json', 'w') as ff:
                ff.write(f.read())
                ff.close()
            f.close()
        with open('reset_b_web.json') as f:
            with open('b_web.json', 'w') as ff:
                ff.write(f.read())
                ff.close()
            f.close()
        self._call.REBOOT()

    def Looping(self):
        pass

class System:
    def __init__(self):
        gc.enable()
        gc.collect()
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
        try:
            gc.collect()
            print("Start....")
            self._data.append(Storage(self))
            print("function Storage Ready")
            self._data.append(Audio(self))
            print("function Audio Ready")
            self._data.append(Hardware(self))
            print("function Hardware Ready")
            self._data.append(Wifi(self))
            print("function Wifi Ready")
            self._data.append(WebServer(self))
            print("function WebServer Ready")
        except Exception as e:
            print("ERROR LIBRARY :", e)

    def Looping(self):
        gc.enable()
        gc.collect()
        while True:
            for a in self._data:
                try:
                    gc.collect()
                    a.Looping()
                except Exception as e:
                    print("ERROR Looping :", e)
                    pass

    def Exit(self):
        for a in self._data:
            try:
                gc.collect()
                a.Exit()
            except:
                pass
        self.Save, self.JSON_Web, self.JSON_Main, self.AUDIO, self.LED, self.REBOOT, self.RESET = [None, None, None, None, None, None, None]
        self.wifi_connect = False
        del self._data
        print("Exit....")
        gc.collect()

Main = System()
Main.Looping()
Main.Exit()
