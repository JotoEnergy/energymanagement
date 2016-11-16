#!/usr/bin/python
import MySQLdb
import time

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="joto123",  # your password
                     db="raspi")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
curs = db.cursor()


curs.execute ("SELECT * FROM devices")

print "\nDate     	Time		Zone		Temperature"
print "==========================================================="

for reading in curs.fetchall():
    print str(reading[0])+"	"+str(reading[1])+" 	"+ \
          reading[2]+"  	"+str(reading[3])