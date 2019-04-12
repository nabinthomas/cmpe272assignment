
# Build: 
##  docker build -t cmpe272assignment .

# To Run (-it for interactive mode)
## docker run -it --rm cmpe272assignment

FROM ubuntu:bionic

WORKDIR /root/

#Install required tools and frameworks. 
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install flask

#Expose ports
EXPOSE 80/tcp


#RUN pip3 install --no-cache-dir -r requirements.txt

#COPY The app folders. 


#Default command to start the server
CMD ["python3", "app/server/main.py"]

