import json
import threading
import rethinkdb as r

config = False
with open('database-config.json', 'r') as fin:
    config = json.loads(fin.read())


class WatchTable:

    def __init__(self, tablename, callback):
        self.create_connection_to_database()
        self.setup(tablename, callback)
        self.thread = self.create_thread()

    def create_connection_to_database(self):
        self.__connection = r.connect(
            user=config["user"],
            host=config["host"],
            password=config["password"]
        )
        print("Connected to database")

    def setup(self, tablename, callback):
        self.tablename = tablename
        self.callback = callback
        self.cursor = r \
            .db('telemetry') \
            .table(tablename) \
            .changes()

    def create_thread(self):
        myThread = threading.Thread(None, self.changes_thread)
        myThread.start()
        return myThread

    def changes_thread(self):
        for change in self.cursor.run(self.__connection):
            self.callback(change)
            self.changes(change)

    def changes(self, change):
        print("Got change", json.dumps(change, indent=4, sort_keys=True))


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