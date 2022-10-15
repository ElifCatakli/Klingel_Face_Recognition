import RPi.GPIO as GPIO
import time

Button = 17
Buzzer = 22

def setup(pin1,pin2):
    global ButtonPin
    global BuzzerPin
    ButtonPin = pin1
    BuzzerPin = pin2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ButtonPin, GPIO.IN)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)
        
def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup(Button, Buzzer)
    GPIO.output(BuzzerPin, GPIO.LOW)
    try:
        buttonPressed = 0
        while True:
            if(GPIO.input(ButtonPin) and (buttonPressed == 0)):
                print("Buzzer an.")
                GPIO.output(BuzzerPin, GPIO.HIGH)
                buttonPressed = 1
                time.sleep(0.5)
        
            if(GPIO.input(ButtonPin) and (buttonPressed == 1)):
                print("Buzzer aus.")
                GPIO.output(BuzzerPin, GPIO.LOW)
                buttonPressed = 0
                time.sleep(0.5)
    except KeyboardInterrupt:
        destroy()
