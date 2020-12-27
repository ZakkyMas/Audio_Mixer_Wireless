import os, sys

os.popen('pip install adafruit-ampy')

__all__ = []

arg = sys.argv
if '--port' in arg:
    pass
else:
    print("--port!!")
    sys.exit()

data = os.listdir()
port = ""

for a in data:
    if a == '_install-files.py':
        continue
    __all__.append(a)

try:
    for a in range(len(arg)):
        if arg[a] == '--port':
            port = arg[a+1]
            break
except:
    print("--port!!")
    sys.exit()

for a in __all__:
    try:
        os.popen('ampy --port {} put {}'.format(port, a)).read()
        print("Install success :", a)
    except:
        print("Install error :", a)
        break