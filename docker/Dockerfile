
# Build: 
## cd <gitroot>/ 
##  docker build -t cmpe272assignment -f docker/Dockerfile .

# To Run 
## Interactive mode
### docker run -it --rm cmpe272assignment
## Run the server with local files. 
### From the docker dir: 
### docker run  --rm -v `pwd`/..:/root/app/ -p 80:80/tcp cmpe272assignment
## Run the server with prepackaged application files. 
### docker run  --rm  -p 80:80/tcp cmpe272assignment

FROM ubuntu:bionic

WORKDIR /root/

#Install required tools and frameworks. 
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install flask
RUN pip3 install pytz

#Expose ports
EXPOSE 80/tcp

#RUN pip3 install --no-cache-dir -r requirements.txt

#COPY The app folders. 
COPY server /root/app/server

#Default command to start the server
CMD ["python3", "app/server/main.py"]

