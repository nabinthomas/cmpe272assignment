
# Build: 
##  docker build -t cmpe272assignment .

# To Run (-it for interactive mode)
## docker run -it --rm cmpe272assignment

FROM ubuntu:bionic

WORKDIR /root/

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
#RUN apt-get install -y python3-venv
RUN pip3 install flask
#COPY ./server/requirements.txt ./
#RUN pip3 install --no-cache-dir -r requirements.txt
#COPY . . 
CMD ["/bin/bash"]

