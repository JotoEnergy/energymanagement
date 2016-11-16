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
    adc = spi.xfer2([1, (8py + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def convertVolt (input1):

    return (input1 * 3.3) / float(1024)

#def newConvertVolt (input1, decimals):
def convertCurrent (data):

    return (data - 500) / 19


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



now = int(round(time.time()))

verbraucherStorage = []
batteryStorage = []
solarStorage = []

verbraucherWattStorage = []
batteryWattStorage = []
solarWattStorage = []

for i in xrange(1, 50):

    #Convert to Volts
    #verbraucherVolts = convertVolt(readChannel(0))
    #batteryVolts = convertVolt(readChannel(1))
    #solarVolts = convertVolt(readChannel(2))

    #Read Bitdata and linear function


    #Write to array and create average
    #verbraucherStorage.append(verbraucherVolts)
    #batteryStorage.append(batteryVolts)

    #Measure Power (Bits - Volt - Current) - input SPI Channel
    solarData = measurePower(2)
    #Get Bits and use linear algebra to find floating around 0
    solarOutput = (float(solarData[0]) - float(500)) / float(19)  * float(1000)
    #Set Offset
    solarOutput = setOffset(float(solarOutput), float(offset[0]))
    #miliAmpere * miliWatt (12500 hardcoded)
    solarWatt = convertPower(12500, solarOutput)

    #Measure Power (Bits - Volt - Current) - input SPI Channel
    batteryData = measurePower(1)
    batteryOutput = (float(batteryData[0]) - float(500)) / float(19)  * float(1000)
    batteryOutput =  setOffset(float(batteryOutput), float(offset[1]))
    batteryWatt = convertPower(12500, batteryOutput)

    #Measure Power (Bits - Volt - Current) - input SPI Channel
    verbraucherData = measurePower(0)
    verbraucherOutput = (float(verbraucherData[0]) - float(500)) / float(19)  * float(1000)
    verbraucherOutput = setOffset(float(verbraucherOutput), float(offset[2]))
    verbraucherWatt = convertPower(12500, verbraucherOutput)

    #Store in Array to create average of 100 calls
    solarStorage.append(solarOutput)
    batteryStorage.append(batteryOutput)
    verbraucherStorage.append(verbraucherOutput)

    verbraucherWattStorage.append(verbraucherWatt)
    batteryWattStorage.append(batteryWatt)
    solarWattStorage.append(solarWatt)
    time.sleep(0.1)

#Average Array
averageVerbraucher = round(reduce(lambda x, y: x + y, verbraucherStorage) / len(verbraucherStorage),3)
averageBattery = round(reduce(lambda x, y: x + y, batteryStorage) / len(batteryStorage),3)
averageSolar = reduce(lambda x, y: x + y, solarStorage) / len(solarStorage)

averageVerbraucherWatt = round(reduce(lambda x, y: x + y, verbraucherWattStorage) / len(verbraucherWattStorage),3)
averageBatteryWatt = round(reduce(lambda x, y: x + y, batteryWattStorage) / len(batteryWattStorage),3)
averageSolarWatt = reduce(lambda x, y: x + y, solarWattStorage) / len(solarWattStorage)

verbraucherPrice = (float(averageVerbraucherWatt) / float(1000)) * float(0.25)


# Print out results

#verbraucherLevel
#Batterie_level
#Solarpanel_level

#averageVerbraucherWatt = averageVerbraucherWatt * (-1)
print ("--------------------------------------------")
print("Verbraucher: Bits {} | {}V | {}mA | {}W | Preis {} Euro pro h".format(verbraucherData[0],round(verbraucherData[1], 3), round(averageVerbraucher), round(averageVerbraucherWatt), verbraucherPrice))
#print("Batterie   : Bits {} | {}V | {}mA".format(batteryData[0],round(batteryData[1], 3), averageBattery))
print("Solarpanel : Bits {} | {}V | {}mA | {}W".format(solarData[0],round(solarData[1], 3), round(averageSolar), round(averageSolarWatt)))
#print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

db = mysqlConnect()
cursor = db.cursor()
device = "Verbraucher"
try:
    # Execute the SQL command
    cursor.execute("INSERT INTO powerSensor (datum, power, volt, device) VALUES ('{}', '{}', '{}', '{}')".format(now, averageVerbraucherWatt, round(verbraucherData[1], 3), device) )
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

db.close()





