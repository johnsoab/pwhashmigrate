import sqlite3
import hashlib
import bcrypt

conn = sqlite3.connect('example.db')
c = conn.cursor()


# Create table
c.execute('''CREATE TABLE AppUsers
             (username text, password text)''')

# Insert a row of data.. a hex encoded sha1 of "password" to start is good, maybe some others for good measure
c.execute("INSERT INTO AppUsers VALUES ('usera','" + hashlib.sha1(b'password').hexdigest() + "')")
c.execute("INSERT INTO AppUsers VALUES ('userb','" + hashlib.sha1(b'password123').hexdigest() + "')")
c.execute("INSERT INTO AppUsers VALUES ('userc','" + hashlib.sha1(b'changeme').hexdigest() + "')")
# We'll add one already upgraded, so you can evaluate the different format of password field
c.execute("INSERT INTO AppUsers VALUES ('userd','" + bcrypt.hashpw((hashlib.sha1(b'r00t').hexdigest()).encode('UTF-8'),bcrypt.gensalt()).decode('UTF-8') + "')")
# Add one new format, to show it also works
c.execute("INSERT INTO AppUsers VALUES ('usere','" + bcrypt.hashpw('Spring2020!'.encode('UTF-8'),bcrypt.gensalt()).decode('UTF-8') + "')")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
