# pwhashmigrate
Simple Python3/SQLite3 demo of migrating from sha1 hashes to bcrypt by wrapping the original hashes.
This is useful when
1. You have a database full of users whos passwords are plain sha1 hashes (same concept would work for any hash.. m4/md5/sha1/sha256/sha384/sha512)
1. You really need to upgrade to a more secure password hash storage
1. Your users don't login frequently enough, or have expiring passwords (otherwise, just update the storage at next login)
1. You don't want to, or can't reset all users passwords and force them to create a new one
1. You eventually want to excise all old hash methods from your code

## Quick explanation of the demo
First, we're creating a database of user/password hashes. Usually, you'll have something like sha1 hashes for users, and you want to improve the security of the storage mechanism.
You COULD simply bcrypt all the sha1 hashes in the database (as the dbupgrade.py does), and upon login, always sha1() the users password, and feed that into the bcrypt.checkpw() method as this demo does as a fall through. That is 100% safe. The downside is, that sha1() method call will always be in your code, and SAST/Linters will forever torment you that you use legacy hash methods.

The alternative is: you may choose to try native bcrypt.checkpw() first, and only fail back to bcrypt.hashpw(sha1(password)). 
This means keeping the sha1() conversion around for a while, as users who havent changed their password recently will still need to hit.
After a suitable time, if all of your active users have signed in, you can remove the sha1() check, and simply disable or reset those remaining users who haven't logged in since the change. The good news is, at least their password wasnt stored as sha1() anymore.


## To demonstrate, setup your python3 virtualenv, and install the requirements (really just bcrypt).
usually just:
```
virtualenv .
pip install -r ./requirements.txt
```

## Don't forget to activate your virtualenv:
```
$ . ./bin/activate
```

## Now create the database with example data:
```
python3 ./dbcreate.py
```

This will create the sqlite database and seed it with five accounts of various types of passwords.
Feel free to query the sqlite AppUsers table to see the values.

```
$ sqlite3 ./example.db

SQLite version 3.33.0 2020-08-14 13:23:32
Enter ".help" for usage hints.

example.db
sqlite> .tables
AppUsers
sqlite> select * from AppUsers;
usera|5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
userb|cbfdac6008f9cab4083784cbd1874f76618d2a97
userc|fa9beb99e4029ad5a6615399e7bbae21356086b3
userd|$2b$12$OMCfN2AMRVEllvVE/m3NveXPjddOlXQDsIJTCXZGDlDuHslNAdZci
usere|$2b$12$S2bvph/d2DTHYucQibnRQekR.nNh3tG2JbKmvhhnjq3AHxCttcy.2
sqlite>
```

## Next, Perform the upgrade on the old hashes:
```
python3 ./dbupgrade.py
```

This will read any non-bcrypt passwords and bcrypt the sha1 values, so that only the bcrypt entry remains in the database. All sha1 entries in the table will be gone.

## Finally, run the test harness to make sure the passwords still work (or fail):
```
python3 ./dbtestpw.py
```

This will execute a few user/password tests to demonstrate how the various methods are working.
