import gc
gc.enable()

import utime as time
from machine import Pin

res = 0
for a in range(20):
    if not Pin(0, Pin.IN).value():
        res = 1
        break
    time.sleep_ms(100)

if not res:
    try:
        from m_System import System

        main = System()
        main.Looping()
        main.Exit()
    except Exception as e:
        gc.collect()
        print("File Error :", e)
        print("Exit....")