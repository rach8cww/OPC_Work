import opc
import time
from usbiss.spi import SPI


def get_instrument(port):
    print('Trying to connect to instrument', port, '...')

    # Build the connector
    try:
        instrument = SPI("/dev/" + port)
    except Exception as e:
        print('Could not connect to /dev/' + port)
        print(e)
        exit(1)

    print('Connected to instrument!', instrument)

    return instrument


def get_alpha(spi):
    # Set the SPI mode and clock speed
    spi.mode = 1
    spi.max_speed_hz = 500000

    try:
        alpha = opc.OPCN2(spi)
        if alpha is None:
            raise Exception('Could not connect!')

        return alpha

    except Exception as e:
        print('Could not start alpha controller')
        print(e)
        exit(1)


def results(alpha):
    # Read the histogram and print to console
    for key, value in alpha.histogram().items():
        print("Key: {}\tValue: {}".format(key, value))

    # Turn the device off
    alpha.off()

    print(alpha)
    print('Finished processing data')

def main():
    spi = get_instrument('ttyACM0')
    alpha = get_alpha(spi)

    try:
        # Turn on the device
        alpha.on()
        results(alpha)

    except Exception as e:
        print('Failed while retreiving results')
        print(e)
        alpha.off()
        exit(1)

if __name__ == '__main__':
    print('Welcome to Rachel\'s beautiful program')
    main()