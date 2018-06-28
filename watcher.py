import rethinkdb as r


connection = r.connect(
    user='admin',
    host='18.218.150.250',
    password='0mu_ptElrvCf7ykSMyID_fuMricNSHA&&t^wKlXf1OeJUh4!'
)

def changes(change):
    print(change)

cursor = r\
    .db('data')\
    .table('drone_test_1')\
    .changes()

for change in cursor.run(connection):
    changes(change)
