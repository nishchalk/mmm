import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="dundundun",  # your password
                     db="mysql")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM book")

# print all the first cell of all the rows
resut = cur.fetchall()
print type(resut)

db.close()