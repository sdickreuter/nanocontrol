__author__ = 'sei'

import serial
import time
import sys
import _defines as d

class OceanOpticsSpectrometer(object):
    _x = 0
    _y = 0

    def __init__(self):
        try:
            self._serial = serial.Serial(d.DEFAULT_SERIAL, d.DEFAULT_BAUDRATE, timeout=1)
        finally:
            self._serial.close()
            raise RuntimeError('Could not open serial connection')

        if self._serial == None:
            raise RuntimeError('Could not open serial connection')

    def _read_return_status(self):
        buf = self._serial.readline()
        print (buf)
        return 0

    def _coarse(self, channel, steps):
        pass

    def _get_coarse_counter(self, channel):
        pass

    def _coarse_reset(self, channel):
        pass

    def _fine(self, channel, steps):
        pass

    def _get_fine_counter(self):
        pass

    def _fine_reset(self, channel):
        pass

    def _moveabs(self,x=None,y=None,channel=None,pos=None):
        if (x != None) & (y != None):
            self._serial.write('moveabs '+str(x)+' '+str(y))
        elif (channel in ('A','B')) & (pos != None):
            self._serial.write('moveabs '+channel+' '+str(pos))
        return self._read_return_status

    def _moverel(self,dx=None,dy=None):
        x, y = self._counterread()
        self._moveabs(x=x+dx,y=y+dy)
        return 0

    def _counterread(self):
        """
        return position in nm
        """
        self._serial.write('counterread')
        print(self._serial.readlines())
        return (0,0)

    def _counterreset(self):
        pass

    def home(self):
        self._moveabs(x=-200000,y=-200000)
        self._counterreset()
        self._moveabs(x=1000,y=1000)
        time.sleep(0.2)
        self._counterreset()