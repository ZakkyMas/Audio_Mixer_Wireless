import os, sys, re, subprocess
com = re.compile(r'^com[0-9]+$')
data = os.listdir()
port = ""
__all__ = []
Status = True
Com_1 = 'esptool.py --port {} erase_flash'

print('Install "esptool"\n')
os.system('pip install esptool')
print('')

print('Install "adafruit-ampy"\n')
os.system('pip install adafruit-ampy')
os.system('cls')
print('Install "esptool" & "adafruit-ampy" Done\n')

while Status:
    a = input('Input Port : ').lower()
    if com.match(a) == None:
        print('Error name port')
        continue
    port = a
    break

if Status:
    os.system('cls')
    try:
        print('Flashing ESP8266')
        subprocess.run(['esptool.py --port {} erase_flash'.format(port)], check=True)
    except Exception:
        print('Error Flashing ESP8266')
        Status=False

if Status:
    try:
        print('Flashing ESP8266')
        subprocess.run(['esptool.py --port {} --baud 460800 write_flash --flash_size=detect 0 esp8266-20210202-v1.14.bin'.format(port)], check=True)
    except Exception:
        print('Error Flashing ESP8266')
        Status=False

if Status:
    os.system('cls')
    print('Flashing ESP8266 Done')

if Status:
    for a in data:
        if a == '__install-files.py':
            continue
        elif a == 'esp8266-20210202-v1.14.bin':
            continue
        __all__.append(a)

    for a in __all__:
        try:
            subprocess.run(['ampy --port {} put {}'.format(port, a)], check=True)
            print("Install success :", a)
        except:
            print("Install error :", a)
            Status=False

input('press any key to exit')
