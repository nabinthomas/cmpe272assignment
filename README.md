# CMPE272 Assignment - aMAZE Group

Team members: 
1. Binu Jose
2. Ginto George
3. Nabin Thomas
4. Sandeep Panakkal

## Status

1. Assignment 1 - In progress

## Build instructions
1. Install git and Sync code to your local machine. (to <gitroot>)
2. Create clone of the repository.	
	git clone https://github.com/nabinthomas/cmpe272assignment.git
  	chmod 700 README.md
	git checkout -b cmpe272assignment_binu
	#following will create the branch and push in changes
	git push origin cmpe272assignment_binu
	#after modifying any file do the following command to update 
	git add -u 
	#commit the changes
	git commit -m "message"
	#push it back to your branch 
	git push origin cmpe272assignment_binu 
3. Install docker
4. Build docker image
```bash
    cd <gitroot>/ 
    docker build -t cmpe272assignment -f docker/Dockerfile .
```

## To Run the docker image
1. Interactive mode
```bash
    docker run -it --rm cmpe272assignment
```
2. Run the server with local files.
```bash
        cd <gitroot>/ 
        docker run  --rm -v `pwd`/server:/root/app/server -p 80:80/tcp cmpe272assignment
```
3. Run the server with prepackaged application files. 
```bash
        docker run  --rm  -p 80:80/tcp cmpe272assignment
```

# Git Cheatsheat
- http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf

