# CMPE272 Assignment - aMAZE Group


Team members: 
1. Binu Jose
2. Ginto George
3. Nabin Thomas
4. Sandeep Panakkal

## Status

### CI/CD Status (Travis-CI)
[![Build Status](https://travis-ci.org/nabinthomas/cmpe272assignment.svg?branch=master)](https://travis-ci.org/nabinthomas/cmpe272assignment)

### Implementation Status
1. Assignment 1 - Submitted. 
	* Docker hub image: amazeteam/cmpe272assignment:1.0
	* Github tag 1.0
2. Assginment 2 - Submitted. 
	* Docker hub image: amazeteam/cmpe272assignment:2.0
	* Github tag 2.0
3. Assginment 3 - Submitted.
	* Docker hub image: amazeteam/cmpe272assignment:3.0
	* Github tag 3.0
4. Assginment 4 - Submitted.
	* Docker hub image: amazeteam/cmpe272assignment:4.0
	* Github tag 4.0
5. Assginment 5 - Submitted
	* Docker hub image: amazeteam/cmpe272assignment:5.0
	* Github tag 5.0
6. Assginment 6 - Ready to submit
	* Docker hub image: amazeteam/cmpe272assignment:6.0 
	* Github tag 6.0 
7. Assginment 7 - In Progress
	* Docker hub image: amazeteam/cmpe272assignment:7.0 (To be created)
	* Github tag 7.0 (To be created)

## Build instructions
1. Install git and Sync code to your local machine. (to ```<gitroot>```)
2. Install docker
3. Build docker image
```bash
    cd <gitroot>/ 
    export AUTHO_CLIENT_SECRET="'aDoe0md20-pFTGP6_XmoazFiUZdYN1Ze5CwxX21qDl1U_MaYbasmuJ4fjb7fDNlZ'""; echo "CLIENT_SECRET=$AUTHO_CLIENT_SECRET"; docker build -t amazeteam/cmpe272assignment -f docker/Dockerfile .
```
## Modifying files with Git branches
1. Create clone of the repository.	
```bash
	git clone https://github.com/nabinthomas/cmpe272assignment.git
```
2. Create your branch, checkout branch and push changes back to the branch. 
```bash
	cd cmpe272assignment
	git checkout -b cmpe272assignment_<branchname>
	#following will create the branch and push in changes
	git push origin cmpe272assignment_<branchname>
	#after modifying any file do the following command to update 
	git add -u 
	#commit the changes
	git commit -m "message"
	#push it back to your branch 
	git push origin cmpe272assignment_<branchname> 
```
3. Now open a pull request from this branch to the main branch using github. 

## To Run the docker image
1. Interactive mode
```bash
    cd <gitroot>/ 
    docker run -it --rm -p 80:80/tcp -p 443:443/tcp -v `pwd`/../database:/data/db amazeteam/cmpe272assignment bash
```
2. Run the server with local files.
```bash
        cd <gitroot>/ 
        docker run --rm -p 80:80/tcp -p 443:443/tcp -v `pwd`/server:/root/app/server -v `pwd`/../database:/data/db -v `pwd`/setup:/root/setup -v `pwd`/test:/root/test   amazeteam/cmpe272assignment
```
3. Run the server with prepackaged application files. 
```bash
        cd <gitroot>/ 
        docker run --rm -p 80:80/tcp -p 443:443/tcp -v `pwd`/../database:/data/db amazeteam/cmpe272assignment
```
4. Run the unit tests
```bash
        cd <gitroot>/ 
        docker run --rm amazeteam/cmpe272assignment unittest
```
5. Kill the current server and rebuild/restart. 
```bash
	cd <gitroot>/
	TODO : The client secret below will be changed. 
	export AUTHO_CLIENT_SECRET="'aDoe0md20-pFTGP6_XmoazFiUZdYN1Ze5CwxX21qDl1U_MaYbasmuJ4fjb7fDNlZ'"; echo "CLIENT_SECRET=$AUTHO_CLIENT_SECRET" >> server/config/settings.cfg ;docker kill `docker ps |grep amaze |cut -f 1 -d ' '`; docker build -t amazeteam/cmpe272assignment -f docker/Dockerfile . ; docker run --rm -p 80:80/tcp -p 443:443/tcp -v `pwd`/server:/root/app/server -v `pwd`/../database:/data/db -v `pwd`/setup:/root/setup -v `pwd`/test:/root/test   -it amazeteam/cmpe272assignment 
```
**Note**: _The database dir is kept outside the docker image to make sure the data is persistent across docker runs. For testing, a different database directory may be used to avoid corrupting real data._ 
## To push the docker image to docker hub
```bash
docker login
docker push amazeteam/cmpe272assignment
```
**Note**: _ Docker image is automatically pushed to Dockerhub with "latest" tag only for commits to the master branch. All other branches will have the branchname as the tag _ 

## To deploy docker on aws ec2 instance (linux 2 ami)
### To run the latest version from dockerhub
```bash
sudo service docker start
nohup sudo docker run --rm -p 80:80/tcp -p 443:443/tcp amazeteam/cmpe272assignment
```
### To run a specific version from dockerhub
```bash
sudo service docker start
nohup sudo docker run --rm -p 80:80/tcp -p 443:443/tcp amazeteam/cmpe272assignment:version
```
**Note**: _Replace **version** with the right tag to run._
# Git Cheatsheat
- http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf

