#!/usr/bin/env python3

import sys
import pymongo
import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

# To achieve reliable test results I encourage you to run tests for different database's size, like 10, 100, 1000 etc.
documentsNumber = int(sys.argv[1])

# We create suitable databases for running various tests
db = client["database{}".format(documentsNumber)]
collection = db["posts"]

# Start time of all insertions
start = datetime.datetime.now()

for i in range(0, documentsNumber):
    # Start time of a single insertion
    now = datetime.datetime.now()

    post = {
        "title": "Title{}".format(i),
        "content": "Content{}".format(i),
        "tags": ["Tag", "Tag{}".format(i)],
        "created": now,
        "categories": ["Category", "Category{}".format(i)],
        "likes": [
            {
                "username": "NormalUser"
            }
        ],
        "comments": [
            {
                "username": "NormalUser",
                "text": "Text{}".format(i)
            }
        ]
    }
    collection.insert_one(post)

    # Duration of a single insertion
    print(str(datetime.datetime.now() - now))

# End time for inserting all of the documents
end = datetime.datetime.now()

print("Duration of all insertions:")
print(str(end - start))
