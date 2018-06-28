#!/usr/bin/python

# Importing libraries
import opc
import time
from time import sleep
from usbiss.spi import SPI
#import openpyxl
import csv
# import openpyxl
import pandas as pd
import csv
import time
from time import sleep

# Importing libraries
import opc
from usbiss.spi import SPI


# Setting error message format for visibility
def exit_error(e, message):
    print('----------------------------------------------------------------------')
    print('\t', message)
    print(e)
    print('----------------------------------------------------------------------')
    exit(1)


# code to connect to the instrument
def get_instrument(port):
    print('Trying to connect to instrument', port, '...')

    # Build the connector
    try:
        instrument = SPI("/dev/" + port)
    except Exception as e:
        exit_error('Could not connect to /dev/' + port)

    print('Connected to instrument!', instrument)

    return instrument


#
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

def initiate(alpha):
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


def perform(alpha):

    print('----------------------------------------------------------------------')
    ts = time.gmtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
    histogram = alpha.histogram()

    if histogram is None:
        raise Exception('Could not load histogram')

    histogram['Bin 00'] = histogram.pop('Bin 0')
    histogram['Bin 01'] = histogram.pop('Bin 1')
    histogram['Bin 02'] = histogram.pop('Bin 2')
    histogram['Bin 03'] = histogram.pop('Bin 3')
    histogram['Bin 04'] = histogram.pop('Bin 4')
    histogram['Bin 05'] = histogram.pop('Bin 5')
    histogram['Bin 06'] = histogram.pop('Bin 6')
    histogram['Bin 07'] = histogram.pop('Bin 7')
    histogram['Bin 08'] = histogram.pop('Bin 8')
    histogram['Bin 09'] = histogram.pop('Bin 9')

    for key in sorted(histogram):
        print("%s: %s" % (key, histogram[key]))


    """   
    #'C:\\Users\\Rachel Whitty\\Desktop\\WORK\\raspberryOPC\\Data\\Trial.csv'
    with open('Trial.csv', 'w') as out:
        print('Initiating the print to file protocol')
        fieldnames = ['Bin_1', 'Bin_2']
        write = csv.DictWriter(out, fieldnames=fieldnames)

        write.writeheader()
        write.writerow({'Bin_1': 'Lots of Aerosols', 'Bin_2': 'Not so many aerosols'})
    """


def shut_down(alpha):
    sleep(2)
    print('----------------------------------------------------------------------')
    ts = time.gmtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
    # Turn the device off
    alpha.off()

    print(alpha, '- Instrument finished getting data')


"""
def write_file(alpha):
    file = open('trial_1.csv', 'w')
    histogram = alpha.histogram()
    file.write(histogram.keys())
    file.write(histogram.values())


def write_file(alpha):
    with open('C:\\Users\\Rachel Whitty\\Desktop\\WORK\\raspberryOPC\\Data\\trial_1.csv', 'w') as out:
        histogram = alpha.histogram()
        w = csv.DictWriter(out, histogram)
        w.writeheader()
        w.writerow(histogram)
"""
"""
def write_file(alpha):
    with open('TestOutput.csv', 'w') as csvfile:
        #fieldnames = ['Bin 00', 'Bin 01', 'Bin 02', 'Bin 03', 'Bin 04', 'Bin 05', 'Bin 06' /
                     # 'Bin 07', 'Bin 08', 'Bin 09', 'Bin 10', 'Bin 11', 'Bin 12', 'Bin 13' /
                     # 'Bin 14', 'Bin 15', 'Bin1 MToF', 'Bin3 MToF', 'Bin4 MToF', 'Bin7 MToF' /
                     # 'Checksum', 'PM1', 'PM10', 'PM2.5', 'Pressure', 'SFR', 'Sampling Period' /
                     # 'Temperature']
        writer = csv.writer(csvfile)
"""

def main():
    spi = get_instrument('ttyACM0')
    alpha = get_alpha(spi)
    print('Alphasense instrument processing request')
    print('-----------------------------------------------------------------------')

    initiate(alpha)

    cc = 0

    for cc in range(0,1): # change to (0,1) for 10 iterations
        sleep(2)
        cc = cc + 1
        try:
            perform(alpha)

        except Exception as e:
            alpha.off()
            exit_error(e, 'Failed while retrieving results, this is still not working...')

        histogram = alpha.histogram()
        try:
            df = pd.DataFrame.from_dict(histogram, orient='index')
            df.to_csv('data.csv')
        except Exception as e:
            alpha.off()
            exit_error(e, 'Failed to save to csv')


    shut_down(alpha)



if __name__ == '__main__':
    print('Welcome to the OPC-N2 interfacing programme')
    main()


"""
with open('C:\\Users\\Cecilia\\Desktop\\Trial.csv', 'w', newline='') as out:
print('Initiating the print to file protocol')
fieldnames = ['Bin_1', 'Bin_2']
write = csv.DictWriter(out, fieldnames=fieldnames)

write.writeheader()
write.writerow({'Bin_1': 'Lots of Aerosols', 'Bin_2': 'Not so many aerosols'})
"""