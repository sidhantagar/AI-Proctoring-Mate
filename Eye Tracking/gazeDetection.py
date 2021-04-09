import cv2
import numpy as np
import dlib
from facialLandmarksDetection import *

print('import Success!!')

def generateEyeRegion(landmarks,eyeIndices):
    """
    Input : 68 facial landmark points, Indices of left or right eyes.
    Output : region covering respective eye, whose indices have been provided.
    """
    region = []
    for i in eyeIndices :
        region.append(
            (landmarks.part(i).x,landmarks.part(i).y)
        )
        
    return region


def createMask(frame):
    """
    Input : Video capture frame.
    Output : A black mask with the size of window's frame
    """
    
    height,width,channels = frame.shape
    mask = np.zeros((height,width),np.uint8)
    return mask
    
    
def extractEye(mask,region,frame):
    """
    Input : 
        - mask : A black mask.
        - region : list of regions to extract from the frame.
        - frame : Video capture frame.
    Output : extracted eyes (iris+pupil+sclera)
    """
    #put the polylines on the mask in the right and left eye region
    cv2.polylines(mask,region,True,255,2)
    cv2.fillPoly(mask,region,255)
        
    #eyes contains a masked frame for both the eyes.
    eyes = cv2.bitwise_and(frame,frame,mask = mask)
    return eyes


def eyeSegmentationAndReturnWhite(img,side):
    """
    Input : Threshold Image to be Bifercated [into sections] . 
    Output : White Pixels Count from the bifercated image.
    """
    
    height,width = img.shape
    if(side=='left'):
        img = img[0:height,0:int(width/2)]
        return cv2.countNonZero(img)
    else:
        img = img[0:height,int(width/2):width]
        return cv2.countNonZero(img)
    
    
def gazeDetection(faces,frame):
    """
    Input : list of all the localised faces from the video frame.
    Output : frame obtained from the video capture.
    
    Action : 
        - Region Extraction.
        - Mask Creation.
        - Eye Extraction.
        - Threshold Application.
        - Ratio Calculations For Gaze.
    
    Display :
        - frame with information of no. of white pixels in a region.
            ** region is bifercated using a segment bisector, in two equal halves[left and right]
            a) upper value represent the pixels of left half.
            b) lower value represent the pixels of right half.
            
        - headings are w.r.t person's original eye. & not w.r.t the cam's view.
    """
    
    #indices for the left and the right eye.
    #w.r.t camera view.
    #w.r.t subject, view is reversed.
    right = [36,37,38,39,40,41]
    left = [42,43,44,45,46,47]
    
    for face in faces :
        
        facialLandmarks = shapePredictor(frame,face)
        
        
        rightEyeRegion = np.array([(facialLandmarks.part(i).x,facialLandmarks.part(i).y) for i in right], np.int32)
        leftEyeRegion = np.array([(facialLandmarks.part(i).x,facialLandmarks.part(i).y) for i in left], np.int32)
        
        #<!--p3-->
        
        #create the mask of our eye,since the threshold does
        #not give us the exact replica of our eye : iris,pupil,sclera.
        
        mask = createMask(frame)
        eyes = extractEye(mask,[rightEyeRegion,leftEyeRegion],frame)
        
        #extracting the rectangular region covering whole of the eye
        #and presenting it on a seperate window.
        
        rmin_x = np.min(rightEyeRegion[:,0])
        rmax_x = np.max(rightEyeRegion[:,0])
        rmin_y = np.min(rightEyeRegion[:,1])
        rmax_y = np.max(rightEyeRegion[:,1])
        
        lmin_x = np.min(leftEyeRegion[:,0])
        lmax_x = np.max(leftEyeRegion[:,0])
        lmin_y = np.min(leftEyeRegion[:,1])
        lmax_y = np.max(leftEyeRegion[:,1])
        
        rightEye = eyes[rmin_y:rmax_y,rmin_x:rmax_x]
        leftEye = eyes[lmin_y:lmax_y,lmin_x:lmax_x]
        
        #converting the normal image to grayscale for applying Threshold.
        rightGrayEye = cv2.cvtColor(rightEye,cv2.COLOR_BGR2GRAY)
        leftGrayEye = cv2.cvtColor(leftEye,cv2.COLOR_BGR2GRAY)
        
        #THRESHOLD APPLICATION
        
        #global threshold
        #retVal, rightTh = cv2.threshold(rightGrayEye,60,255,cv2.THRESH_BINARY)
        #retVal, leftTh = cv2.threshold(leftGrayEye,60,255,cv2.THRESH_BINARY)
        
        #otsu threshold
        #retVal, threshold = cv2.threshold(grayEyes,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        #Adaptive threshold
        rightTh = cv2.adaptiveThreshold(rightGrayEye,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        leftTh = cv2.adaptiveThreshold(leftGrayEye,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        
        #segments of right eye's threshold
        leftSideOfRightTh = eyeSegmentationAndReturnWhite(rightTh,'left')
        rightSideOfRightTh = eyeSegmentationAndReturnWhite(rightTh,'right')
        #segments of left eye's threshold
        leftSideOfLeftTh = eyeSegmentationAndReturnWhite(leftTh,'left')
        rightSideOfLeftTh = eyeSegmentationAndReturnWhite(leftTh,'right')
        
        font = cv2.FONT_HERSHEY_PLAIN
        thickness = 5
        
        #for the right eye of the person
        cv2.putText(frame,'RIGHT',(50,90),font,2,(0,255,255),thickness)
        cv2.putText(frame,str(rightSideOfRightTh),(50,140),font,2,(0,255,255),thickness)
        cv2.putText(frame,str(leftSideOfRightTh),(50,190),font,2,(0,255,255),thickness)
        
        #for the left eye of the person
        cv2.putText(frame,'LEFT',(200,90),font,2,(0,255,255),thickness)
        cv2.putText(frame,str(rightSideOfLeftTh),(200,140),font,2,(0,255,255),thickness)
        cv2.putText(frame,str(leftSideOfLeftTh),(200,190),font,2,(0,255,255),thickness)
        
        
        rightTh = cv2.resize(rightTh,None,fx=10,fy=10)
        leftTh = cv2.resize(leftTh,None,fx=10,fy=10)
        
        cv2.imshow('RIGHT EYE',rightTh)
        cv2.imshow('LEFT EYE',leftTh)