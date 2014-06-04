__author__ = 'sei'

import NanoControl as nano
import time
import math
from datetime import datetime

nc = nano.NanoControl()

#nc.home()

A = 5000 # amplitude in nm
T = 10 # cycle duration in s
n = 100  # number of steps per cycle
duration = 10000 # duration in ms

def millis():
    dt = datetime.now() - starttime
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

t = 0
starttime = datetime.now()
while (t < duration):
        t = millis()
        #print( int(A*math.sin(2*math.pi/T*t)))
        print(nc._moverel(0,int(A*math.sin(2*math.pi/T*t))))
        #time.sleep(T/n)