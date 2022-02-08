

import gc
from pyb import USB_VCP
import pyb
from L3EncoderClass import EncoderClass
from L3MotorDriver import MotorDriver
from L3ClosedLoop import ClosedLoop
import utime
import cotask
import task_share


myUSB = USB_VCP()

testEncoder_1 = EncoderClass(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)

testEncoder_2 = EncoderClass(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)

testMotor_1 = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)

testMotor_2 = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)

testLoop_1 = ClosedLoop(0.92)

testLoop_2 = ClosedLoop(0.92)

def key_input():
    while True:
        if key_flag.get() == 0:
            if myUSB.any():
                userInput = myUSB.read(1).decode()         
                if userInput == 'g' or userInput == 'G':
                    key_flag.put(1)
        yield (0)
        
def mot_1 ():
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
    while True:
        if key_flag.get() == 1:
            testEncoder_2.zero()
            ref_2 = 360
            pos_2 = 0
            duty_2 = 0
            stepTime_2 = utime.ticks_ms()       
            time_diff = utime.ticks_diff(utime.ticks_ms(), stepTime_2)
            while not ref_pos.full():
                time_diff = utime.ticks_diff(utime.ticks_ms(), stepTime_2)
                duty_2 = testLoop_2.update(ref_2, pos_2, 0, saveData=False)
                testMotor_2.set_duty_cycle(-duty_2)
                yield (0)
        yield (0)
    

def show_queue():
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

# def send_data()
#     while True:
        
if __name__ == '__main__':

    
    pos = task_share.Queue ('L', 75, thread_protect = False, overwrite = False, name = "pos")
    ref_pos = task_share.Queue ('L', 75, thread_protect = False, overwrite = False, name = "ref_pos")
    time = task_share.Queue ('L', 75, thread_protect = False, overwrite = False, name = "time")
    
    key_flag = task_share.Share ('h', thread_protect = False, name = "key_flag")
    list_flag = task_share.Share ('h', thread_protect = False, name = "list_flag")
    
    task_0 = cotask.Task(key_input, name = 'Task_0', priority = 2, period = 10, profile=True, trace=False)
    task_1 = cotask.Task(mot_1, name = 'Task_1', priority = 1, period = 10, profile=True, trace=False)
#     task_2 = cotask.Task(mot_2, name = 'Task_2', priority = 1, period = 10, profile=True, trace=False)
    task_3 = cotask.Task(show_queue, name = 'Task_3', priority = 1, period = 10, profile=True, trace=False)
    
    cotask.task_list.append(task_0)
    cotask.task_list.append(task_1)
#     cotask.task_list.append(task_2)
    cotask.task_list.append(task_3)

    key_flag.put(0)
    while True:
        cotask.task_list.pri_sched()
            
                 
#         elif state == 2:
#             for times in tim_list:
#                 myUSB.write(str(times).encode())
#                 myUSB.write(','.encode())
#             myUSB.write('|'.encode())
#             
#             for refs in ref_list:
#                 myUSB.write(str(refs).encode())
#                 myUSB.write(','.encode())
#             myUSB.write('|'.encode())
#             
#             for meas in pos_list:
#                 myUSB.write(str(meas).encode())
#                 myUSB.write(','.encode())
#             myUSB.write('|'.encode())
#             
#             myUSB.write(str(10).encode())
#             myUSB.write('\n'.encode())
#             state = 0

                
                 
                

                 
                

                    

                           
    
    
    
    

    
    
    
