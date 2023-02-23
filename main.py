import RPi.GPIO as GPIO
import cv2
import time
from facerecognition import facerecognition

class main:

    def setupPaths():
    
        global cascPath, recognizerPath, names
        cascPath = "haarcascade_frontalface_default.xml"
        recognizerPath = "trainer/trainer.yml"
        names = ['None', 'Elif', 'Daniel', 'Jathu', 'id4']
    
    
    
    def setupGPIO():
        GPIO.setwarnings(False)
        #Pin für Buzzer festlegen
        global BuzzerPin
        BuzzerPin = 22

        #Pin für Button festlegen und eine Variable zum Abfragen, ob der Knopf bereits gedrückt wurde
        global ButtonPin, buttonAlreadyPressed
        ButtonPin = 17
        buttonAlreadyPressed = 0
    
        GPIO.setmode(GPIO.BCM)

        #Zuweisung des Pins für Button
        GPIO.setup(ButtonPin, GPIO.IN)
    
        #Zuweisung des Pins für Buzzer
        GPIO.setup(BuzzerPin, GPIO.OUT)
        GPIO.output(BuzzerPin, GPIO.LOW)





    def setupCamera(cascPath):
    
        #print(cv2.__version__)
    
        #Facedetection konfigurieren
        global video_capture
        global faceCascade


        faceCascade = cv2.CascadeClassifier(cascPath)
    
        #Variablen für die Fenstergröße deklarieren
        global frameWidth, frameHeight
    
        frameWidth = 640
        frameHeight = 480
    
    
        #Initialisierung der Kamera
        video_capture = cv2.VideoCapture(0)
        video_capture.set(3, frameWidth)
        video_capture.set(4, frameHeight)
    
    
        #Minimale Fenstergröße der Gesichtserkennung festlegen
        global minW, minH
    
        minW = 0.1 * frameWidth
        minH = 0.1 * frameHeight

        #Defaultwerte der Kamera ersetzen
        video_capture.set(cv2.CAP_PROP_BRIGHTNESS, 50) #Helligkeit des Videofeeds
        video_capture.set(cv2.CAP_PROP_FPS, 30) #Framerate der Kamera auf 30 FPS
        #video_capture.set(cv2.CAP_PROP_SATURATION, 0) #Saettigung der Kamera auf -100 gesetzt, fuer BW-Bild (evtl. weniger CPU-Last, da keine Farben?)
        #video_capture.set(cv2.CAP_PROP_CONTRAST, 50) #Anpassung des Kontrasts (evtl. bessere/deutlichere Erkennung von Gesichtern)
 
    
    
    def cleanup():
        #Erst Buzzer ausschalten, dann die GPIO-Pins cleanen
        GPIO.output(BuzzerPin, GPIO.LOW)
        GPIO.cleanup()
        video_capture.release()
        cv2.destroyAllWindows()



    def buzzerOn():
        GPIO.output(BuzzerPin, GPIO.HIGH)



    def buzzerOff():
        GPIO.output(BuzzerPin, GPIO.LOW)



    if __name__ == '__main__':
        setupPaths()
        setupGPIO()
        setupCamera(cascPath)

        while True:
            if(GPIO.input(ButtonPin) and buttonAlreadyPressed == 0):
                buttonAlreadyPressed = 1
                detected = facerecognition(recognizerPath, cascPath, names, video_capture)

                if detected == True:
                    buzzerOn()
                    time.sleep(1.0)
                    buzzerOff()
                    print("Zutritt gewährt!")
                    
                elif detected == False:
                    print("Zutritt nicht gewährt!")
            
                cleanup()
                break