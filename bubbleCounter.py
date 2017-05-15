#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sqlite3 as mydb


def logBubble():
	currentTime=time.strftime('%x %X %Z')
	
	con = mydb.connect('/home/pi/mydatabase.db')
        with con:
                try:
                        cur = con.cursor()
                        sql = "insert into bubbles values('%s')" %(currentTime)
                        cur.execute(sql)
                        print "bubble logged"
                except:
                        e = sys.exc_info()[0]
                        print e



GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(37,GPIO.IN)

while True:
	if(GPIO.input(37) == 1):
		logBubble()
		time.sleep(0.5)	

#transmitter = gpio pin 12 GPIO18
