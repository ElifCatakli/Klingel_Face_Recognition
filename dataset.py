import cv2

def capture_faces(face_id):
    # Initialize the video capture
    camera = cv2.VideoCapture(0)

    # Set the width and height of the video
    camera.set(3, 640)
    camera.set(4, 480)

    # Load the haarcascade for frontal face
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    # Ask the user to enter a face ID
    #face_id = input('\n enter user id end press <return> ==>  ')

    # Print a message to let the user know that the program is initializing
    #print("\n [INFO] Initializing face capture. Look the camera and wait ...")

    # Initialize variable for face count and filename 
    count = 0

    # Capture frames from the camera indefinitely
    while(True):
        # Read the current frame from the video capture
        ret, frame = camera.read()
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        # Iterate over the detected faces
        for (x,y,w,h) in faces:
            # Draw a rectangle around the face 
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            
            # Increment the face count 
            count += 1
            
            # Save the captured image to the datasets folder
            # If count in dataset/User.face_id.count already exist do count+=1
            cv2.imwrite("dataset/User." + str(face_id) + '.' +  str(count) + ".jpg", gray[y:y+h,x:x+w])
            
            # Display the frame with the rectangle around the face
            cv2.imshow('frame', frame)
            
        # Check if the user pressed the 'ESC' key to exit the program, prevents a crash  
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
        
        # Stop capturing faces after 30 frames
        elif count >= 30: 
             break
         
    # Print a message to let the user know that the program is exiting
    print("\n [INFO] Exiting Program and cleanup stuff")

    # Release the video capture and close all windows 
    camera.release()
    cv2.destroyAllWindows()

