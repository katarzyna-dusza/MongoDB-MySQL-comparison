#!/usr/bin/env python3

import sys
import pymysql.cursors
import datetime

connection = pymysql.connect(host='localhost', port=3306, user='root', password='')
cursor = connection.cursor()

# Run tests for different database's size, like 10, 100, 1000 etc. just like during MongoDB tests
documentsNumber = int(sys.argv[1])

# Start time of all insertions
start = datetime.datetime.now()

# We create suitable databases for running various tests
createDatabase = "CREATE DATABASE database{}".format(documentsNumber)
useDatabase = "USE database{}".format(documentsNumber)
createTable = "CREATE TABLE posts (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, title VARCHAR(250) NOT NULL, content VARCHAR(250) NOT NULL, created VARCHAR(250))"
sql = "INSERT INTO `posts` (`title`, `content`, `created`) VALUES (%s, %s, %s)"

with connection.cursor() as cursor:
        cursor.execute(createDatabase)
        cursor.execute(useDatabase)
        cursor.execute(createTable)

        for i in range(0, documentsNumber):
            # Start time of a single insertion
            now = datetime.datetime.now()

            cursor.execute(sql, ("Title{}".format(i), "Content{}".format(i), now))
            connection.commit()

            # Duration of a single insertion
            print(str(datetime.datetime.now() - now))

# End time for inserting all of the documents
end = datetime.datetime.now()

print("Duration of all insertions:")
print(str(end - start))

connection.close()
