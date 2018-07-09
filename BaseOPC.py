#!/usr/bin/python

# Importing libraries
import time
import glob
import serial

from time import sleep

from RethinkDB import RethinkDBConnection

# Importing libraries
import opc
from usbiss.spi import SPI

## class Life
## def breathe(self) : All life breathes

## class Animal(Life) ## Extends life
## def breathe(self) : by default it will call Life.breathe
## def breathe(self): breathe underwater
## class Dog(Animal)

## class Plant(Life) ## Extends life
## class Tree(Plant)

# Setting error message format for visibility
def exit_error(e, message):
	"""Format the exit error for ease of readability"""
	print('----------------------------------------------------------------------')
	print('\t', message)
	print(e)
	print('----------------------------------------------------------------------')
	exit(1)
	
def find_ports():
    """Finding the ports the pi has available"""
	ports = glob.glob('/dev/ttyACM[0-9]*')

    res = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            res.append(port)
        except:
            pass
    return res
	

# code to connect to the instrument
def get_instrument(port):
	"""Connect to the instrument"""
	print('Trying to connect to instrument', port, '...')
	
	open_ports = find_ports()
	
	portName = '/dev/' + port
	if not any(portName in s for s in open_ports):
		print('Found devices on ports: ' + ','.join(open_ports))
		exit_error('CONNECTION_ERROR', 'Could not find device ' + portName)
		
	print('Found device @ ' + portName)
	# Build the connector 
	try:                  
		instrument = SPI(portName)

		print('Connected to instrument!', instrument)

		return instrument
	except Exception as e:
		exit_error('CONNECTION_ERROR', 'Could not connect to ' + portName)


def get_alpha(spi):
	"""Set the SPI mode and clock speed"""
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
	"""Prints the device status, fan and laser stats"""
	print('Device status:')
	print(alpha.read_pot_status())


class BaseOPC:

	def __init__(self, **kwargs):
		"""Sets up the BaseOPC class"""
		self.should_gather_data = kwargs.get('should_gather_data', lambda x: True)
		self.port = kwargs.get("port", "ttyACM0")
		self.config = kwargs.get("instrumentConfig", None)

	def runOPC(self):
		"""runOPC function to run the main section of code (gets instrument to run)"""
		self.main()

	def initiate(self):
		"""Turn on the device"""
		self.alpha.on()
		device_status(self.alpha)

		sleep(2) # time to warm up 

		self.alpha.toggle_fan(True)
		self.alpha.toggle_laser(True)

		power = 255
		self.alpha.set_fan_power(power)
		# alpha.set_laser_power(power)

		device_status(self.alpha)

	def get_bin_name(self, bin_name):
		"""Sets type name underscore rather than spaces"""
		bin_name = bin_name.lower()

		if " " in bin_name:
			return bin_name.replace(" ", "_")

		return bin_name

	
	def get_type(self, bin_name):
		""""Sometimes the bin_name has capital letters 
		Here we'll remove those spaces, and normalize the names"""
		bin_name = self.get_bin_name(bin_name)

		if "bin_" in bin_name:
			return 'bin'

		if 'mtof' in bin_name:
			return 'mtof'

		return bin_name

		
	def perform(self):
		"""prints the timestamp to the console, collects the histogram data
		saves the histogram to key (type name) and data (measurements)"""
		print('----------------------------------------------------------------------')
		ts = time.gmtime()
		print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
		histogram = self.alpha.histogram()

		if histogram is None:
			raise Exception('Could not load histogram')

		for key in histogram:
			self.save_data(key, histogram[key])

	def save_data(self, key, data):
		"""Called in the Working.py"""
		print("Got data to save", key, data)

	def shut_down(self):
		"""Prints the time and turns off the fan"""
		sleep(2)
		print('----------------------------------------------------------------------')
		print('Shutting device down')
		ts = time.gmtime()
		print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
		# Turn the device off
		self.alpha.off()

		print(self.alpha, '- Instrument finished getting data')
		exit(0)

	def should_gather_data(self):
		"""If the server has not sent the config yet"""
		return False
		
	def main(self):
		"""Main code to run the OPC, called as runOPC function (above)"""
		spi = get_instrument(self.port)
		self.alpha = get_alpha(spi)
		print('Alphasense instrument processing request')
		print('-----------------------------------------------------------------------')

		self.initiate()

		while True:
			try:
				sleep(2)
				
				# self.should_gather_data should return true if the config suggests
				# we should not gather data at this time.
				if not self.should_gather_data():
					print("Waiting for config OK to collect")
					continue;
				
				print('perform')
				self.perform()

			except KeyboardInterrupt as e:
				"""Keyboard interrupt and pause, then will initiate shut_down"""
				print('Goodbye...')
				break

			except Exception as e:
				self.shut_down()
				exit_error(e, 'Failed while retrieving results, this is still not working...')

		self.shut_down()


def get_opc():

	opcDriver = WorkOPC(config="database-config.json").runOPC()

if __name__ == '__main__':
	print('Welcome to the OPC-N2 interfacing programme')