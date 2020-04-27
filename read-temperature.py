#!/usr/bin/env python
import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

temperature_sensor = '/sys/bus/w1/devices/28-0517c026dbff/w1_slave'

# MySQL/MariaDB variables
db = MySQLdb.connect(host="localhost", user="gebruiker",passwd="wachtwoord",db="temperature_database")
cur = db.cursor()

def temperatureRead():
    t = open(temperature_sensor, 'r')
    lines = t.readlines()
    t.close()

    temperature_output = lines[1].find('t=')
    if temperature_output != -1:
        temperature_string = lines[1].strip()[temperature_output+2:]
        temperature_c = float(temp_string)/1000
    return round(temperature_c,2)