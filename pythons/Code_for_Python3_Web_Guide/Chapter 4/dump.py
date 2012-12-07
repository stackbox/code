import tasklistdb

tasklistdb.connect('/tmp/oink2.db')

print("\n".join(list(tasklistdb.data.conn.iterdump())))
