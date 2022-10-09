from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
 
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
                 help = "path to where to the face cascade resides")
ap.add_argument("-o", "--output", required=True,
                 help = "path to output directory")
args = vars(ap.parse_args())

detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
print("[INFO] starting video stream..")
vs = VideoStream(src=0).start()
time.sleep(2.0)
total = 0
 
while True:
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width = 400)

    #detect grayscale
    rects = detector.detectMultiScale(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor =1.1,
        minNeighbours = 5, minSize = (30,30))
    
    for(x,y,w,h) in rects:
        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),2)
         
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    #when "x" pressed, write to the *original* dataframe
    if key == ord("x"):
        p = os.path.sep.join([args["output"], "{}.png".format(
            str(total).zfill(5))])
        cv2.imwrite(p,orig)
        total += 1
    
    #when "b" pressed -> break the loop 
    elif key == ord("b"):
        break
    
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up..")
cv2.destroyAllWindows()
vs.stop()