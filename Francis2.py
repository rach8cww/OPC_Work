#################################################################################
# Python script for data logging output from a Alphasense OPC-N2 onto a Raspberry Pi 3
# Script written by Dr Robin Price (www.robinprice.net) and Dr Francis Pope (University of Birmingham)
# uses py-opc python library for operating the Alphasense OPC-N2 written by David H. Hagan (MIT),
# full documentation available at https://github.com/dhhagan/py-opc
# set to datalog with a 10 s time period with maximum duration of 1 year
##################################################################################
#!/usr/bin/python

# Importing libraries
import opc
import datetime
from time import sleep
from usbiss.spi import SPI

# Setting error message format for visibility
def exit_error(e, message):
    print('----------------------------------------------------------------------')
    print('\t', message)
    print(e)
    print('----------------------------------------------------------------------')
    exit(1)


def get_instrument(port):
    print('Trying to connect to instrument', port, '...')

    # Build the connector
    try:
        instrument = SPI("/dev/" + port)
    except Exception as e:
        exit_error('Could not connect to /dev/' + port)

    print('Connected to instrument!', instrument)

    return instrument


#alpha = opc.OPCN2()


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
        exit_error(e, 'Could not start alpha controller')


def device_status(alpha):
    print('Device status:')
    print(alpha.read_pot_status())


def device_status(alpha):
    print('Device status:')
    print(alpha.read_pot_status())


def perform(alpha):
    # Turn on the device
    alpha.on()
    device_status(alpha)

    sleep(2)

    alpha.toggle_fan(True)
    alpha.toggle_laser(True)

    power = 255
    alpha.set_fan_power(power)
    # alpha.set_laser_power(power)

    device_status(alpha)

    histogram = alpha.histogram()

    if histogram is None:
        raise Exception('Could not load histogram')



















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

