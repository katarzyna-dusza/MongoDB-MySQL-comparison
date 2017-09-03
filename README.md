# MongoDB and MySQL performance comparison

## Overview
This repo is a part of my master's thesis, of which the main topic was comparing a performance between databases (MongoDB, MySQL) and web services (written in Node.JS 7, PHP 7).
It's still in progress. 

## Requirements
- **Docker** for building one, equivalent environment in both images. They are based on the same image: [phusion/baseimage:0.9.9](https://github.com/phusion/baseimage-docker), which is very light.
- **Python 3.6.2** for running measurements, collecting results, preparing and populating test data.
- **sys, datetime, pymongo, PyMySQL** libraries installed

## Build images and run containers
### MongoDB
1. Go to `mongo` directory and run 
    ```shell
    docker build -t mongo-image .
    ```
    
1. Run a container with _mongod_ by running 
    ```shell
    docker run -p 27017:27017 --name=my-mongo mongo-image
    ```
    
1. Run _mongo_ in the newly created container to make sure that everything is up and working :)
    ```
    docker ps
    docker exec -it my-mongo bash
    cd /data/db
    mongo
    ```

> NOTICE:
If you have already installed MongoDB on your local machine, make sure, that you don't have any running _mongod_ processes: ```ps aux | grep mongo```
If so, then kill it: `kill PID_ID`. Remember, if you won't kill them, then all python scripts will be trying to connect with your _MongoDB_ on your local machine instead of container's one.

### MySQL
1. Go to `mysql` directory and run 
    ```shell
    docker build -t mysql-image .
    ```

1. Run a container by running 
    ```shell
    docker run -p 3306:3306 --name=my-mysql mysql-image
    ```
    
1. Log into _mysql_ and set grants in the newly created container
    ```
    docker ps
    docker exec -it my-mysql bash
    mysql -u root -p
    # password: root
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.17.0.1' IDENTIFIED BY '';
    ```

> NOTICE:
I assume you have already noticed difference between MongoDB and MySQL insertions. In MongoDB, we have more information than in MySQL (like category for example), because I used the second normal form. Thus, all information about categories and tags are in other tables - we don't need them to make performance tests. But if you want to create other tables, then run simply `./createTables.py <documents_number>` in `mysql` directory.


## Test MongoDB performance
1. Install `pymongo` library by running
    ```shell
    python3 -m pip install pymongo
    ```
1. Run _inserting data_ performance test passing the number of documents to be inserted as an argument.
    ```shell
    ./insertDataToMongoDB.py <documents_number>
    ``` 
> INFO:
You can change the number of inserted documents. The schema of a document is a blog post - you can also change it, but keep in mind that all Python scripts are prepared for that schema. 

3. Run _fetching data_ performance test passing the required number of documents (to connect with proper database) and an option, which represents a query. Skip, limit and uniqueNumber arguments are optional.
 
   Possible options (queries):
    - uniqueCategory (required option: unique number)
    - nonUniqueCategory
     - uniqueCategoryAndUniqueTag (required option: unique number)
     - nonUniqueCategoriesAndTags
     - favouritePosts
     - skip (required options: skip and limit numbers)
    
    Command for running tests:
    ```shell
    ./fetchingDataFromMongoDB.py <documents_number> <query_option> <other_arguments>
    ``` 
 
    Running tests examples:
    
    ```shell
    # Fetching data from 10-element's database and SKIP 5 elements LIMIT to 3 documents
    ./fetchingDataFromMongoDB.py 10 skip 5 3
    
    # Fetching data with nonunique category from 100-element's database
    ./fetchingDataFromMongoDB.py 100 nonUniqueCategory
    ```

## Test MySQL performance
1. Install `pymysql` library by running
    ```shell
    python3 -m pip install PyMySQL
    ```

1. Run _inserting data_ performance test passing the number of rows to be inserted as an argument.
    ```shell
    ./insertDataToMySQL.py <documents_number>
    ``` 
    
> INFO:
In _insertDataToMySQL.py_ script we also measure duration with creating database, because as you probably now, in MongoDB there is no possibility to create database or collection without insert operation - that's why our MySQL tests (without creating databases) could be a little bit distorted. 

3. Run _fetching data_ performance test passing the required number of rows (to connect with proper database) and an option, which represents a query. Skip, limit and uniqueNumber arguments are optional.
 
   Possible options (queries):
    - uniqueCategory (required option: unique number)
    - nonUniqueCategory
    - uniqueCategoryAndUniqueTag (required option: unique number)
    - nonUniqueCategoriesAndTags
    - favouritePosts
    - skip (required options: skip and limit numbers) - it behaves differently from MongoDB option!
    
    Command for running tests:
    ```shell
    ./fetchingDataFromMySQL.py <rows_number> <query_option> <other_arguments>
    ``` 
 
    Running tests examples:
    
    ```shell
    # Fetching data from 10-element's database and SKIP 3 elements LIMIT to 5 rows
    ./fetchingDataFromMySQL.py 10 skip 5 3
    
    # Fetching data with nonunique category from 100-element's database
    ./fetchingDataFromMySQL.py 100 nonUniqueCategory
    ```