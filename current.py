import spidev
import time
import os

#pin_number = int(input('Type in the chip pin number you want to use: '))
# Define delay between readings
delay = 1 #int(input('Type delay between readings: '))

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    if channel > 7 or channel < 0:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def ReadChannelBat(channel):
    if channel > 7 or channel < 0:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    Bat = ((adc[1] & 3) << 8) + adc[2]
    return Bat

def ReadChannelSolar(channel):
    if channel > 7 or channel < 0:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    Solar = ((adc[1] & 3) << 8) + adc[2]
    return Solar

def readChannel(channel):
    #Channel must be between 1, 6
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.

def convertVolt (input1, decimals):

    return round((input1 * 3.3) / float(1024), decimals)

#def newConvertVolt (input1, decimals):

while True:

    verbraucherStorage = []
    batteryStorage = []
    solarStorage = []

    for i in xrange(1, 10):
        # Read the light sensor data
        #Convert to Volts
        verbraucherVolts = convertVolt(readChannel(0), 3)
        batteryVolts = convertVolt(readChannel(1), 3)
        solarVolts = convertVolt(readChannel(2), 3)

        #Write to array and create average
        verbraucherStorage.append(verbraucherVolts)
        batteryStorage.append(batteryVolts)
        solarStorage.append(solarVolts)
        time.sleep(0.1)

    averageVerbraucher = round(reduce(lambda x, y: x + y, verbraucherStorage) / len(verbraucherStorage),3)
    averageBattery = round(reduce(lambda x, y: x + y, batteryStorage) / len(batteryStorage),3)
    averageSolar = round(reduce(lambda x, y: x + y, solarStorage) / len(solarStorage),3)

    # Print out results

#verbraucherLevel
#Batterie_level
#Solarpanel_level
    print ("--------------------------------------------")
    print("Verbraucher: {} ({}V)".format( averageVerbraucher))
    print("Batterie   : {} ({}V)".format(averageBattery))
    print("Solarpanel : {} ({}V)".format(averageSolar))
    #print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

    # Wait before repeating loop
