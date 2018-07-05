import json
import rethinkdb as r

config = False
with open('database-config.json', 'r') as fin:
    config = json.loads(fin.read())

connection = r.connect(
    user=config["user"],
    host=config["host"],
    password=config["password"]
)

def changes(change):
    print(change)

cursor = r\
    .db('telemetry')\
    .table('config')\
    .changes()

for change in cursor.run(connection):
    changes(change)
