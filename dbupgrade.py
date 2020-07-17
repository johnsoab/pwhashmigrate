import sqlite3
import bcrypt

conn = sqlite3.connect('example.db')
c = conn.cursor()

# Grab all values in AppUsers table where the password format hasn't been converted. If using Bcrypt, the prefix will be $2b.
for row in c.execute("SELECT username,password FROM AppUsers WHERE password NOT LIKE '$2b%'").fetchall():
    print("UPDATE AppUsers SET password = ? WHERE username = ?", ((bcrypt.hashpw(row[1].encode('UTF-8'), bcrypt.gensalt() ).decode('UTF-8')), row[0]))
    c.execute("UPDATE AppUsers SET password = ? WHERE username = ?", ((bcrypt.hashpw(row[1].encode('UTF-8'), bcrypt.gensalt() ).decode('UTF-8')), row[0]))
            

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
