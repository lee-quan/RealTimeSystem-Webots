from controller import Robot
from controller import Camera
from enum import Enum

robot = Robot()

timestep = int(robot.getBasicTimeStep())

camera = Camera('CAM')
camera.enable(timestep)
camera.recognitionEnable(timestep)

counter=0
i=0
status = 'WAITING'
targetRed=[-1.0,2.0,-1.0,0.0]
targetBlue=[-0.532,0.05,0]
targetGreen=[0.443,0.05,0]

handmotor=[]
handmotor.append(robot.getDevice('finger_1_joint_1'))
handmotor.append(robot.getDevice('finger_2_joint_1'))
handmotor.append(robot.getDevice('finger_middle_joint_1'))

urmotor=[]
urmotor.append(robot.getDevice('shoulder_lift_joint'))
urmotor.append(robot.getDevice('elbow_joint'))
urmotor.append(robot.getDevice('wrist_1_joint'))
urmotor.append(robot.getDevice('wrist_2_joint'))

# urmotor[2].setPosition(0)
# urmotor[0].setPosition(0)
# urmotor[1].setPosition(0)

# urmotor[3].setPosition(-1)

speed = 1.0;
for x in urmotor:
    x.setVelocity(speed)
distanceSensor = robot.getDevice('distance sensor')
distanceSensor.enable(timestep)

positionSensor = robot.getDevice('wrist_1_joint_sensor')
positionSensor.enable(timestep)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    print(distanceSensor.getValue())
    numOfObjects = camera.getRecognitionNumberOfObjects();
    
    objects = camera.getRecognitionObjects()
    for i in objects:
        for j in range(i.getNumberOfColors()):
            a=i.getColors()[3*j]
            b=i.getColors()[3*j+1]
            c=i.getColors()[3*j+2]

    if counter <=0:

        match status:
            case 'WAITING':
                if(distanceSensor.getValue() < 200):
                    counter=8
                    print(counter, "COUNTER!!")
                    status='GRABBING'
                    print('GRABBING')
                    for i in handmotor:
                        i.setPosition(0.85)
                        
                        
            case 'GRABBING':
                counter=50
                status='ROTATING'
                for i in range(4):
                    urmotor[i].setPosition(targetRed[i])
                    
            case 'ROTATING':
                counter=8
                for i in handmotor:
                    i.setPosition(i.getMinPosition())


    else:

        counter = counter -1
    pass

# Enter here exit cleanup code.
