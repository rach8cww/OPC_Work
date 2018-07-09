#################################################################################
# Python script for data logging output from a Alphasense OPC-N2 onto a Raspberry Pi 3
# Script written by Dr Robin Price (www.robinprice.net) and Dr Francis Pope (University of Birmingham)
# uses py-opc python library for operating the Alphasense OPC-N2 written by David H. Hagan (MIT),
# full documentation available at https://github.com/dhhagan/py-opc
# set to datalog with a 10 s time period with maximum duration of 1 year
##################################################################################

# !/usr/bin/env python
import opc
from usbiss.spi import SPI as spi
from time import sleep
from datetime import datetime

alpha = opc.OPCN2


def get_alpha(spi):
    # Set the SPI mode and clock speed
    spi.mode = 1
    spi.max_speed_hz = 500000

    try:
        alpha = opc.OPCN2(spi, debug=True)

        if alpha is None:
            raise Exception('Could not connect!')

        print('Connected to', alpha)
        return alpha

    except Exception as e:
        print('Could not start alpha controller'.format(e))


#
alpha.off()

sleep(2)

alpha.on()

sleep(2)

print(alpha.config2())
for i in range(60*60*24*365):
    robin = alpha.histogram()
    print(robin)
    francis = open('filename', 'a')
    francis.write(str(datetime.utcnow()) + ", ")
    francis.write(str(robin['PM1']) + ", ")
    francis.write(str(robin['PM2.5']) + ", ")
    francis.write(str(robin['PM10']) + ", ")
    francis.write(str(robin['Bin 0']) + ", ")
    francis.write(str(robin['Bin 1']) + ", ")
    francis.write(str(robin['Bin 2']) + ", ")
    francis.write(str(robin['Bin 3']) + ", ")
    francis.write(str(robin['Bin 4']) + ", ")
    francis.write(str(robin['Bin 5']) + ", ")
    francis.write(str(robin['Bin 6']) + ", ")
    francis.write(str(robin['Bin 7']) + ", ")
    francis.write(str(robin['Bin 8']) + ", ")
    francis.write(str(robin['Bin 9']) + ", ")
    francis.write(str(robin['Bin 10']) + ", ")
    francis.write(str(robin['Bin 11']) + ", ")
    francis.write(str(robin['Bin 12']) + ", ")
    francis.write(str(robin['Bin 13']) + ", ")
    francis.write(str(robin['Bin 14']) + ", ")
    francis.write(str(robin['Bin 15']) + ", ")
    francis.write(str(robin['Sampling Period']) + "\n")
    francis.close()
    sleep(10)

alpha.off()

