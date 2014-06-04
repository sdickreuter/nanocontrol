__author__ = 'sei'

import serial
import time
import sys
import _defines as d

class NanoControl(object):
    _x = 0
    _y = 0

    def __init__(self, port=None):
        try:
            if port is None:
                self._serial = serial.Serial(d.DEFAULT_SERIAL, d.DEFAULT_BAUDRATE, timeout=1)
            else:
                self._serial = serial.Serial(port, d.DEFAULT_BAUDRATE, timeout=1)
        except:
            self._serial.close()
            raise RuntimeError('Could not open serial connection')

        if self._serial is None:
            raise RuntimeError('Could not open serial connection')

        print('NanoControl initialized on port %s' %self._serial.name)
        self._serial.write('version\r')
        print('Firmware Version: ' + self._read_return_status())
        self._x, self._y = self._counterread()


    def _read_return_status(self):
        buf = self._serial.readline()
        buf = buf.split("\t")
        if buf[0] == 'e':
           raise RuntimeError('Return Status reported an error')

        return buf[1]

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

    def _moveabs(self, x=None, y=None, channel=None, pos=None):
        if (x is not None) & (y is not None):
            self._serial.write('moveabs '+str(x)+' '+str(y)+'\r')
        elif (channel in ('A','B')) & (pos is not None):
            self._serial.write('moveabs '+channel+' '+str(pos)+'\r')
        return self._read_return_status

    def _moverel(self, dx=None, dy=None):
        x, y = self._counterread()
        self._moveabs(x=x+dx,y=y+dy)
        return self._read_return_status()

    def _counterread(self):
        """
        return position in nm
        """
        self._serial.write('counterread\r')
        buf = self._read_return_status()
        buf = buf.split(' ')
        return int(buf[0]), int(buf[1])

    def _counterreset(self):
        """
        resets all position counters

        :return: return status, values of the counters
        """
        self._serial.write('counterreset\r')
        return self._read_return_status()


    def home(self):
        self._moveabs(x=-200000,y=-200000)
        self._counterreset()
        self._moveabs(x=1000,y=1000)
        time.sleep(0.2)
        print(self._counterreset())
