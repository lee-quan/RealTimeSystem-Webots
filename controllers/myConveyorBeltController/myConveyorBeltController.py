from controller import Motor
from controller import Robot

robot = Robot()

belt = robot.getDevice('belt_motor')
timestep = int(robot.getBasicTimeStep())
while robot.step(timestep) != -1:
    belt.setVelocity(0.3)
    belt.setPosition(float('inf'))
    pass

# Enter here exit cleanup code.
