import cv2
import numpy as np
import time

import logging

logging.basicConfig(filename="confidence.log", level = logging.DEBUG)



def facerecognition(recognizerPath, cascadePath, names, camera):

    # Create the face recognizer and load the trained data
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(recognizerPath)

    # Load the Haarcascade classifier for face detection
    faceCascade = cv2.CascadeClassifier(cascadePath);

    # Set the front for displaying text on the frame
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize the ID counter and names dictionary
    id = 0


    # Set the width and height of the frame
    width = 640
    height = 480

    # Set the minimum window size to be recognized as a face
    minW = 0.1 * width
    minH = 0.1 * height
    
    waitCounter = 0
    
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

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
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            confidence = round(confidence, 0)
            
            logging.debug(confidence)
            
            if confidence < 100:
                
                name = names[id]
                
                confidence = "  {0}%".format(confidence)
                
                waitCounter += 1
                
                if waitCounter >= 30:
                    return True
                
            else:
                # If the confidence level is low, display "unknown"
                name = "unkown"
                confidence = "0%"
                
                waitCounter += 1
                
                if waitCounter >= 30:
                    return False
            
            # Display the name and confidence level on the frame
            cv2.putText(frame, name, (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(frame, confidence, (x+5,y+h-5), font, 1, (255,255,0), 1)
            
            logging.info(confidence)

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