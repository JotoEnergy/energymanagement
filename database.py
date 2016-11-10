#!/usr/bin/python
import MySQLdb
import datetime

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="joto123",  # your password
                     db="raspi")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

now = datetime.datetime.now()
# Use all the SQL you like
cur.execute("INSERT INTO powerSensor (datum, power, volt, device) VALUES (%s, %s, %s, %s, %s)", (now, 10, 1.5, 'Verbraucher'))

# print all the first cell of all the rows


db.close()