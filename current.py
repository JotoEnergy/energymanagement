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
def readChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
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



while True:

    verbraucherStorage = []
    batteryStorage = []
    solarStorage = []

    for i in xrange(1, 200):

        #Convert to Volts
        #verbraucherVolts = convertVolt(readChannel(0))
        #batteryVolts = convertVolt(readChannel(1))
        #solarVolts = convertVolt(readChannel(2))

        #Read Bitdata and linear function


        #Write to array and create average
        #verbraucherStorage.append(verbraucherVolts)
        #batteryStorage.append(batteryVolts)


        solarPanel = measurePower(2)
        solarStorage.append(solarPanel)
        time.sleep(0.05)

    #Average Array
    #averageVerbraucher = round(reduce(lambda x, y: x + y, verbraucherStorage) / len(verbraucherStorage),3)
   # averageBattery = round(reduce(lambda x, y: x + y, batteryStorage) / len(batteryStorage),3)
    averageSolar = round(reduce(lambda x, y: x + y, solarStorage) / len(solarStorage))

    # Print out results

#verbraucherLevel
#Batterie_level
#Solarpanel_level
    data = measurePower(2)
    currentOutput = (float(data[0]) - float(500)) / float(19)  * float(1000)
    print ("--------------------------------------------")
    #print("Verbraucher: ({}V)".format(averageVerbraucher))
    #print("Batterie   : ({}V)".format(averageBattery))
    print("Solarpanel : Bits {} | {}V | {}mA".format(data[0],round(data[1], 3), averageSolar))
    #print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

    #time.sleep(0.5)

    # Wait before repeating loop
