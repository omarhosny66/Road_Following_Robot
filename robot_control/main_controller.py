from robot import Robot
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np
import cv2
import time

def main():
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    r2 = Robot("/PioneerP3DX[2]", sim)
    # Debugging
    robot2_camera = sim.getObject("/PioneerP3DX[2]/Vision_sensor")
    
    sim.setStepping(True)
    sim.startSimulation()
    while (t := sim.getSimulationTime()) < 30:
        s = f'Simulation time: {t:.2f} [s]'
        print(s)
        r2.start(5)

        # Debugging
        img, [resX, resY] = sim.getVisionSensorImg(robot2_camera, 0, 
                                                      0.0, [0, 0], 
                                                      [80, 80])
        img = np.frombuffer(img, dtype=np.uint8).reshape(80, 80, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img_left = img[0:80, 0:20]
        img_right = img[0:80, 60:80]
        left_img_mean = cv2.mean(img_left)
        left_color_mean = (left_img_mean[0] + left_img_mean[1] + left_img_mean[2]) / 3
        right_img_mean = cv2.mean(img_right)
        right_color_mean = (right_img_mean[0] + right_img_mean[1] + right_img_mean[2]) / 3

        # print("left image mean: " + str(left_img_mean))
        # print("left color mean: " + str(left_color_mean))
        # print("right image mean: " + str(right_img_mean))
        # print("right color mean: " + str(right_color_mean))

        # Setting the print options 
        # np.set_printoptions(threshold = np.inf)
        # print("image flip: \n")
        # print("type: " + str(type(img)) + '\n')
        # print("size: " + str(len(img)) + '\n')
        # print(img[0])
        # print(img[len(img)-1])
        cv2.imshow('', img)
        cv2.waitKey(1)
        sim.step()  # triggers next simulation step
        # time.sleep(0.1)

    cv2.destroyAllWindows()
    sim.stopSimulation()

if __name__ == '__main__':
    main()