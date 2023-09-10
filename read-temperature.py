#!/usr/bin/env python3
import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

#change 28-0517c026dbff to the address of your sensor!
temperature_sensor = '/sys/bus/w1/devices/28-0517c026dbff/w1_slave'

# MySQL/MariaDB variables
db = MySQLdb.connect(host="localhost", user="gebruiker",passwd="wachtwoord",db="temperatuur_database")
cur = db.cursor()

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

#write the temperature with date and time onto the screen and into the SQL database
while True:
    temperature = temperatureRead()
    print temperature
    datewrite = time.strftime("%Y-%m-%d ") 
    timewrite = time.strftime("%H:%M:%S")
    print (datewrite + " @ " + timewrite)
    sql = ("""INSERT INTO temperatuurLog (datum,tijd,temperatuur) VALUES (%s,%s,%s)""",(datewrite,timewrite,temperature))
    try:
        print "Writing the data to the database..."
        # Executing the SQL command
        cur.execute(*sql)
        # Commiting the changes to the database
        db.commit()
        print "The data has been writen"

    except:
        # When there is an error -> rollback
        db.rollback()
        print "Failed to write to the database"

    cur.close()
    db.close()
    break
