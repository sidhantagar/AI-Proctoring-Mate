# Object Detection using ImageAI and YOLO

#Loading Modules
import cv2
from imageai import Detection

#Defining Path
modelpath = ""

#Loading YOLO
yolo = Detection.ObjectDetection()
yolo.setModelTypeAsYOLOv3()
yolo.setModelPath(modelpath)
yolo.loadModel()

#Loading Camera
cam = cv2.VideoCapture(0) 

while True:
    #Read frames
    ret, img = cam.read()

    #Predict
    img, preds = yolo.detectCustomObjectsFromImage(input_image=img, 
                      custom_objects=None, input_type="array",
                      output_type="array",
                      minimum_percentage_probability=70,
                      display_percentage_probability=False,
                      display_object_name=True)
                      
    #Display predictions
    cv2.imshow("", img)
    print(preds)

    #Press 'q' or 'esc' to break
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

#Close camera
cam.release()
cv2.destroyAllWindows()
