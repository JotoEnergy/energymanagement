#!/usr/bin/python
import MySQLdb
import datetime

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="joto123",  # your password
                     db="raspi")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cursor = db.cursor()

now = datetime.datetime.now()
# Use all the SQL you like
cursor.execute("INSERT INTO powerSensor (datum, power, volt, device) VALUES (%s, %s, %s, %s)", (now, 10, 1.5, 'Verbraucher'))


try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

db.close()