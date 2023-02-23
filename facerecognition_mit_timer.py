import cv2
import numpy as np
from time import time
import logging

logging.basicConfig(filename="confidence.log", level = logging.DEBUG)

'''
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

recognizerPath, cascadePath und names werden jetzt in der main gehandlet

videoPath = 0
'''
def facerecognition(recognizerPath, cascadePath, names, camera, timeout):

    # Create the face recognizer and load the trained data
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(recognizerPath)

    # Load the Haarcascade classifier for face detection
    faceCascade = cv2.CascadeClassifier(cascadePath);

    '''
     Daniel, wir können die ID auch außerhalb der methode definieren bsp. da wo wir die Parameter in der main definieren. Hatten dies als globale Variable. 
     Auch font ggf als globale variable? oder als parameter?
     Sieht vllt scheisse aus wenn das als einziges hier stehen bleibt, kanns die aber aussuchen
     oder einfach ohne parameter siehe facerecognition_without_Parameters
    '''
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

    start_time = 0
    face_detected = False

    while True:
        print((time() - start_time) , "face_detected: " , face_detected)
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
        
        if not face_detected and np.any(faces):
                face_detected = True
                start_time = time()
        
        elif not np.any(faces):
            face_detected = False #Reset if the faces werent found
            
        elif face_detected and time() - start_time >= timeout:
            # Loop through the detected faces
            for(x,y,w,h) in faces:
                
                print("Test")
                # Draw a rectangle around the face
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

                # Predict the identity of the face and calculate the confidence level
                id, loss = recognizer.predict(gray[y:y+h,x:x+w])
                logging.debug(loss)
            
                # If loss is less than 100 || if 0 = perfect match 
                if loss < 100:
                    # If the confidence level is high, display the predicted name
                    name = names[id]
                   # confidence = "  {0}%".format(round(100 - loss))
                    confidence = "  {0}%".format(round(100-float(loss)))
                    cv2.putText(frame, name, (x+5,y-5), font, 1, (255,255,255), 2)
                else:
                    # If the confidence level is low, display "unknown"
                    name = "unkown"
                    confidence = "  {0}%".format(round(100 - loss))
                    cv2.putText(frame, name, (x+5,y-5), font, 1, (255,255,255), 2)
            
                # Display the name and confidence level on the frame
                cv2.putText(frame, name, (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(frame, confidence, (x+5,y+h-5), font, 1, (255,255,0), 1)
            
                logging.info(confidence)
                return True

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