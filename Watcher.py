import json
import threading
import rethinkdb as r

from RethinkDB import RethinkDBConnection

class WatchTable(RethinkDBConnection):

    def __init__(self, tablename, callback, **kwargs):
        super(WatchTable, self).__init__(**kwargs)
        self.setupCursor(tablename, callback)
        self.thread = self.create_thread()

    def setupCursor(self, tablename, callback):
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
        for change in self.runQuery(self.cursor):
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