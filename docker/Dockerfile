# Build: 
## cd <gitroot>/ 
##  docker build -t amazeteam/cmpe272assignment -f docker/Dockerfile .

# To Run From the <gitroot> dir: 
## Interactive mode
### docker run -it --rm -p 80:80/tcp -v `pwd`/../database:/data/db amazeteam/cmpe272assignment bash
## Run the server with local files. 
### docker run --rm -p 80:80/tcp -v `pwd`/..:/root/app/ -v `pwd`/../database:/data/db amazeteam/cmpe272assignment
## Run the server with prepackaged application files. 
### docker run --rm -p 80:80/tcp -v `pwd`/../database:/data/db amazeteam/cmpe272assignment

FROM ubuntu:bionic

WORKDIR /root/

#Install required tools and frameworks. 
RUN apt-get update --fix-missing
RUN apt-get install -y python3
RUN apt-get install -y vim
RUN apt-get install -y python3-pip
RUN apt-get install -y mongodb mongodb-server mongo-tools
RUN pip3 install flask
RUN pip3 install pytz
RUN pip3 install python-jose
RUN pip3 install six
# pymongo  for connecting to mongodb
RUN pip3 install pymongo
# For unit tests. TODO: Keep this only for unit tests
RUN pip3 install mongomock
RUN pip3 install pyopenssl
#Expose ports
EXPOSE 80/tcp
EXPOSE 443/tcp

#COPY The app folders. 
COPY server /root/app/server
COPY setup setup
#COPY data data
COPY test test

# Main entry point for the docker image
ENTRYPOINT [ "/bin/bash", "setup/entrypoint.sh" ]

# see ../setup/entrypoint.sh for other possible commands. 
# Default command is to start the servers
CMD ["startserver"]
