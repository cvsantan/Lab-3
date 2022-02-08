'''!
@file       Lab1MotorDriver.py
@brief      Class for controlling a motor
@details    Class that initializes a motor given I/O pins and a timer.
            Contains methods to set motor power from 0% to 100% using
            PWM control. An H-Bridge or physical motor driver board should
            be used for motor control.
@author     Jakob Frabosilio, Ayden Carbaugh, Cesar Santana
@date       01/11/2022
'''

import pyb

class MotorDriver:
    '''!
    This class implements a motor driver for an ME405 project.
    '''
    
    def __init__(self, en_pin, in1pin, in2pin, timer):
        '''!
        Initializes motor object given I/O pins and a timer.
        @param en_pin     A pyb.Pin object for the EN/OCD "toggle" pin
        @param in1pin     A pyb.Pin object for the IN1 pin (+)
        @param in2pin     A pyb.Pin object for the IN2 pin (-)
        @param timer      The number of the timer to be used by the motor
        '''
        
        self.en_pin = pyb.Pin(en_pin, pyb.Pin.PULL_UP)
        self.in1pin = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self.in2pin = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        self.tim = pyb.Timer(timer,freq = 20000)
        self.mPos = self.tim.channel(1, pyb.Timer.PWM, pin=self.in1pin)
        self.mNeg = self.tim.channel(2, pyb.Timer.PWM, pin=self.in2pin)
        self.en_pin.high()                                                # Enable EN pin
        self.mPos.pulse_width_percent(0)                                  # Set motor duty to 0 for safety
        self.mNeg.pulse_width_percent(0)                                  # Set motor duty to 0 for safety
        
        
    def set_duty_cycle(self, level):
        '''!
        Sets the duty cycle of the motor to the given level. Positive values cause
        torque in one direction, negative values cause torque in opposite direction.
        @param level     Duty cycle value between -100 and 100
        '''
        
        if level < 0 and level >= -100:
            self.mPos.pulse_width_percent(0)
            self.mNeg.pulse_width_percent(-level)
        elif level >= 0 and level <= 100:
            self.mPos.pulse_width_percent(level)
            self.mNeg.pulse_width_percent(0)