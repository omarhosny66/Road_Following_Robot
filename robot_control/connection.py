import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')

robot2_right_motor = sim.getObject("/PioneerP3DX[2]/rightMotor")
robot2_left_motor = sim.getObject("/PioneerP3DX[2]/leftMotor")
robot2_camera = sim.getObject("/PioneerP3DX[2]/Vision_sensor")

sim.setStepping(True)

sim.startSimulation()

robot2_img, robot2_res = sim.getVisionSensorImg(robot2_camera, 0, 0.0, [0, 0], [0, 0])

uint8Numbers = sim.unpackUInt8Table(robot2_img)

# print(robot2_img)
print("Resolution = \n" + str(robot2_res))
print("\nImage Size = \n" + str(len(uint8Numbers)))
# print(uint8Numbers)
print('\n')

while (t := sim.getSimulationTime()) < 2:
    s = f'Simulation time: {t:.2f} [s]'
    print(s)
    sim.step()

    sim.setJointTargetVelocity(robot2_right_motor, 5.0)
    sim.setJointTargetVelocity(robot2_left_motor, 3.0)

    # time.sleep(0.2)

while (t := sim.getSimulationTime()) < 3:
    s = f'Simulation time: {t:.2f} [s]'
    print(s)
    sim.step()

    sim.setJointTargetVelocity(robot2_right_motor, 5.0)
    sim.setJointTargetVelocity(robot2_left_motor, 5.0)

    # time.sleep(0.2)

robot2_img, robot2_res = sim.getVisionSensorImg(robot2_camera, 0, 0.0, [0, 0], [0, 0])

uint8Numbers = sim.unpackUInt8Table(robot2_img)

# print(uint8Numbers)

sim.stopSimulation()