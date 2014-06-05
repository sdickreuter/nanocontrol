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
                self._serial = serial.Serial(d.DEFAULT_SERIAL, d.DEFAULT_BAUDRATE, timeout=0.1)
            else:
                self._serial = serial.Serial(port, d.DEFAULT_BAUDRATE, timeout=0.1)
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
        if channel in ('A','B'):
            if (steps >= -65536) & (steps <= 65535):
                self._serial.write('coarse '+channel+' '+str(steps)+'\r')
                return self._read_return_status()
        raise RuntimeError('illegal parameters in _coarse(channel, steps)')

    def _get_coarse_counter(self, channel):
        self._serial.write('coarse ?\r')
        return self._read_return_status()

    def _coarse_reset(self):
        self._serial.write('coarsereset\r')
        return self._read_return_status()


    def _fine(self, channel, steps):
        if channel in ('A','B'):
            if (steps >= -2048) & (steps <= 2047):
                self._serial.write('fine '+channel+' '+str(steps)+'\r')
                return self._read_return_status()
        raise RuntimeError('illegal parameters in _fine(channel, steps)')

    def _get_fine_counter(self):
        """


        :return:
        """
        self._serial.write('fine ?\r')
        return self._read_return_status()

    def _relax(self):
        """
        relax all channels (no voltage on the piezos)

        :return: return status
        """
        self._serial.write('relax\r')
        return self._read_return_status()

    def _moveabs(self, x=None, y=None, channel=None, pos=None):
        """
        move stage to absolute coordinates (only when stage has encoders !)

        :param x: move x-axis to the x position in nanometers
        :param y: move y-axis to the y position in nanometers
        :param channel: if you only want to move one channel/axis, define channel here (A=x,B=y)
        :param pos: position in nm the channel is moved to
        :return: return status
        """
        if (x is not None) & (y is not None):
            self._serial.write('moveabs '+str(x)+' '+str(y)+'\r')
        elif (channel in ('A','B')) & (pos is not None):
            self._serial.write('moveabs '+channel+' '+str(pos)+'\r')
        return self._read_return_status

    def _moverel(self, dx=None, dy=None):
        """
        move the stage by dx and dy [nm]

        :param dx: move x-axis by dx nanometers
        :param dy: move y-axis by dy nanometers
        :return: return status, values of the counters
        """
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
        """
        homes both axes of the stage

        :return: returns counter values after homing
        """
        self._moveabs(x=-200000,y=-200000)
        self._counterreset()
        self._moveabs(x=1000,y=1000)
        time.sleep(0.2)
        self._relax()
        time.sleep(0.2)
        return self._counterreset()
