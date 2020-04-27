!/usr/bin/env python
import os
import time
import datetime
import glob
from time import strftime

#change 28-0517c026dbff to the address of your sensor
temp_sensor = '/sys/bus/w1/devices/28-0517c026dbff/w1_slave'

def tempRead():
        t = open(temp_sensor, 'r')
        lines = t.readlines()
        t.close()

        temp_output = lines[1].find('t=')
        if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = float(temp_string)/1000.0
        return round(temp_c,1)

while True:
    temp = tempRead()
    print temp
    datetimeWrite = (time.strftime("%d-%m-%Y ") + time.strftime("%H:%M:%S"))
    print datetimeWrite
    break
