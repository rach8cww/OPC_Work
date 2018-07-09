import json
import threading
import rethinkdb as r

from RethinkDB import RethinkDBConnection

class WatchTable(RethinkDBConnection):

	def __init__(self, tablename, callback, **kwargs):
		"""Setting up the WatchTable class"""
		super(WatchTable, self).__init__(**kwargs)
		self.setupCursor(tablename, callback)
		self.thread = self.create_thread()

	def setupCursor(self, tablename, callback):
		"""Sets up the telemetry remote file"""
		self.tablename = tablename
		self.callback = callback
		self.cursor = r \
			.db('telemetry') \
			.table(tablename) \
			.changes(include_initial=True)

	def create_thread(self):
		"""Initiate the threading process"""
		myThread = threading.Thread(None, self.changes_thread)
		myThread.start()
		return myThread

	def changes_thread(self):
		"""One thread to watch for changes from the remote server"""
		for change in self.runQuery(self.cursor):
			self.changes(change)
	
	def changes(self, change):
		"""Prints change found and then prints the particulars of the change"""
		print("Got change", json.dumps(change, indent=4, sort_keys=True))
		
		print(self.callback)
		if callable(self.callback):
			self.callback(change)

# instrument -> raspberry -> database
# browser -> webserver -> database

# Single threaded
# Watcher.py -> single threaded application

# Multi threaded
# Watcher.py -> First thread
# Working.py -> Second thread


# |
# |
# |\
# | |
# | |\
# | | | config = {}
# | | |
# | | |
# |
# |
# |
# |