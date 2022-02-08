

import gc
from pyb import USB_VCP
import pyb
from Lab1EncoderClass import EncoderClass
from Lab1MotorDriver import MotorDriver
from Lab2ClosedLoop import ClosedLoop
import utime
import cotask
import task_share


testEncoder_1 = EncoderClass(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)

testEncoder_2 = EncoderClass(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)

testMotor_1 = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)

testMotor_2 = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)

testLoop_1 = ClosedLoop(0.92)

testLoop_2 = ClosedLoop(0.92)

def mot_1 ():
    testEncoder_1.zero()
    ref_1 = 180
    pos_1 = 0
    duty_1 = 0
    while True:
        print('m1')
        pos_1 = testEncoder_1.update()
        print(pos_1)
        duty_1 = testLoop_1.update(ref_1, pos_1, 0, saveData=False)
        print(duty_1)
        testMotor_1.set_duty_cycle(duty_1)
        yield (0)
        
def mot_2 ():
    testEncoder_2.zero()
    ref_2 = 360
    pos_2 = 0
    duty_2 = 0
    while True:
        pos_2 = testEncoder_2.update()
        print('m2')
        print(pos_2)
        duty_2 = testLoop_2.update(ref_2, pos_2, 0, saveData=False)
        print(duty_2)
        testMotor_2.set_duty_cycle(-duty_2)
        yield (0)


if __name__ == '__main__':
    
    task_1 = cotask.Task(mot_1, name = 'Task_1', priority = 1, period = 10, profile=True, trace=False)
    
    task_2 = cotask.Task(mot_2, name = 'Task_2', priority = 2, period = 10, profile=True, trace=False)
    
    cotask.task_list.append(task_1)
    cotask.task_list.append(task_2)
    
    while True:
        cotask.task_list.pri_sched()
   
    
    
    
    

    
    
    
