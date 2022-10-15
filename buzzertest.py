import RPi.GPIO as GPIO
import time

Buzzer = 22

def setup(pin):
    global BuzzerPin
    BuzzerPin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
def on():
    GPIO.output(BuzzerPin, GPIO.LOW)
    
def off():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)

def loop():
    while True:
        beep(0.25)
        
def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup(Buzzer)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()