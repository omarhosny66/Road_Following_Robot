import time
import numpy as np
from numpy import savetxt
import cv2
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')

robot2_right_motor = sim.getObject("/PioneerP3DX[1]/rightMotor")
robot2_left_motor = sim.getObject("/PioneerP3DX[1]/leftMotor")
robot2_camera = sim.getObject("/PioneerP3DX[1]/Vision_sensor")

sim.setStepping(True)

sim.startSimulation()

# robot2_img, robot2_res = sim.getVisionSensorImg(robot2_camera, 0, 0.0, [0, 0], [0, 0])

# uint8Numbers = sim.unpackUInt8Table(robot2_img)

# # print(robot2_img)
# print("Resolution = \n" + str(robot2_res))
# print("\nImage Size = \n" + str(len(uint8Numbers)))
# # print(uint8Numbers)
# print('\n')

while (t := sim.getSimulationTime()) < 3:
    s = f'Simulation time: {t:.2f} [s]'
    print(s)
    
    img, [resX, resY] = sim.getVisionSensorImg(robot2_camera, 0, 
                                                      0.0, [0, 0], 
                                                      [80, 80])
    img = np.frombuffer(img, dtype=np.uint8).reshape(80, 80, 3)
    # # Setting the print options 
    # np.set_printoptions(threshold = np.inf)
    # print("image reshape: \n")
    # print("type: " + str(type(img)) + '\n')
    # print("size: " + str(len(img)) + '\n')
    # print(img)

    # In CoppeliaSim images are left to right (x-axis), and bottom to top (y-axis)
    # (consistent with the axes of vision sensors, pointing Z outwards, Y up)
    # and color format is RGB triplets, whereas OpenCV uses BGR:
    img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_left = img[0:80, 0:20]
    img_right = img[0:80, 60:80]
    left_img_mean = cv2.mean(img_left)
    left_color_mean = (left_img_mean[0] + left_img_mean[1] + left_img_mean[2]) / 3
    right_img_mean = cv2.mean(img_right)
    right_color_mean = (right_img_mean[0] + right_img_mean[1] + right_img_mean[2]) / 3

    print("left image mean: " + str(left_img_mean))
    print("left color mean: " + str(left_color_mean))
    print("right image mean: " + str(right_img_mean))
    print("right color mean: " + str(right_color_mean))

    # Setting the print options 
    np.set_printoptions(threshold = np.inf)
    # print("image flip: \n")
    # print("type: " + str(type(img)) + '\n')
    # print("size: " + str(len(img)) + '\n')
    # print(img[0])
    # print(img[len(img)-1])
    cv2.imshow('', img)
    cv2.waitKey(1)
    sim.step()  # triggers next simulation step

    sim.setJointTargetVelocity(robot2_right_motor, 5.0)
    sim.setJointTargetVelocity(robot2_left_motor, 4.0)

    time.sleep(0.2)

# while (t := sim.getSimulationTime()) < 3:
#     s = f'Simulation time: {t:.2f} [s]'
#     print(s)
#     sim.step()

#     sim.setJointTargetVelocity(robot2_right_motor, 5.0)
#     sim.setJointTargetVelocity(robot2_left_motor, 5.0)

#     # time.sleep(0.2)

robot2_img, robot2_res = sim.getVisionSensorImg(robot2_camera, 0, 0.0, [0, 0], [0, 0])

uint8Numbers = sim.unpackUInt8Table(robot2_img)

# print(uint8Numbers)

cv2.destroyAllWindows()
sim.stopSimulation()