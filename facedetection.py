import cv2
import sys
import time

cascPath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

#Defaultwerte ersetzen
video_capture.set(cv2.CAP_PROP_BRIGHTNESS, 50) #Helligkeit des Videofeeds
video_capture.set(cv2.CAP_PROP_FPS, 15) #Framerate der Kamera auf 30 FPS
video_capture.set(cv2.CAP_PROP_SATURATION, -100) #Saettigung der Kamera auf -100 gesetzt, fuer BW-Bild (evtl. weniger CPU-Last, da keine Farben?)
video_capture.set(cv2.CAP_PROP_CONTRAST, 50) #Anpassung des Kontrasts (evtl. bessere/deutlichere Erkennung von Gesichtern)

while True:
    ret, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (50, 50),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video_capture.release()
