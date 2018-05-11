from usbiss.spi import SPI
import opc


def getInstrument(port):
    print('Trying to connect to instrument', port, '...')

    # Build the connector
    instrument = SPI("/dev/" + port)

    print('Connected to instrument!', instrument)

    return instrument


def main():
    spi = getInstrument('ttyACM0')

    # Set the SPI mode and clock speed
    spi.mode = 1
    spi.max_speed_hz = 500000

    alpha = opc.OPCN2(spi)

    # Turn on the device
    alpha.on()

    # Read the histogram
    histogram = alpha.histogram()

    # Turn the device off
    alpha.off()

    print(alpha)
    print(histogram)
    print('Finished processing data')

if __name__  == '__main__':
    main()