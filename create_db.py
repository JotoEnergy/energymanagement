#!/usr/bin/python
import MySQLdb
import time

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="joto123",  # your password
                     db="raspi")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cursor = db.cursor()

try:
    # Execute the SQL command
    cursor.execute("CREATE TABLE devices( ID int(5), deviceName varchar(255), bitOffset varchar(10), channel varchar(3), sensorType varchar(3) );")
    result = cursor.fetchall()
    print result[0]
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

db.close()