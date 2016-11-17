#!/usr/bin/python
import spidev
import time
import os
import MySQLdb
import numpy

def mysqlConnect ():

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="joto123",  # your password
                         db="raspi")        # name of the data base
    return db

#cursor = db.cursor()


#pin_number = int(input('Type in the chip pin number you want to use: '))
# Define delay between readings
delay = 1 #int(input('Type delay between readings: '))

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Offset 1) Solar 2) Battery 3) Verbraucher
offset = [300, 0, 550]

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def readChannel(channel):
    #adc = spi.xfer2([1, (8 + channel) << 4, 0])
    #data = ((adc[1] & 3) << 8) + adc[2]
    #return data
    adc = spi.xfer2([6+((4&channel)>>2),(3&channel)<<6,0])
    data = ((adc[1]&15) << 8) + adc[2]
    return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def convertVolt (input1):

    voltage = (input1 * 3.3) / float(4096)
    linearVoltage = voltage * 7.08
    return linearVoltage

def convertCurrent (data):

    return float((data - 2048) / 19)


#Give SPI Channel and receive Array: [0] - Bits [1] - Volt, [2] - Current
def measurePower (channel):
    bitData = readChannel(channel)
    volt = convertVolt(bitData)
    current = convertCurrent(bitData)

    return [bitData, volt, current]

def setOffset (data, offsetHeight):
    if(data > 0):
        return data - offsetHeight
    else:
        return data + offsetHeight


def convertPower(volt, ampere):
    return (float(volt)*float(ampere) / 1000) / 1000


def getOffsets():
    offsetArr = []
    db = mysqlConnect()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()

    for row in rows:
        offsetArr.append(row["bitOffset"])

    db.close()
    return offsetArr


devices = 4
device = 0
channel = 0

allOffsets = getOffsets()

for i in xrange(0, devices):

    #Take first channel for Ampere
    currentArr = []
    #Get current Offset
    currentOffset = allOffsets[i]
    for a in xrange(0,50):
        bitData = readChannel(channel) + currentOffset
        current = convertCurrent(bitData)
        currentArr.append(current)
        time.sleep(0.01)

    currentBitData = bitData
    currentAverage = round(reduce(lambda x, y: x + y, currentArr) / len(currentArr), 5)

    #Increase channel
    channel+=1
    #Take second Channel for Voltage
    voltageArr = []
    for b in xrange(0,50):
        bitData = readChannel(channel)
        voltage = convertVolt(bitData)
        voltageArr.append(voltage)
        time.sleep(0.01)

    voltBitData = bitData

    voltageAverage = round(reduce(lambda x, y: x + y, voltageArr) / len(voltageArr), 5)
    power = currentAverage
    volt = voltageAverage

    watt = convertPower(volt, power)

    db = mysqlConnect()
    cursor = db.cursor()
    device+=1

    print('Device {}, BitRate: {} - Power {} - Volt {} - Watt {}'.format(device, currentBitData, power, volt, watt))
    now = int(round(time.time()))
    try:
    # Execute the SQL command
        cursor.execute("INSERT INTO powerSensor (datum, power, volt, watt, device) VALUES ('{}', '{}', '{}', '{}', '{}')".format(now, float(power), float(volt), float(watt), device) )
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()

    db.close()
    channel+=1




#Average Array

#averageSolar = reduce(lambda x, y: x + y, solarStorage) / len(solarStorage)

#averageVerbraucherWatt = round(reduce(lambda x, y: x + y, verbraucherWattStorage) / len(verbraucherWattStorage),3)
#averageBatteryWatt = round(reduce(lambda x, y: x + y, batteryWattStorage) / len(batteryWattStorage),3)
#averageSolarWatt = reduce(lambda x, y: x + y, solarWattStorage) / len(solarWattStorage)

#verbraucherPrice = (float(averageVerbraucherWatt) / float(1000)) * float(0.25)


#print('\n'.join([''.join(['{:4}'.format(item) for item in row])
#                 for row in portStorage]))
# Print out results

#verbraucherLevel
#Batterie_level
#Solarpanel_level

#averageVerbraucherWatt = averageVerbraucherWatt * (-1)
#print ("--------------------------------------------")
#print("Verbraucher: Bits {} | {}V | {}mA | {}W | Preis {} Euro pro h".format(verbraucherData[0],round(verbraucherData[1], 2), round(averageVerbraucher), round(averageVerbraucherWatt), verbraucherPrice))
#print("Batterie   : Bits {} | {}V | {}mA".format(batteryData[0],round(batteryData[1], 3), averageBattery))
#print("Solarpanel : Bits {} | {}V | {}mA | {}W".format(solarData[0],round(solarData[1], 2), round(averageSolar), round(averageSolarWatt)))
#print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

#db = mysqlConnect()
#cursor = db.cursor()
#device = "Verbraucher"
#try:
    # Execute the SQL command
    #cursor.execute("INSERT INTO powerSensor (datum, power, volt, device) VALUES ('{}', '{}', '{}', '{}')".format(now, averageVerbraucherWatt, round(verbraucherData[1], 3), device) )
    # Commit your changes in the database
    #db.commit()
#except:
    # Rollback in case there is any error
    #db.rollback()

#db.close()





