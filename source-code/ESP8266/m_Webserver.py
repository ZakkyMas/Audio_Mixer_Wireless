import gc
import usocket as socket, ujson as json, ure as re

class WebServer:
    def __init__(self, system):
        self._call = system
        self.s = socket.socket()
        self.s.bind(('', 80))
        self.s.listen(3)

    def readFile(self, name):
        data = ""
        with open(name, 'r') as f:
            gc.collect()
            data = f.read()
            f.close()
        return data

    def Filter_Data(self, data):
        regex = re.compile('\s')
        data = regex.split(data)
        m_mode = data[0][2:]
        regex = re.compile('\?')
    
        data_l = regex.split(data[1])
        m_link = data_l[0]
        if len(data_l) > 1:
            regex = re.compile('&')
            data_l = regex.split(data_l[1])
        else:
            data_l = []
        del regex
        return [m_mode, m_link, data_l]

    def ConventerJson(self, file, Address):
        if len(file) < 1:
            return
        data = {}
        regex = re.compile('=')
        d = []
        for a in file:
            b, c = regex.split(a)
            d.append(b)
            data[b] = c
        
        if 'InputStereo' in d:
            data['name'] = 'Audio'
            self.Filter_Json(data)
        del data, d, regex

    def Filter_Json(self, file):
        if file['name'] == 'Audio':
            self._call.JSON_Main['audio']['inpu'] = self._call.JSON_Web['audio']['inpu'] = int(file['InputStereo'])
            self._call.JSON_Main['audio']['loud'] = self._call.JSON_Web['audio']['loud'] = int(file['InputLoud'])
            self._call.JSON_Main['audio']['gain'] = self._call.JSON_Web['audio']['gain'] = int(file['InputGain'])
            self._call.JSON_Main['audio']['volu'] = self._call.JSON_Web['audio']['volu'] = int(file['InputVolume'])
            self._call.JSON_Main['audio']['bass'] = self._call.JSON_Web['audio']['bass'] = int(file['InputBass'])
            self._call.JSON_Main['audio']['treb'] = self._call.JSON_Web['audio']['treb'] = int(file['InputTreble'])
            self._call.JSON_Main['audio']['ba-r'] = self._call.JSON_Web['audio']['ba-r'] = int(file['InputBalanceR'])
            self._call.JSON_Main['audio']['ba-l'] = self._call.JSON_Web['audio']['ba-l'] = int(file['InputBalanceL'])
            self._call.Save()
            self._call.AUDIO()
            return

    def Looping(self):
        Server, Address = self.s.accept()
        data_m = Server.recv(2048)
        if not data_m:
            Server.close()
            data_m = ""
            return 
        
        self._call.LED(0)
        Address = Address[0]
        data_m = str(data_m)
        m_mode, m_link, data_g = self.Filter_Data(data_m)

        # print("")
        # print("FREE :", gc.mem_free(), " USE :", gc.mem_alloc())
        # print("ADDR :", Address)
        # print("OLD  :", data_m)
        # print("MODE :", m_mode)
        print("LINK :", m_link)
        print("DATA :", data_g)
        del data_m
        gc.collect()

        self.ConventerJson(data_g, Address)
        gc.collect()

        data_p, data_t = ["", "text/html"]
        if m_link == '/a_.css':
            data_p = self.readFile('a_.css')
            data_t = "text/css"
            
        elif m_link == '/audiomixer':
            data_p = self.readFile('a_audiomixer.html')
            data_t = "text/html"

        elif m_link == '/b_web.js':
            data_p = self.readFile('b_web.js')
            data_t = "text/javascript"

        elif m_link == '/b_web.json':
            data_p = json.dumps(self._call.JSON_Web)
            data_t = "application/json"
        
        elif m_link == '/home':
            data_p = self.readFile('a_home.html')
            data_t = "text/html"

        else:
            Server.send('HTTP/1.1 301 OK\n')
            Server.send('Location: /home\n')
            Server.send('Serverection: close\n\n')
            Server.close()
            self._call.LED(2)
            return
        
        Server.send('HTTP/1.1 200 OK\n')
        Server.send('Content-Type: {}\n'.format(data_t))
        Server.send('Serverection: close\n\n')
        Server.sendall(data_p)
        Server.close()

        
        del Address, data_g, m_link, m_mode
        self._call.LED(4)
        gc.collect()

    def Exit(self):
        self.s.exit()
