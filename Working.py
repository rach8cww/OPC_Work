#!/usr/bin/python

# Importing libraries
import json
import time
import rethinkdb as r
from time import sleep

from Watcher import WatchTable

# Importing libraries
import opc
from usbiss.spi import SPI

config = False
with open('database-config.json', 'r') as fin:
    config = json.loads(fin.read())

connection = r.connect(
    user=config["user"],
    host=config["host"],
    password=config["password"]
)

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


def get_bin_name(bin_name):
    bin_name = bin_name.lower()

    if " " in bin_name:
        return bin_name.replace(" ", "_")

    return bin_name


def get_type(bin_name):
    bin_name = get_bin_name(bin_name)

    if "bin_" in bin_name:
        return 'bin'

    if 'mtof' in bin_name:
        return 'mtof'

    return bin_name


def perform(alpha):

    print('----------------------------------------------------------------------')
    ts = time.gmtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
    histogram = alpha.histogram()

    if histogram is None:
        raise Exception('Could not load histogram')

    for key in histogram:
        r.db('data').table('telemetry').insert({
            "name": key,
            "type": get_type(key),
            "time": time.time(),
            "value": histogram[key]
        }).run(connection)


def shut_down(alpha):
    sleep(2)
    print('----------------------------------------------------------------------')
    ts = time.gmtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
    # Turn the device off
    alpha.off()

    print(alpha, '- Instrument finished getting data')

running = True

def main():
    spi = get_instrument('ttyACM0')
    alpha = get_alpha(spi)
    print('Alphasense instrument processing request')
    print('-----------------------------------------------------------------------')

    initiate(alpha)

    while True:
        if running is not True:
            break
        try:
            sleep(2)
            perform(alpha)

        except KeyboardInterrupt as e:
            print('Goodbye...')
            break

        except Exception as e:
            shut_down(alpha)
            exit_error(e, 'Failed while retrieving results, this is still not working...')

    shut_down(alpha)


def callback(change):
    print("OMG in my callback", change)

if __name__ == '__main__':
    print('Welcome to the OPC-N2 interfacing programme')
    # main()

    myWatcher = WatchTable("config", callback)

    while True:
        time.sleep(1)
        print("In my main thread")

# opcDriver = myOpcDriver('ttyACM0', max_speed_hertz=500000).run()