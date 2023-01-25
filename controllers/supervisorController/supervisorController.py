from controller import Supervisor
from controller import Robot
from controller import Receiver
import array

timestep = 1
sv = Supervisor()
receiver = Receiver('receiver')
receiver.enable(1)
counter =0;
while sv.step(timestep) != -1:
    conveyor = sv.getFromDef('conveyor')
    speed = conveyor.getField('speed')
    if(receiver.getQueueLength()>0):
        if(receiver.getString() == 'WAITING'):
            speed.setSFFloat(0.3)
        else:
            speed.setSFFloat(0.0)
        print(receiver.getString())
        receiver.nextPacket()
    pass
