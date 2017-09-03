#!/usr/bin/env python3

import pymongo
import datetime
import math
import sys
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Definitions
uniqueNumber = 0
skip = 0
limit = 0

# Database size provided before
documentsNumber = int(sys.argv[1])

# One of 6 queries to choose
option = sys.argv[2]

# In case of unique data like unique category, we have to pass uniqueNumber option with an unique number
if option == 'uniqueCategoryAndUniqueTag' or option == 'uniqueCategory':
    uniqueNumber = int(sys.argv[3])

# In case of skip data like pagination, we have to pass skip and limit options
if option == 'skip':
    skip = int(sys.argv[3])
    limit = int(sys.argv[4])

# Connecting with proper databases for the tests
db = client["database{}".format(documentsNumber)]
collection = db['posts']

# Queries
uniqueCategory = {
    'categories': "Category{}".format(uniqueNumber)
}

nonUniqueCategory = {
    'categories': 'Category'
}

uniqueCategoryAndUniqueTag = {
    '$or': [
            {"tags": {'$in': "Tag{}".format(uniqueNumber)}},
            {"categories": {'$in': "Category{}".format(uniqueNumber)}}
        ]
}

nonUniqueCategoriesAndTags = {
    '$or': [
            {"tags": {'$in': 'Tag'}},
            {"categories": {'$in': 'Category'}}
        ]
}

favouritePosts = {
    'likes.username': 'NormalUser'
}

posts = {
  'uniqueCategory': collection.find(uniqueCategory),
  'nonUniqueCategory': collection.find(nonUniqueCategory),
  'uniqueCategoryAndUniqueTag': collection.find(uniqueCategoryAndUniqueTag),
  'nonUniqueCategoriesAndTags': collection.find(nonUniqueCategoriesAndTags),
  'favouritePosts': collection.find(favouritePosts),
  'skip': collection.find().skip(skip).limit(limit)
}

# Start time of a getting data
now = datetime.datetime.now()

# Getting data
posts = posts.get(option)

# End time for getting all of the matched documents
end = str(datetime.datetime.now() - now)

# Just for displaying data
for post in posts:
    print(post)

print("Duration of fetching documents:")
print(end)
