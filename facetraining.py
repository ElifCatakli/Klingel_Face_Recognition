import cv2
import numpy as np
from PIL import Image
import os
from dataset import capture_faces

#Test Methodes
# Ask the user to enter a face ID
face_id = input('\n enter user id end press <return> ==>  ')

# Print a message to let the user know that the program is initializing
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

capture_faces(face_id)

# Path for face image database
path = 'dataset'

# LBPH is a method used for face recognition  
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the haarcascade for frontal face detection
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

# Function to get the images and label data
def getImagesAndLabels(path):
    # looks for image path
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    
    # Iterate over the image paths
    for imagePath in imagePaths:
        
        # Open the images in grayscale
        PIL_img = Image.open(imagePath).convert('L')
        
        # Convert the image to a Numpy array
        img_numpy = np.array(PIL_img,'uint8')
        
        # Get the ID from the file name
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        
        # Detect faces in the images
        faces = detector.detectMultiScale(img_numpy)
        
        # Iterate over the detected faces
        for (x,y,w,h) in faces:
            # Add the faces and its ID to the lists
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

# Print a message to let the user know that the program is processing
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")

# Get the face samples and IDs
faces,ids = getImagesAndLabels(path)

# Train the model with the face sample and IDs
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') 

# Print the numer of faces trained and end the program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))