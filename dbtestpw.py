import sqlite3
import hashlib
import bcrypt

conn = sqlite3.connect('example.db')
c = conn.cursor()


def checkpw(username, password):
    """
    Accept username, and raw password from user
    First attempt, simply bcrypt.checkpw(password) for the user
    If fails, perhaps it's an upgraded hash, so instead, bcrypt.checkpw(sha1(password))
    """
    user = c.execute("SELECT username,password FROM AppUsers WHERE username = ? LIMIT 1", (username,)).fetchone()
    if (len(user) > 0):
        if (bcrypt.checkpw(password.encode('UTF-8'), (user[1].encode('UTF-8')))):
             print("Successfully logged in as", username, "using new scheme")
             return 0
        else:
             # If we failed the password check natively, now sha1 the original password. Linters/SAST may complain about using sha1, but under this context, it is safe: we're not storing it this way, it's to support legacy lookup. 
             sha1pw = (hashlib.sha1(password.encode('UTF-8')).hexdigest()).encode('UTF-8')
             if (bcrypt.checkpw(sha1pw, user[1].encode('UTF-8'))):
                 print("Successfully logged in as", username ,"using old scheme")
                 # Consider updating the hash here if user passwords never expire, since you now have the real users password, and it's been verified.
                 # This will drop the sha1 secondary lookup from recurring.
                 return 0
    # our final fall thru is reject
    print("Failed username or password for ", username)
    return 1


# Should pass
assert(checkpw('usera','password') == 0)

# Should fail
assert(checkpw('userb','password1') == 1)

# Should pass
assert(checkpw('userb','password123') == 0)

# Should fail
assert(checkpw('usera','badpass') == 1)

# Should pass
assert(checkpw('userd','r00t') == 0)

# Should pass
assert(checkpw('usere','Spring2020!') == 0)
# Save (commit) the changes
#conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
