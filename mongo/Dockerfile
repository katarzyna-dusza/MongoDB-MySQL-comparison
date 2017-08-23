FROM phusion/baseimage:0.9.9

ENV HOME /root

# Mongodb Installation
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
RUN echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

# Install MongoDB
RUN apt-get update
RUN apt-get install -y mongodb-org
RUN mkdir -p /data/db
RUN chown -R mongodb:mongodb /data
RUN echo "bind_ip = 0.0.0.0" >> /etc/mongodb.conf

# Mongo runs on 27017
EXPOSE 27017
# END Mongodb Installation

# Clean up APT when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["mongod"]