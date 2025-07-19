import numpy as np
import cv2

def getImage(sim, visionSensor, resX = 0, resY = 0):
    img, [resInX, resInY] = sim.getVisionSensorImg(visionSensor, 0, 
                                                      0.0, [0, 0], 
                                                      [resX, resY])   
    return img, [resInX, resInY]

def formatImage(image, resX, resY):
    img = np.frombuffer(image, dtype=np.uint8).reshape(resX, resY, 3)
    img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img
    
def imageSeg(image, segWidth, segLength, resX, resY):
    if(segWidth > resX): segWidth = resX
    if(segLength > resY): segLength = resY
    leftSeg = image[0:segLength, 0:segWidth]
    rightSeg = image[0:segLength, (resX-segLength):resX]
    return leftSeg, rightSeg

def imageColorMean(image):
    imgBgrMean = cv2.mean(image)
    imgColMean = (imgBgrMean[0] + imgBgrMean[1] + imgBgrMean[3]) / 3
    return imgColMean