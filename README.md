# CMPE272 Assignment - aMAZE Group

After submission

Team members: 
1. Binu Jose
2. Ginto George
3. Nabin Thomas
4. Sandeep Panakkal

## Status

1. Assignment 1 - Submitted. 
	* Docker hub image: amazeteam/cmpe272assignment:1.0
	* Github tag 1.0
2. Assginment 2 - In progress.

## Build instructions
1. Install git and Sync code to your local machine. (to <gitroot>)
2. Install docker
3. Build docker image
```bash
    cd <gitroot>/ 
    docker build -t amazeteam/cmpe272assignment -f docker/Dockerfile .
```
## Modifying files with Git branches
1. Create clone of the repository.	
```bash
	git clone https://github.com/nabinthomas/cmpe272assignment.git
  	chmod 700 README.md
```
2. Checkout branch and push changes back to the branch. 
```bash
	git checkout -b cmpe272assignment_binu
	#following will create the branch and push in changes
	git push origin cmpe272assignment_binu
	#after modifying any file do the following command to update 
	git add -u 
	#commit the changes
	git commit -m "message"
	#push it back to your branch 
	git push origin cmpe272assignment_binu 
```
3. Now open a pull request from this branch to the main branch using github. 

## To Run the docker image
1. Interactive mode
```bash
    cd <gitroot>/ 
    docker run -it --rm -p 80:80/tcp -v `pwd`/../database:/data/db amazeteam/cmpe272assignment bash
```
2. Run the server with local files.
```bash
        cd <gitroot>/ 
        docker run --rm -p 80:80/tcp -v `pwd`/..:/root/app/ -v `pwd`/../database:/data/db  -p 80:80/tcp amazeteam/cmpe272assignment
```
3. Run the server with prepackaged application files. 
```bash
        cd <gitroot>/ 
        docker run --rm -p 80:80/tcp -v `pwd`/../database:/data/db amazeteam/cmpe272assignment
```
**Note**: _The database dir is kept outside the docker image to make sure the data is persistent across docker runs. For testing, a different database directory may be used to avoid corrupting real data._ 
## To push the docker image to docker hub
```bash
docker push amazeteam/cmpe272assignment
```
## To deploy docker on aws ec2 instance (linux 2 ami)
### To run the latest version from dockerhub
```bash
sudo service docker start
nohup sudo docker run --rm -p 80:80/tcp amazeteam/cmpe272assignment
```
### To run a specific version from dockerhub
```bash
sudo service docker start
nohup sudo docker run --rm -p 80:80/tcp amazeteam/cmpe272assignment:version
```
**Note**: _Replace version with the right tag to run._
# Git Cheatsheat
- http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf

