import gc
gc.collect()

import ujson as json

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
        with open('reset-main.json') as f:
            with open('main.json', 'w') as ff:
                ff.write(f.read)
                ff.close()
            f.close()
        with open('reset-b_web.json') as f:
            with open('b_web.json', 'w') as ff:
                ff.write(f.read)
                ff.close()
            f.close()
        self._call.REBOOT()

    def Looping(self):
        pass
