__author__ = 'sei'

import serial

DEFAULT_SERIAL = '/dev/ttyS0'
DEFAULT_BAUDRATE = 19200


ser = serial.Serial(DEFAULT_SERIAL, DEFAULT_BAUDRATE, timeout=1)

print ser.name          # check which port was really used
ser.write("?\r")      # write a string

#while(1)
input = ser.readlines()
input = input[0].split("\r")

print(input)

#for i in range(25):
#    print ser.readline()


ser.close()             # close port