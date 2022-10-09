import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids
# needs input method for app/ interface
names = ['None', 'Elif', 'Daniel', 'Jathu', 'id4'] 

# Initialize and start realtime video capture
camera = cv2.VideoCapture(0)
camera.set(3, 640) # set video widht
camera.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*camera.get(3)
minH = 0.1*camera.get(4)
while True:
    ret, frame =camera.read()
    #img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        id, loss = recognizer.predict(gray[y:y+h,x:x+w])
        
        # If loss is less than 100 || if 0 = perfect match 
        if (loss < 100):
            id = names[id]
            loss = "  {0}%".format(round(100 - loss))
        else:
            id = "unknown"
            loss = "  {0}%".format(round(100 - loss))
        
        cv2.putText(frame, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(frame, str(loss), (x+5,y+h-5), font, 1, (255,255,0), 1)  

    cv2.imshow('camera',frame) 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
camera.release()
cv2.destroyAllWindows()