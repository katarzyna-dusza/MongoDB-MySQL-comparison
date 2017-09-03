#!/usr/bin/env python3

import datetime
import math
import sys
import pymysql.cursors

# Definitions.
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
connection = pymysql.connect(host='localhost', port=3306, user='root', password='', db="database{}".format(documentsNumber))
cursor = connection.cursor()

# Queries
uniqueCategory = "SELECT title, content, created FROM posts AS p JOIN postsCategories AS pc ON p.id = pc.post_id JOIN categories AS c ON pc.category_id = c.id_category WHERE c.name = 'Category{}'".format(uniqueNumber)

nonUniqueCategory = "SELECT * FROM posts AS p JOIN postsCategories AS pc ON p.id = pc.post_id JOIN categories AS c ON pc.category_id = c.id_category WHERE c.name = 'Category'"

uniqueCategoryAndUniqueTag = "SELECT DISTINCT title, content, created FROM posts AS p JOIN postsCategories AS pc ON p.id = pc.post_id JOIN categories AS c ON pc.category_id = c.id_category JOIN postsTags AS pt ON p.id = pt.post_id JOIN tags AS t ON pt.tag_id = t.id_tag WHERE c.name = 'Category{}'".format(uniqueNumber)  + " OR t.name = 'Tag{}'".format(uniqueNumber)

nonUniqueCategoriesAndTags = "SELECT DISTINCT title, content, created FROM posts AS p JOIN postsCategories AS pc ON p.id = pc.post_id JOIN categories AS c ON pc.category_id = c.id_category JOIN postsTags AS pt ON p.id = pt.post_id JOIN tags AS t ON pt.tag_id = t.id_tag WHERE c.name IN ('Category') OR t.name IN ('Tag')"

favouritePosts = "SELECT * FROM posts AS p JOIN likes AS l ON p.id = l.post_id JOIN users AS u ON l.user_id = u.id_user WHERE u.name = 'NormalUser'"

pagination = "SELECT * FROM posts LIMIT {}".format(limit) + ", {}".format(skip)

posts = {
  'uniqueCategory': uniqueCategory,
  'nonUniqueCategory': nonUniqueCategory,
  'uniqueCategoryAndUniqueTag': uniqueCategoryAndUniqueTag,
  'nonUniqueCategoriesAndTags': nonUniqueCategoriesAndTags,
  'favouritePosts': favouritePosts,
  'skip': pagination
}

posts = posts.get(option)

# Start time of a getting data
now = datetime.datetime.now()

# Getting data
cursor.execute(posts)
posts = cursor.fetchall()

# End time for getting all of the matched documents
end = str(datetime.datetime.now() - now)

# Just for displaying data
for post in posts:
    print(post)

print("Duration of fetching documents:")
print(end)
