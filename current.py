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

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data, places):
    #return .0264 * data - 13.51
    volts = (data * 3.3) / float(1023)
    volts = round(volts, places)
    return volts

def ConvertVoltsBat(Bat, places):
    #return .0264 * data - 13.51
    voltsBat = (Bat * 3.3) / float(1023)
    voltsBat = round(voltsBat, places)
    return voltsBat

def ConvertVoltsSolar(Solar, places):
    #return .0264 * data - 13.51
    voltsSolar = (Solar * 3.3) / float(1023)
    voltsSolar = round(voltsSolar, places)
    return voltsSolar

def convertVolt (input1, decimals):
    return round((input1 * 3.3) / float(1023), decimals)

while True:
    # Read the light sensor data
    Verbraucher_level = ReadChannel(0)
    Verbraucher_volts = convertVolt(Verbraucher_level, 3)
    
    Batterie_level = ReadChannelBat(1)
    Batterie_volts = convertVolt(Batterie_level, 3)

    Solarpanel_level = ReadChannelSolar(2)
    Solarpanel_volts = convertVolt(Solarpanel_level, 3)
    # Read the temperature sensor data
    #temp_level = ReadChannel(temp_channel)
    #temp_volts = ConvertVolts(temp_level, 2)
    #temp = ConvertTemp(temp_level, 2)

    # Print out results
    print ("--------------------------------------------")
    print("Verbraucher: {} ({}V)".format(Verbraucher_level, Verbraucher_volts))
    print("Batterie   : {} ({}V)".format(Batterie_level, Batterie_volts))
    print("Solarpanel : {} ({}V)".format(Solarpanel_level, Solarpanel_volts))
    #print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

    # Wait before repeating loop
    time.sleep(delay)
