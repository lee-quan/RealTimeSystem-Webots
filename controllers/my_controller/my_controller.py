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
targetRed=[-1.88,-2.14,-2.3,0]
targetBlue=[-1.88,2.14,-2,-1]
targetGreen=[-3,-0.5,-2.3,0.3]
test=[-3,-0.5,-2.3,0.3]

# targetRed=[-1.88,-2.14]
# targetBlue=[-1.88,2.14]
# targetGreen=[-1.88,-1.14]

handmotor=[]
handmotor.append(robot.getDevice('finger_1_joint_1'))
handmotor.append(robot.getDevice('finger_2_joint_1'))
handmotor.append(robot.getDevice('finger_middle_joint_1'))

urmotor=[]
urmotor.append(robot.getDevice('shoulder_lift_joint'))
urmotor.append(robot.getDevice('elbow_joint'))
urmotor.append(robot.getDevice('wrist_1_joint'))
urmotor.append(robot.getDevice('wrist_2_joint'))
shoulderpanjoint = robot.getDevice('shoulder_pan_joint')
wrist3joint = robot.getDevice('wrist_3_joint')

# urmotor[0].setPosition(test[0])
# urmotor[1].setPosition(test[1])
# urmotor[2].setPosition(test[2])
# urmotor[3].setPosition(test[3])

speed = 3.0;
for x in urmotor:
    x.setVelocity(speed)
distanceSensor = robot.getDevice('distance sensor')
distanceSensor.enable(timestep)

positionSensor = robot.getDevice('wrist_1_joint_sensor')
positionSensor.enable(timestep)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    numOfObjects = camera.getRecognitionNumberOfObjects();
    
    objects = camera.getRecognitionObjects()
    for i in objects:
        print(i.model)
        for j in range(i.getNumberOfColors()):
            a=i.getColors()[3*j]
            b=i.getColors()[3*j+1]
            c=i.getColors()[3*j+2]

    if counter <=0:
        
        match status:
            case 'WAITING':
                if(distanceSensor.getValue() < 150):
                    counter=8
                    print(counter, "COUNTER!!")
                    status='GRABBING'
                    print('GRABBING')
                    for i in handmotor:
                        i.setPosition(0.85)
                        
            case 'GRABBING':
                counter=30
                status='ROTATING'
                if(a==1.0):
                    target=targetRed
                elif(b==1.0):
                    target=targetGreen
                else:
                    target=targetBlue
                print('ROTATING')
                for i in range(4):
                    urmotor[i].setPosition(target[i])
                    
            case 'ROTATING':
                status='RELEASING'
                print(status)
                counter=8
                for i in handmotor:
                    i.setPosition(i.getMinPosition())
            case 'RELEASING':
                status='ROTATING BACK'
                print(status);
                for i in urmotor:
                    i.setPosition(0.0)
                shoulderpanjoint.setPosition(0.0)
                wrist3joint.setPosition(0.0)
            case 'ROTATING BACK':
                if(positionSensor.getValue() > -0.1):
                    status='WAITING'
                    print(status)

    else:
        counter = counter -1
    pass

# Enter here exit cleanup code.
