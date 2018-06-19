#!/usr/bin/python

# Importing libraries
import opc
import time
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


def perform(alpha):
    # Turn on the device
    alpha.on()
    device_status(alpha)

    alpha.toggle_fan(True)
    alpha.toggle_laser(True)

    power = 255
    alpha.set_fan_power(power)
    # alpha.set_laser_power(power)

    device_status(alpha)

    histogram = alpha.histogram()

    if histogram is None:
        raise Exception('Could not load histogram')

    # Read the histogram and print to console
    for key, value in histogram.items():
        print("Key: {}\tValue: {}".format(key, value))

    time.sleep(2)

    # Turn the device off
    alpha.off()

    print(alpha)
    print('Finished processing data')


def main():
    spi = get_instrument('ttyACM0')
    alpha = get_alpha(spi)
    print('Alphasense instrument processing request')

    try:
        perform(alpha)

    except Exception as e:
        alpha.off()
        exit_error(e, 'Failed while retrieving results, this is still not working...')

"""
print('histogram_sum: ', opc.histogram_sum)
print('Checksum: ', opc.Checksum)
"""

if __name__ == '__main__':
    print('Welcome to Rachel\'s beautiful program')
    main()