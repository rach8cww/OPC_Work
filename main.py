from usbiss.spi import SPI

spi = SPI(80)

spi.mode = 1
spi.max_speed_hz = 500000

print(repr(spi._usbiss))

# SPI transaction

response = spi.xfer([0x00, 0x00])