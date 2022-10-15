#Imports für I2C-Display
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import psutil

import os

#Code des I2C-Displays:
lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

def get_cpu_temp():
    t = psutil.sensors_temperatures()
    for x in t:
        return t[x][0].current

try:
    os.system("python ./facedetection_opt.py &")
    while True:
        CPU_Temp = get_cpu_temp()
        CPU_Temp = float("{:.1f}".format(CPU_Temp))
        CPU_Usage = psutil.cpu_percent(interval = .5)
        lcd.text("CPU-Tmp: " + str(CPU_Temp) + " C", 1)
        lcd.text("CPU-Usg: " + str(CPU_Usage) + "%", 2)
    
    pause()

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()
    os.system("pkill -f ./facedetection_opt.py &")