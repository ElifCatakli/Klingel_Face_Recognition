import RPi.GPIO as GPIO
import time

Button = 17

def setup(pin):
    global ButtonPin
    ButtonPin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ButtonPin, GPIO.IN)
        
def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup(Button)
    try:
        buttonPressed = 0
        while True:
            if(GPIO.input(ButtonPin) and (buttonPressed == 0)):
                print("Button wurde gedrückt.")
                buttonPressed = 1
                time.sleep(0.5)
        
            if(GPIO.input(ButtonPin) and (buttonPressed == 1)):
                print("Button wurde nochmal gedrückt.")
                buttonPressed = 0
                time.sleep(0.5)
    except KeyboardInterrupt:
        destroy()