# pwhashmigrate
Simple Python3/SQLite3 demo of migrating from sha1 hashes to bcrypt by wrapping the original hashes.

To demonstrate, setup your python3 virtualenv, and install the requirements (really just bcrypt).
Then execute:
python3 ./dbcreate.py

This will create the sqlite database and seed it with five accounts of various types of passwords.
Feel free to query the sqlite AppUsers table to see the values.

Next, execute:
python3 ./dbupgrade.py

This will read any non-bcrypt passwords and bcrypt the sha1 values, so that only the bcrypt entry remains in the database. All sha1 entries in the table will be gone.

Finally, execute:
python3 ./dbtestpw.py

This will execute a few user/password tests to demonstrate how the various methods are working.
