'''!
@file         main.py
@author       Cesar Santana
@author       Ayden Carbaugh
@author       Jacob Frabosilio
@date         2/9/2022
'''

from pyb import USB_VCP
import pyb
from L3EncoderClass import EncoderClass
from L3MotorDriver import MotorDriver
from L3ClosedLoop import ClosedLoop
import utime
import cotask
import task_share

## Serial bus used to communicate with PC
myUSB = USB_VCP()
## Encoder 1 Object
testEncoder_1 = EncoderClass(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
## Encoder 2 Object
testEncoder_2 = EncoderClass(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
## Motor 1 Objcet
testMotor_1 = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
## Motor 2 Object
testMotor_2 = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)
## Closed Loop Controller Object for Motor 1
testLoop_1 = ClosedLoop(0.92)
## Closed Loop Controller Object for Motor 2
testLoop_2 = ClosedLoop(0.92)

def key_input():
    '''!
    This generator waits for a keyboard input and then
    sends a flag variable to initiate a tep response
    '''
    while True:
        if key_flag.get() == 0:
            if myUSB.any():
                userInput = myUSB.read(1).decode()         
                if userInput == 'g' or userInput == 'G':
                    key_flag.put(1)
        yield (0)
        
def mot_1 ():
    '''!
    This generator checks for a flag value and then runs a step
    response on motor one while simultaneously filling queues
    with positional and time data
    '''
    while True:
        if key_flag.get() == 1:
            list_flag.put(0)
            testEncoder_1.zero()
            stepTime_1 = utime.ticks_ms()
            ref_1 = 180
            pos_1 = 0
            duty_1 = 0
            time_diff = utime.ticks_diff(utime.ticks_ms(), stepTime_1)
            while not ref_pos.full():
                time_diff = utime.ticks_diff(utime.ticks_ms(), stepTime_1)
                pos.put(int(pos_1))
                time.put(int(time_diff))
                ref_pos.put(int(ref_1))
                pos_1 = testEncoder_1.update()
                duty_1 = testLoop_1.update(ref_1, pos_1, 0, saveData=False)
                testMotor_1.set_duty_cycle(duty_1)
                if ref_pos.full():
                    list_flag.put(1)
                yield (0)
        yield (0)
        
        
def mot_2 ():
    '''!
    This generator checks for a flag value and then runs a step
    response on motor two
    '''
    while True:
        if key_flag.get() == 1:
            testEncoder_2.zero()
            ref_2 = 360
            pos_2 = 0
            duty_2 = 0
            while not ref_pos.full():
                pos_2 = testEncoder_2.update()
                duty_2 = testLoop_2.update(ref_2, pos_2, 0, saveData=False)
                testMotor_2.set_duty_cycle(duty_2)
                yield (0)
        yield (0)
    

def show_queue():
    '''!
    This generator waits for a flag value and the appends queue data
    into lists, and then send the datat to the front end for plotting
    via serial communication
    '''
    while True:
        if list_flag.get() == 1:
            pos_list = []
            ref_list = []
            tim_list = []
            while pos.any():
                pos_list.append(pos.get())

            while ref_pos.any():
                ref_list.append(ref_pos.get())
            while time.any():
                tim_list.append(time.get())
                
            for times in tim_list:
                myUSB.write(str(times).encode())
                myUSB.write(','.encode())
            myUSB.write('|'.encode())
            
            for refs in ref_list:
                myUSB.write(str(refs).encode())
                myUSB.write(','.encode())
            myUSB.write('|'.encode())
            
            for meas in pos_list:
                myUSB.write(str(meas).encode())
                myUSB.write(','.encode())
            myUSB.write('|'.encode())
            
            myUSB.write(str(10).encode())
            myUSB.write('\n'.encode())
            key_flag.put(0)
            list_flag.put(0)
            
        yield (0)

        
if __name__ == '__main__':

    ## Queue used to store positional values of motor 1
    pos = task_share.Queue ('L', 100, thread_protect = False, overwrite = False, name = "pos")
    ## Queue used to store the reference position of motor 1
    ref_pos = task_share.Queue ('L', 100, thread_protect = False, overwrite = False, name = "ref_pos")
    ## Queue used to share the time elapsed between runs of gthe controller
    time = task_share.Queue ('L', 100, thread_protect = False, overwrite = False, name = "time")
    
    
    ## Shared flag variable used to indicate when a keyboard input has been made
    key_flag = task_share.Share ('h', thread_protect = False, name = "key_flag")
    ## Shared flag variable used to indicate when the queue is full
    list_flag = task_share.Share ('h', thread_protect = False, name = "list_flag")
    
    ## Creates key_input task
    task_0 = cotask.Task(key_input, name = 'Task_0', priority = 3, period = 10, profile=True, trace=False)
    ## Creates mot_1 task
    task_1 = cotask.Task(mot_1, name = 'Task_1', priority = 2, period = 12, profile=True, trace=False)
    ## Creates mot_2 task
    task_2 = cotask.Task(mot_2, name = 'Task_2', priority = 2, period = 12, profile=True, trace=False)
    ## Creates show_queue task
    task_3 = cotask.Task(show_queue, name = 'Task_3', priority = 1, period = 10, profile=True, trace=False)
    
    cotask.task_list.append(task_0)
    cotask.task_list.append(task_1)
    cotask.task_list.append(task_2)
    cotask.task_list.append(task_3)

    key_flag.put(0)
    while True:
        cotask.task_list.pri_sched()
            
                 


                
                 
                

                 
                

                    

                           
    
    
    
    

    
    
    
