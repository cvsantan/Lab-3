'''!
@file       Lab1EncoderClass.py
@brief      Class for reading from an encoder
@details    Class that initializes an encoder given input pins and a timer.
            Contains methods to zero and update (read from) the encoder.
            Configured to convert from ticks to degrees using 16:1 ratio,
            256 CPR optical encoder readings.
@author     Jakob Frabosilio, Ayden Carbaugh, Cesar Santana
@date       01/11/2022
'''

import pyb

class EncoderClass:
    '''!
    This class implements a motor driver for an ME405 project
    '''
    
    def __init__(self, in1pin, in2pin, timer):
        '''!
        Creates the encoder object.
        @param in1pin         A pyb.Pin object for the encoder channel A
        @param in2pin         A pyb.Pin object for the encoder channel B
        @param timer          The number of the timer to be used by the encoder
        '''

        self.period = 65535
        self.tim = pyb.Timer(timer, prescaler=0, period=self.period)
        self.tch1 = self.tim.channel(1, pyb.Timer.ENC_A, pin=in1pin)
        self.tch2 = self.tim.channel(2, pyb.Timer.ENC_B, pin=in2pin)
        self.pos = 0
        self.lastpos = 0
        self.count = 0
        self.lastCount = 0
        self.delta = 0
        self.lastDelta = 0

    
    def zero(self):
        '''!
        Sets the position of the encoder and the counter to zero.
        '''
        self.pos = 0
        self.lastpos = 0
        self.count = 0
        self.tim.counter(0)

    
    def update(self):
        '''!
        Updates the current position (in degrees) of the motor based on the last updated position.
        '''
        self.lastPos = self.pos
        self.lastCount = self.count
        self.count = self.tim.counter()
        self.delta = self.count - self.lastCount
        
        # Makes sure that the delta value hasn't overflowed over the period, and corrects it
        if self.delta > self.period / 2:
            self.delta -= self.period
        elif self.delta < -self.period / 2:
            self.delta += self.period
            
        # As measured on this encoder, 360 degrees of rotation is equivalent to 256*32 ticks
        # with a prescaler of 0
        self.delta = self.delta * 360 / (256*16*2)
        self.pos += self.delta
        return self.pos