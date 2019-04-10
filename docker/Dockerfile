
# Build: 
##  docker build -t cmpe272assignment .

# To Run (-it for interactive mode)
## docker run -it --rm cmpe272assignment

FROM ubuntu:bionic

WORKDIR /root/

#COPY ./server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#COPY . . 
CMD ["/bin/bash"]

