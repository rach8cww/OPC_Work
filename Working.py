#!/usr/bin/python

# Importing libraries
import csv
import time
import rethinkdb as r

from ConfigOPC import ConfigOPC
from RethinkDB import RethinkDBConnection

def open_csv_file_append_mode(file_name, headers):
	with open(file_name, 'w') as fout:
		writer = csv.DictWriter(fout, fieldnames=headers)
		writer.writeheader()
		
	append_file = open(file_name, "a")
	return csv.DictWriter(append_file, fieldnames=headers)
	
def csv_name(time_obj):
	return time.strftime("data/%a_%d_%b_%Y_%H:%M:%S", time_obj)
	
def open_csv_file_append_mode_time(headers):
	return open_csv_file_append_mode(csv_name(), headers)
	
GROUP_NAMES = ["name", "sampleName", "type", "time", "value"]

class WorkOPC(ConfigOPC):

	def __init__(self, **kwargs):
		super(WorkOPC, self).__init__(**kwargs)
		
		## Create a local connection to rethinkdb that we can use to insert data
		self.rethink = RethinkDBConnection(**kwargs)
		
		fileName = kwargs.get('local_file', 'data.json')
		self.time = time.gmtime()
		self.fileName = csv_name(self.time)
		
	def runOPC(self):
		print("Running WorkOPC:runOPC")
		super(WorkOPC, self).runOPC()

	def update_is_running(self):
		"""Let the server know that we're connected (via drone) every so often"""
		self.rethink.runQuery(
			r.db('config').insert({
				"time": time.time(),
				"droneRunning": True,
				"id": 'drone-running'
			})
		)

	def send_error_to_remote(self, error):
		try:
			self.rethink.runQuery(
				r.db('telemetry').table('errors').insert({
					"error": error,
					"shouldAlert": True
				})
			)
		except Exception as e:
			print("Error while sending error to remote:", e)

	def save_to_remote(self, key, data):
		"""Save data to remote host"""
		try:
			currentSample = self.config["sampleName"]["value"]

			self.rethink.runQuery(
				r.db('telemetry').table('data').insert({
					"name": key,
					"sampleName": currentSample,
					"type": self.get_type(key),
					"time": time.time(),
					"value": data
				})
			)
		except Exception as e:
			print("Error while saving to remote:", e)

	def save_to_local(self, key, data):
		# save data to local sim card in case of connection loss
		# https://stackoverflow.com/questions/4706499/how-do-you-append-to-a-file
		# self.file.write (because we don't want to open the file each time, it's slow)
		try:
			currentSample = self.config["sampleName"]["value"]
			with open(csv_name(self.time), 'a') as fout:
				writer = csv.DictWriter(fout, fieldnames=GROUP_NAMES)

				writer.writerow({
					"name": key,
					"sampleName": currentSample,
					"type": self.get_type(key),
					"time": time.time(),
					"value": data
				})
			
		except Exception as e:
			print("Error while saving to local:", e)

	def save_data(self, key, data):
		self.save_to_local(key, data)
		self.save_to_remote(key, data)

if __name__ == '__main__':
	print('Welcome to the OPC-N2 interfacing programme')
	## ttyAMA0
	## ttyAMC1
	## ttyACM0
	opcDriver = WorkOPC(port="ttyACM0", config="database-config.json").runOPC()
