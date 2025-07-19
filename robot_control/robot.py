from utils import *
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

class Robot:

    def __init__(self, name, simHandle):
        self.__name = name
        self.__simHandle = simHandle
        self.__leftMotor = simHandle.getObject(name + "/leftMotor")
        self.__rightMotor = simHandle.getObject(name + "/rightMotor")
        self.__visionSensor = simHandle.getObject(name + "/Vision_sensor")
        self.__lock = False
        self.__dir = 0

    @property
    def name(self):
        return self.__name

    def getSegmentsMean(self):
        img, [resX, resY] = getImage(self.__simHandle, self.__visionSensor)
        img = formatImage(img, resX, resY)
        leftSeg, rightSeg = imageSeg(img, 20, resY, resX, resY)
        lSegMean = imageColorMean(leftSeg)
        rSegMean = imageColorMean(rightSeg)
        return lSegMean, rSegMean

    def computeWheelsFactor(self, velocity):
        l, r = self.getSegmentsMean()
        print("\n l: " + str(l))
        print("\n r: " + str(r))
        print("\n lock: " +str(self.__lock))
        # Todo: Add wait time
        if (int(l*100) > int(r*100)):
            self.__dir = 2
            self.__lock = True
        elif (int(l*100) < int(r*100)):
            self.__dir = 3
            self.__lock = True
        elif ((r == 0) and (l == 0)):
            self.__dir = 1
            self.__lock = False
        dir = self.__dir
        return dir
        # l, r = self.getSegmentsMean()
        # # Check if any segment contains color other than black
        # if (l or r):
        #     # Calculate difference factor
        #     lF = 1 - ((l - r)/(l + r))
        #     rF = 1 - ((r - l)/(r + l))
        #     # Normalize difference factor
        #     lN = lF/(lF+rF)
        #     rN = rF/(lF+rF)
        #     if (lN > rN): 
        #         lN = 1.2
        #         rN = 0.1 * rN
        #     else: 
        #         rN = 1.2
        #         lN = 0.1 * lN
        # else:
        #     lN = 1
        #     rN = 1
        # return lN, rN

    def moveForward(self, velocity):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, velocity)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, velocity)

    def moveBackward(self, velocity):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, velocity)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, velocity)

    def steerLeft(self, velocity):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, 0)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, velocity * 130)

    def steerRight(self, velocity):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, velocity * 130)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, 0)

    def move(self, velocity, leftWheelF, rightWheelF):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, velocity * leftWheelF)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, velocity * rightWheelF)
    
    def start(self, velocity):
        # # Compute left and right wheel factors
        # lWF , rWF = self.computeWheelsFactor()
        # # Call move function feeding updated factors
        # self.move(velocity, lWF, rWF)
        d = self.computeWheelsFactor(velocity)
        if (d == 1):
            print("\ndir: " + str(d))
            self.moveForward(velocity)
        elif (d == 2):
            print("\ndir: " + str(d))
            self.steerRight(velocity)
        elif (d == 3):
            print("\ndir: " + str(d))
            self.steerLeft(velocity)
        else:
            self.stop()
        

    def stop(self):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, 0)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, 0)
        