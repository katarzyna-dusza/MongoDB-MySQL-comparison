#!/usr/bin/env python3

import sys
import pymysql.cursors
import datetime

# Database's size
documentsNumber = int(sys.argv[1])

connection = pymysql.connect(host='localhost', port=3306, user='root', password='', db="database{}".format(documentsNumber))
cursor = connection.cursor()

# Create 1-N tables
createTags = 'CREATE TABLE tags (id_tag INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250) NOT NULL)'
createCategories = 'CREATE TABLE categories (id_category INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250) NOT NULL)'
createUsers = 'CREATE TABLE users (id_user INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250) NOT NULL, password VARCHAR(250) NOT NULL)'

# Create M-N tables
createPostsCategories = 'CREATE TABLE postsCategories (id_post_category INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, post_id INT(10), category_id INT(10))'
createPostsTags = 'CREATE TABLE postsTags (id_post_tag INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, post_id INT(11), tag_id INT(10))'
createLikes = 'CREATE TABLE likes (id_like INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, post_id INT(11), user_id INT(10))'

with connection.cursor() as cursor:
    cursor.execute(createTags)
    cursor.execute(createCategories)
    cursor.execute(createUsers)

    cursor.execute(createPostsCategories)
    cursor.execute(createPostsTags)
    cursor.execute(createLikes)

    # tags
    sql = "INSERT INTO `tags` (`name`) VALUES (%s)"
    cursor.execute(sql, ('Tag'))
    connection.commit()

    for i in range(0, documentsNumber):
        sql = "INSERT INTO `tags` (`name`) VALUES (%s)"
        cursor.execute(sql, ("Tag{}".format(i)))
        connection.commit()

    # categories
    sql = "INSERT INTO `categories` (`name`) VALUES (%s)"
    cursor.execute(sql, ('Category'))
    connection.commit()

    for i in range(0, documentsNumber):
        sql = "INSERT INTO `categories` (`name`) VALUES (%s)"
        cursor.execute(sql, ("Category{}".format(i)))
        connection.commit()

    # users
    sql = "INSERT INTO `users` (`name`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, ('NormalUser', 'password'))
    connection.commit()

    # posts tags
    sql = "INSERT INTO `postsTags` (`post_id`, `tag_id`) VALUES (%s, %s)"
    for i in range(0, documentsNumber):
        cursor.execute(sql, (i+1, 1))
        connection.commit()

        cursor.execute(sql, (i+1, i+2))
        connection.commit()

    # posts categories
    sql = "INSERT INTO `postsCategories` (`post_id`, `category_id`) VALUES (%s, %s)"
    for i in range(0, documentsNumber):
        cursor.execute(sql, (i+1, 1))
        connection.commit()

        cursor.execute(sql, (i+1, i+2))
        connection.commit()

    # likes
    sql = "INSERT INTO `likes` (`post_id`, `user_id`) VALUES (%s, %s)"
    for i in range(0, documentsNumber):
        cursor.execute(sql, (i+1, 1))
        connection.commit()

connection.close()