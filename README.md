# MongoDB and MySQL performance comparison

## Overview
This repo is still in progress.

## Requirements
- **Docker** for building one, equivalent environment in both images. They are based on the same image: [phusion/baseimage:0.9.9](https://github.com/phusion/baseimage-docker), which is very light.
- **Python 3.6.2** for running measurements, collecting results, preparing and populating test data.

## Build image and run container
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
