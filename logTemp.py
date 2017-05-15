#!/usr/bin/python

import os
import time
import sqlite3 as mydb
import sys
""" Log Current Time, Temperature in Celsius and Fahrenheit
Returns a list [time, tempC, tempF] """
def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-03168598f0ff/w1_slave")
	tempfile_text = tempfile.read()
	currentTime=time.strftime('%x %X %Z')
	tempfile.close()
	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF=tempC*9.0/5.0+32.0
	return [currentTime, tempC, tempF]


def logTemp():
	con = mydb.connect('/home/pi/mydatabase.db')
	with con:
		try:
 			[t,C,F]=readTemp()
 			print "Current time is %s and temperature is: %s F" %(t,F)
 			cur = con.cursor()
 			sql = "insert into temps values('%s',%s)" %(t,F)
			#print "sql = '%s'"%(sql)
			cur.execute(sql)
 			print "Temperature logged"
 		except:
 			e = sys.exc_info()[0]
			print e


logTemp()
