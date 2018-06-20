import pymssql
conn = pymssql.connect(host='localhost', user='sa', password='p@ssw0rd', database='SampleDB')
cur = conn.cursor()
cur.execute('CREATE TABLE persons(id INT, name VARCHAR(100))')
cur.executemany("INSERT INTO persons VALUES(%d, %s)", \
    [ (1, 'John Doe'), (2, 'Jane Doe') ])
conn.commit()  # you must call commit() to persist your data if you don't set autocommit to True

cur.execute('SELECT * FROM persons WHERE name=%s', 'John Doe')
row = cur.fetchone()
while row:
    print( "ID=%d, Name=%s" % (row[0], row[1]))
    row = cur.fetchone()

# if you call execute() with one argument, you can use % sign as usual
# (it loses its special meaning).
cur.execute("SELECT * FROM persons WHERE name LIKE 'J%'")

conn.close()

