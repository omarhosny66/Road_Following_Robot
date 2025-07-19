from utils import *
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from constants import *

class Robot:

    def __init__(self, name, simHandle):
        # Instance private variables
        self.__name = name
        self.__simHandle = simHandle
        self.__leftMotor = simHandle.getObject(name + "/leftMotor")
        self.__rightMotor = simHandle.getObject(name + "/rightMotor")
        self.__visionSensor = simHandle.getObject(name + "/Vision_sensor")
        self.__error_prev = 0.0
        self.__integral = 0.0
        self.__integral_reset = 0

    @property
    def name(self):
        return self.__name

    def getDiffFactor(self, desCentroid, actCentroid):
        # Calculate the error in X direction
        error = desCentroid - actCentroid
        # Update intergral and derivative elements
        self.__integral = self.__integral + error
        derivative = error - self.__error_prev
        # Compute pid controller output
        pidOutput = KP * error + KI * self.__integral + KD * derivative
        print("PID: ", pidOutput)
        # Store previous error
        self.__error_prev = error
        print("Error: ", error)
        # Reset integral error for windup
        if (self.__integral_reset < 10): 
            self.__integral_reset += 1
        else:
            self.__integral_reset = 0
            self.__integral = 0.0
        
        # return the differential factor
        diffFactor = (pidOutput)
        return diffFactor

    def move(self, velocity, diffFactorX):
        # Calculate left motor velocity
        lMV = velocity + (diffFactorX)
        # Calcualte right motor velocity
        rMV = velocity - (diffFactorX)
        # Debugging: printing motors' velocities
        print("leftV: ", lMV)
        print("rightV: ", rMV)
        # Feeding the updated velocities to motors
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, lMV)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, rMV)

    def update(self, velocity = DEF_VEL, showImg = False):
        # Update robot image
        rawImage, [resX, resY] = getRawImage(self.__simHandle, self.__visionSensor, RES_X, RES_Y)
        # Get desired centroid according to configured resolution
        dCent = resX/2
        # Update threshhold
        thresh, image = getThresh(rawImage, RES_X, RES_Y)
        # Update actual centroid
        aCentX, aCentY = getCentroid(thresh, dCent)
        # Update differential factor
        dFX = self.getDiffFactor(dCent, aCentX)
        # Update the robot motors' velocity
        self.move(velocity, dFX)
        # Check the parameter showImage and stream the vision sensor accordingly
        if (showImg): 
            showImage((self.__name + "/Image"), image)       


    def stop(self):
        self.__simHandle.setJointTargetVelocity(self.__leftMotor, 0)
        self.__simHandle.setJointTargetVelocity(self.__rightMotor, 0)
        