import cv2
import numpy as np
import os 

# Create the face recognizer and load the trained data
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Load the Haarcascade classifier for face detection
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the front for displaying text on the frame
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize the ID counter and names dictionary
id = 0

# names related to ids
names = ['None', 'Elif', 'Daniel', 'Jathu', 'id4'] 

# Set the width and height of the frame
width = 640
height = 480

# Initialize and start the video capture
camera = cv2.VideoCapture(0)
camera.set(3, width)
camera.set(4, height)

# Set the minimum window size to be recognized as a face
minW = 0.1 * width
minH = 0.1 * height

while True:
    # Capture frame-by-frame
    ret, frame =camera.read()

    # Convert the frame to grayscale for easier processing
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    # Loop through the detected faces
    for(x,y,w,h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # Predict the identity of the face and calculate the confidence level
        id, loss = recognizer.predict(gray[y:y+h,x:x+w])
        
        # If loss is less than 100 || if 0 = perfect match 
        if loss < 100:
            # If the confidence level is high, display the predicted name
            name = names[id]
            confidence = "  {0}%".format(round(100 - loss))
            # TODO: if confidence >(55-)60  -> piepen
        else:
            # If the confidence level is low, display "unknown"
            name = "unkown"
            confidence = "  {0}%".format(round(100 - loss))
            # TODO: kein piepen, oder print -> kein Zutritt
        
        # Display the name and confidence level on the frame
        cv2.putText(frame, name, (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(frame, confidence, (x+5,y+h-5), font, 1, (255,255,0), 1)  

    # Display the frame
    cv2.imshow('camera',frame) 

    # Check for user input to stop the script
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
camera.release()
cv2.destroyAllWindows()
