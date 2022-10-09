import cv2
import sys

# Path to the XML file used to detect faces 
cascadePath = './haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    
    for (x, y, w, h) in faces:
        # Cuts part of image to save -> rectangle 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    cv2.imshow('Video', frame)
    
    # Waits for user input, prevents a crash  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Closes video file or the capturing device     
video_capture.release()
