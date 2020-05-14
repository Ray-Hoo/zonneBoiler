#!/usr/bin/env python
import os
import time
import datetime
import glob
from time import strftime

#change 28-0517c026dbff to the address of your sensor
temperature_sensor = '/sys/bus/w1/devices/28-0517c026dbff/w1_slave'

#read the temperature and process the data
def temperatureRead():
        t = open(temperature_sensor, 'r')
        lines = t.readlines()
        t.close()

        temperature_output = lines[1].find('t=')
        if temperature_output != -1:
                temperature_string = lines[1].strip()[temperature_output+2:]
                temperature_c = float(temperature_string)/1000
        return round(temperature_c,2)

#write the temperature with date and time to the screen
while True:
    temperature = temperatureRead()
    print temperature
    datetimeWrite = (time.strftime("%d-%m-%Y ") + "@ "+ time.strftime("%H:%M:%S"))
    print datetimeWrite
    break
