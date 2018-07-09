import json
import time

from BaseOPC import BaseOPC
from Watcher import WatchTable

class ConfigOPC(BaseOPC):

	def __init__(self, **kwargs):
		"""Setting up the CongifOPC class"""
		super(ConfigOPC, self).__init__(**kwargs)
		
		self.config = self.load_default_config() # load config from file
		
		## Runs a separate thread to watch for configuration changes
		self.configWatcher = WatchTable(
			"config",
			self.config_callback,
			config="database-config.json"
		)
		
	def should_gather_data(self):
		"""If the remote "collect data" button is checked then will gather data"""
		print(self.config)
		return self.config['active']['checked'] is True
				
	def load_default_config(self):
		"""Load the default config settings (so don't have to get config from remote"""
		with open('defaultConfig.json', 'r') as fin:
			return json.loads(fin.read())
	
	def config_callback(self, change):
		"""Prints the new config which was received in the change"""
		print('Received new configuration for drone')
		new_config = change["new_val"]
		
		print(new_config)
		if new_config['id'] is 'drone-configuration':
		
			self.config = new_config['config']