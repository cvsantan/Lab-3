'''!
@file       Lab2ClosedLoop.py
@brief      Class for creating a proportional controller
@details    Class that initializes a proportional closed-loop controller.
            Contains methods to update actuation value
@author     Jakob Frabosilio, Ayden Carbaugh, Cesar Santana
@date       01/11/2022
'''

class ClosedLoop:
    
    def __init__(self,Kp):
        '''! Creates a speed controller object.
        @param Kp       A value of Kp to use for speed control correction
        '''
        
        ## Value of Kp
        self.Kp = Kp
        
        ## Duty cycle value (L_actual)
        self.lAct = 0
        
        ## List for time value storage
        self.timeVals = []
        
        ## List for measured position value storage
        self.measVals = []
        
        ## List for reference position value storage
        self.refVals = []
        
        
    def update(self,wRef,wCalc,time=0,saveData=False):
        '''! Updates the current duty cycle value for a motor.
        @param wRef     The reference velocity that is being targeted
        @param wCalc    The current measured velocity of the motor
        @param time     The current time, used for plotting purposes
        @return         Returns the updated duty cycle value
        '''
        
        # Kp * (omega_ref - omega_measured) is the equation for a basic speed controller
        self.lAct = self.Kp * (wRef - wCalc)
        if saveData:
            self.timeVals.append(time)
            self.measVals.append(wCalc)
            self.refVals.append(wRef)
        
        # Duty cycle value cannot be larger than +-100%; if value exceeds +-100, set to +-100
        if self.lAct > 100:
            self.lAct = 100
        elif self.lAct < -100:
            self.lAct = -100
             
        return self.lAct
    
    def setKp(self,Kp):
        '''! Sets the value of Kp.
        @param Kp       The desired value of Kp
        '''
        self.Kp = Kp
        
        
    def getKp(self):
        '''! Returns the current value of Kp
        @return         Returns Kp
        '''
        return self.Kp
    
    def clearResults(self):
        '''! Clears the values of timeVals, measVals, and refVals
        '''
        self.timeVals = []
        self.measVals = []
        self.refVals = []