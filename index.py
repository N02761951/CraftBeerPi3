 #!/usr/bin/python

import os
import time
from datetime import datetime,timedelta
import datetime
from dateutil import parser
import sqlite3 as mydb
import sys

print "Content-type:text/html\r\n\r\n"


"""
will take in a datetime and return a boolean weather
that datetime was within the last 24 hours
"""
def isWithin24(dateTime):
    
    #timeNow = time.strftime('%x %X %Z')
    #print "dateTime type = %s"%(type(dateTime))
    #print "dateTime = %s"%(dateTime)
    dateTimeU = dateTime[0]
    #print "dateTimeU = %s"%(dateTimeU)
    #print "dateTimeU type = %s"%(type(dateTimeU))

    stringdateSplit = dateTimeU.split()
    stringdate = stringdateSplit[0]+" "+stringdateSplit[1]

    stringdate2 = stringdateSplit[0].split("/")
    
    #gettting the exact month day and year from the string
    stringMonth = stringdate2[0]
    stringDay = stringdate2[1]
    stringYear = stringdate2[2]
    #print "month = %s day = %s year = %s"%(stringMonth,stringDay,stringYear)

    stringdateTime = stringdateSplit[1].split(":")
    stringHour = stringdateTime[0]
    stringMin = stringdateTime[1]
    stringSec = stringdateTime[2]
    #print "hour = %s min = %s second   = %s"%(stringHour,stringMin,stringSec)

    theDateTime = datetime.datetime(int(stringYear)+2000,int(stringMonth),int(stringDay),int(stringHour),int(stringMin),int(stringSec),0,None)
    #print "theDateTime = %s"%(theDateTime)
    #print "THE CURRENT DATE IS %s"%(datetime.datetime.now())
    aDayAgo = datetime.datetime.now() - timedelta(days=1)

    if(aDayAgo <= theDateTime <= datetime.datetime.now()):
        return True
        #print "the current date is within a day ago"
    else:
        return False
        #print "the current date is not within a day ago"



"""
will take in a datetime and return a boolean weather
that datetime was within the last hour
"""
def isWithin1(dateTime):
    
    #timeNow = time.strftime('%x %X %Z')
    #print "dateTime type = %s"%(type(dateTime))
    #print "dateTime = %s"%(dateTime)
    dateTimeU = dateTime[0]
    #print "dateTimeU = %s"%(dateTimeU)
    #print "dateTimeU type = %s"%(type(dateTimeU))

    stringdateSplit = dateTimeU.split()
    stringdate = stringdateSplit[0]+" "+stringdateSplit[1]

    stringdate2 = stringdateSplit[0].split("/")
    
    #gettting the exact month day and year from the string
    stringMonth = stringdate2[0]
    stringDay = stringdate2[1]
    stringYear = stringdate2[2]
    #print "month = %s day = %s year = %s"%(stringMonth,stringDay,stringYear)

    stringdateTime = stringdateSplit[1].split(":")
    stringHour = stringdateTime[0]
    stringMin = stringdateTime[1]
    stringSec = stringdateTime[2]
    #print "hour = %s min = %s second   = %s"%(stringHour,stringMin,stringSec)

    theDateTime = datetime.datetime(int(stringYear)+2000,int(stringMonth),int(stringDay),int(stringHour),int(stringMin),int(stringSec),0,None)
    #print "theDateTime = %s"%(theDateTime)
    #print "THE CURRENT DATE IS %s"%(datetime.datetime.now())
    aDayAgo = datetime.datetime.now() - timedelta(hours = 1)

    if(aDayAgo <= theDateTime <= datetime.datetime.now()):
        return True
        #print "the current date is within a day ago"
    else:
        return False
        #print "the current date is not within a day ago"



"""Will return the high and low temperatures of the past hour and day"""
def getTemps():


    dayTemps = []
    hourTemps = []
    
    
    con = mydb.connect('/home/pi/mydatabase.db')
    with con:
        try:
            cur = con.cursor()
            sql = "select * from temps"
            cur.execute(sql)
            output = cur.fetchall()
            for i in output:
                #print "i = %s"%(i)
                if(isWithin24(i)):
                    dayTemps.append(i[1]) 
                    #print "%s is within 24, temp was %s"%(i[0],i[1])
                if(isWithin1(i)):
                    hourTemps.append(i[1])
                    #print "%s is within 1, temp was %s"%(i[0],i[1])
            return dayTemps,hourTemps
    	except Exception as e:
            #e = sys.exc_info()[0]
            print e


"""Will search through both the temperatures reported in the past hour and the
temperatures reported in the past day and find and return the highs and lows of each """
def getHighsAndLows(dayTemps,hourTemps):
    highDay = dayTemps[0]
    lowDay = dayTemps[0]
    highHour = hourTemps[0]
    lowHour = hourTemps[0]
    
   
    
    for i in dayTemps:
        if (i > highDay):
            highDay = i
        if (i < lowDay):
            lowDay = i
            
    for j in hourTemps:
        if (j > highHour):
            highHour = j
        if (j < lowHour):
            lowHour = j

            
    return highDay,lowDay,highHour,lowHour
            

"""Will return the number of bubbles logged within the past hour"""
def countBubbles():
    dayCount = 0
    hourCount = 0
    
    con = mydb.connect('/home/pi/mydatabase.db')
    with con:
        try:
            cur = con.cursor()
            sql = "select * from bubbles"
            cur.execute(sql)
            output = cur.fetchall()
            for i in output:
                #print "i = %s"%(i)
                if(isWithin24(i)):
                    dayCount = dayCount + 1
                if(isWithin1(i)):
                    hourCount = hourCount + 1
            return dayCount,hourCount
    	except Exception as e:
            #e = sys.exc_info()[0]
            print e    



output = getTemps()
dayTempsOutput = output[0]
hourTempsOutput = output[1]

stats = getHighsAndLows(dayTempsOutput,hourTempsOutput)
#print "high day = %s lowDay = %s highHour = %s lowHour = %s"%(stats[0],stats[1],stats[2],stats[3])
result = countBubbles()
#print "the number of bubbles within the last day = %s the number of bubbles within the last hour = %s"%(result[0],result[1])

print "<style>"
print ".boxed{border: 1px solid}"
print "p{display:inline}"
print "</style>"
print "<h2>The Last 24 Hours:</h2>"
print "<h3>High:</h3>"
print "<p div class = \"boxed\"> %s <p>"%(stats[0])
print "<h3>Low:</h3>"
print "<p div class = \"boxed\"> %s <p>"%(stats[1])
print "<h3>The Number Of Bubbles Spotted :</h3>"
print "<p div class = \"boxed\">|      %s       |<p>"%(result[0])
print "<br><br><br><br>"
print "<h2>The Last Hour</h2>"
print "<h3>High:</h4>"
print "<p div class = \"boxed\"> %s <p>"%(stats[2])
print "<h3>Low:<h4>"
print "<p div class = \"boxed\">    %s    <p>"%(stats[3])
print "<h3>The Number Of Bubbles Spotted:</h4>"
print "<p div class = \"boxed\">|      %s       |<p>"%(result[1])
