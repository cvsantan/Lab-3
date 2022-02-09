'''!
@file       L3FrontEnd.py
@brief      
@details    
@author     Jakob Frabosilio, Ayden Carbaugh, Cesar Santana
@date       01/11/2022
'''

import time
import serial
import matplotlib.pyplot as myPlot
import matplotlib.ticker as ticker

def sendChar():
    ''' Triggers an input command that sends an ASCII character through the serial bus
    @return     Returns the uppercase variant of the inputted character.
    '''
    inv = input('Input: ')
    if inv.upper() != 'H':
        ser.write(str(inv).encode('ascii'))
    return inv.upper()

def cmdsMsg():
    ''' Prints the list of possible inputs
    '''
    print('\nCHARACTER | ACTION')
    print('  G / g   | Step response activate.')
    print('  S / s   | Send data to serial and reset.')

ser = serial.Serial(port='COM5',baudrate=115273,timeout=1)

startTime = time.time()
state = 0
n = 0
i = 0
timeValsAppend = []
refValsAppend = [] 
measValsAppend = []
kpAppend = []
timeVals = []
refVals = []
measVals = []
kpVals = []

## String that holds raw string data sent from Nucleo, from data collection state
csvList = ''

cmdsMsg()

while True:
    if state == 0: # input state
        # If one second has not elapsed since last input, wait until it has.
        # This allows time for the Nucleo to send serial data over the
        # serial bus and is a UX decision for the user.
        if time.time() - startTime > 1 and ser.in_waiting == 0:
            myChar = sendChar()
            if myChar == 'S':
                startTime = time.time()
                state = 3
                print('please')
            elif myChar == 'G':
                startTime = time.time()
                state = 1
                print('listen')
            else:
                cmdsMsg()
                startTime = time.time()
                
        elif ser.in_waiting != 0:
            print(ser.readline().decode('ascii'))

    elif state == 1: # data collection
        if time.time() - startTime > 2.5:
            while ser.in_waiting != 0:
                csvList += ser.read().decode()
            if ser.in_waiting == 0:
                state = 2
                print('work')
            startTime = time.time()
            
    elif state == 2:
#         print(csvList)
        try:
            splitCSV = csvList.split('|')

#             splitCSV[0] = splitCSV[0].strip('g\r\n')
            timeValsAppend = splitCSV[0].split(',')
            refValsAppend = splitCSV[1].split(',')
            measValsAppend = splitCSV[2].split(',')
            kpAppend = splitCSV[3]
            timeValsAppend.pop()
            refValsAppend.pop()
            measValsAppend.pop()
            for times in timeValsAppend:
                timeValsAppend[i] = float(times)
                i += 1
            i = 0
            for refs in refValsAppend:
                refValsAppend[i] = float(refs)
                i += 1
            i = 0
            for meas in measValsAppend:
                measValsAppend[i] = float(meas)
                i += 1
            i = 0
            timeVals.append(timeValsAppend)
            refVals.append(refValsAppend)
            measVals.append(measValsAppend)
            kpVals.append(kpAppend)
#             print(len(timeVals))
#             print(timeVals)
#             print(refVals)              
#             print(measVals)
            csvList = ''
        except ValueError: 
            pass
        state = 0
        
    elif state == 3:
        if timeVals != ['']:
            fig, ax = myPlot.subplots(1, 1)
            for lines in measVals:
                ax.plot(timeVals[n], lines, ls = '-', label = 'Measured Values, Kp = ' + str(kpVals[n]))
                n += 1
            ax.plot(timeVals[0], refVals[0], color = 'k', ls = ':', label = 'Reference Values')
#             ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
#             ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
            myPlot.xlabel('Time (ms)')                     # sets axes labels
            myPlot.ylabel('Position (degrees)')
#             myPlot.legend()                                     # turns on legend
            myPlot.show()
            timeVals = []
            refVals = []
            measVals = []
            kpVals = []
        n = 0
        state = 0
