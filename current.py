import spidev
import time
import os

pin_number = int(input('Type in the chip pin number you want to use: '))
# Define delay between readings
delay = int(input('Type delay between readings: '))

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

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data, places):
    #return .0264 * data - 13.51
    volts = (data * 3.3) / float(1023)
    volts = round(volts, places)
    return volts

while True:
    # Read the light sensor data
    current_level = ReadChannel(pin_number)
    current_volts = ConvertVolts(current_level, 2)

    # Read the temperature sensor data
    #temp_level = ReadChannel(temp_channel)
    #temp_volts = ConvertVolts(temp_level, 2)
    #temp = ConvertTemp(temp_level, 2)

    # Print out results
    print ("--------------------------------------------")
    print("Current Laptop: {} ({}V)".format(current_level, current_volts))
    #print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

    # Wait before repeating loop
    time.sleep(delay)
