from controller import Robot
from controller import Emitter
from controller import Camera
from enum import Enum

robot = Robot()
emitter = Emitter('emitter')

timestep = int(robot.getBasicTimeStep())
camera = Camera('CAM')
camera.enable(timestep)
camera.recognitionEnable(timestep)

counter=0
counter1=0
i=0
state = 'WAITING'
emitter.send(state)
targetRed=[-1.88,-2,-2.3,0]
targetBlue=[-1.88,2.14,-2,-1]
targetGreen=[-3,-0.5,-2.3,0.3]
test=[-3,-0.5,-2.3,0.3]

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

#urmotor[0].setPosition(test[0])
#urmotor[1].setPosition(test[1])
#urmotor[2].setPosition(test[2])
#urmotor[3].setPosition(test[3])

speed = 5.0;
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
    currState = state
    objects = camera.getRecognitionObjects()
    for i in objects:
        object = i.model
        for j in range(i.getNumberOfColors()):
            a=i.getColors()[3*j]
            b=i.getColors()[3*j+1]
            c=i.getColors()[3*j+2]
    if counter <=0:
        match state:
            case 'WAITING':
                if(distanceSensor.getValue() < 150):
                    counter=8
                    state='GRABBING'
                    emitter.send(state)
                    for i in handmotor:
                        i.setPosition(0.85)
                        
            case 'GRABBING':
                counter=50
                state='ROTATING'
                emitter.send(state)
                if(object=='bottle'):
                    target=targetRed
                elif(object=='can'):
                    target=targetGreen
                else:
                    target=targetBlue
                for i in range(4):
                    urmotor[i].setPosition(target[i])
                    
            case 'ROTATING':
                state='RELEASING'
                emitter.send(state)
                counter=60
                for i in handmotor:
                    i.setPosition(i.getMinPosition())
            case 'RELEASING':
                counter=30
                state='ROTATING BACK'
                emitter.send(state)
                for i in urmotor:
                    i.setPosition(0.0)
                shoulderpanjoint.setPosition(0.0)
                wrist3joint.setPosition(0.0)
            case 'ROTATING BACK':
                if(positionSensor.getValue() > -0.1):
                    state='WAITING'
                    emitter.send(state)

    else:
        counter = counter -1
    pass

# Enter here exit cleanup code.
