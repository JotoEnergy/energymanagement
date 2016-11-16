#!/usr/bin/python
import spidev
import time
import os
import MySQLdb

def mysqlConnect ():

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="joto123",  # your password
                         db="raspi")        # name of the data base
    return db

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def readChannel(channel):
    #adc = spi.xfer2([1, (8 + channel) << 4, 0])
    #data = ((adc[1] & 3) << 8) + adc[2]
    #return data
    adc = spi.xfer2([6+((4&channel)>>2),(3&channel)<<6,0])
    data = ((adc[1]&15) << 8) + adc[2]
    return data


while True:
    typeStorage = []
    for i in xrange(0, 7):
        data = readChannel(i)
        typeStorage.append(data)
    print str(typeStorage)[1:-1]

    time.sleep(1)