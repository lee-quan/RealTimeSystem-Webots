
from controller import Robot

# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())

arms = []
wheelNames = ['wheel1','wheel2', 'wheel3', 'wheel4']
wheels = []
fingers = []
speeds = []
# Arms
for i in range(5):
    arms.append(robot.getDevice('arm'+str(i+1)))
# Wheels
for i in range(4):
    wheels.append(robot.getDevice(wheelNames[i]))
    speeds.append(14.81)
# Fingers
# for i in range(2):
    # fingers.append(robot.getDevice('finger'+str(i+1)))

for i in range(4):
    wheels[i].setVelocity(speeds[i])
    
while robot.step(timestep) != -1:
    for i in range(4):
        wheels[i].setVelocity(speeds[i])
    pass

# Enter here exit cleanup code.
