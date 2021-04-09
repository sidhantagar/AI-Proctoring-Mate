import cv2
import numpy as np
import dlib
from facialLandmarksDetection import *
from blink import *

# Video stream generation
cap = cv2.VideoCapture(0)

#values hold the blink script Output
values = []

if(cap.isOpened()==False):
    cap.open()

while True:
    ret, frame = cap.read()
    
    # converting frame to grayscale
    # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    # these two lines inside frame read, will localize the face and mark the facial landmarks.
    # <!-- important --> must Run to know about the faces.
    faceCount,faces = detectFace(frame)
    #landmarkLocalisation(faces,frame)
    #isBlinking() will return a tuple of ratios and conclusion.
    values.append(isBlinking(faces,frame))
    
    
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()