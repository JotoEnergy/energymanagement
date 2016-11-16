import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def readChannel(channel):
    adc = spi.xfer2([1, (8py + channel) << 4, 0])

    print("adc: ".format(adc)

    data = ((adc[1] & 3) << 8) + adc[2]
    return data

while True:
    readChannel(2)