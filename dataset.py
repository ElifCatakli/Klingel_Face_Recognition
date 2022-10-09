import cv2
import os

camera = cv2.VideoCapture(0)
camera.set(3, 640) # set video width
camera.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

# Initialize face count, filename 
count = 0
while(True):
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        # Cuts part of image to save -> rectangle  
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' +  
                    str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('frame', frame)
    # Waits for user input, prevents a crash  
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break
     
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
# Closes video file or the capturing device 
camera.release()
cv2.destroyAllWindows()

