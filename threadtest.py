from picamera import PiCamera
from threading import Thread

class myCamrecord():
    def __init__(self,resolution=(1280,720),framerate=45,RecLen=5):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.Reclen = RecLen

    def RecordVideo(self)
        self.camera.start_recording("testvid.h264",foramt="h264", quality=23)
        self.camera.wait_recording(5)
        self.camera.stop_recording()

ReVid = myCamrecord()
Camthread1 = Thread(None, ReVid.RecordVideo)
Camthread1.start()