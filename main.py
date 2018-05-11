from usbiss.spi import SPI
import opc

print('Trying to connect to instrument...')

# Build the connector
spi = SPI("/dev/ttyAMA0")

print('Connected to instrument!')

# Set the SPI mode and clock speed
spi.mode = 1
spi.max_speed_hz = 500000

alpha = opc.OPCN2(spi)

# Turn on the device
alpha.on()

# Read the histogram
alpha.histogram()

# Turn the device off
alpha.off()