import numpy as np
import cv2
from constants import *

def getRawImage(sim, visionSensor, resX = 0, resY = 0):
    img, [resInX, resInY] = sim.getVisionSensorImg(visionSensor, 0, 
                                                      0.0, [0, 0], 
                                                      [resX, resY])   
    return img, [resInX, resInY]

def getThresh(image, resX, resY):
    # Change image format to uint8 array and reshape it
    img = np.frombuffer(image, dtype=np.uint8)
    # Reshape image according to the resolution and dimensions
    img = img.reshape(resX, resY, 3)
    # Flip and Rotate image to get the right orientation
    # img = cv2.flip(img, 0)
    # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Transfer image to gray scale
    greyImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Get image threshhold
    ret, thresh = cv2.threshold(greyImage, THRESH_LL, THRESH_UL, 0)    
    return thresh, img
    
def getCentroid(thresh, desCentroid):
    # Get the image moments
    M = cv2.moments(thresh)
    # Compute the centroid
    if M["m00"] == 0:
        cX = desCentroid
        cY = desCentroid
    else:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    # Debugging: printing the centroid 
    print("C_X: ", cX)
    return cX , cY

def showImage(viewStr, img):
    cv2.imshow(viewStr, img)
    cv2.waitKey(1)