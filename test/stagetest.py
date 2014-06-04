__author__ = 'sei'

import NanoControl as nano
import time
import math
from datetime import datetime

nc = nano.NanoControl()

#nc.home()

A = 2047 # amplitude in nm
T = 2 # cycle duration in s
n = 200  # number of steps per cycle
duration = 10 # duration in s

def millis():
    dt = datetime.now() - starttime
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

t = 0
starttime = datetime.now()
while (t < duration):
        t = millis()/1000
        sin_value = math.sin(2*math.pi/float(T)*t)
        print "Val: {0:6} | t: {1:.3f}".format(int(A*sin_value),t) + '  ' + '#'.rjust(int(10*sin_value+10))
        #nc._fine('A',A*sin_value)
        #print(nc._moverel(0,int(A*math.sin(2*math.pi/T*t))))
        time.sleep(float(T)/n)