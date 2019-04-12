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
2. Install docker
3. Build docker image
```bash
    cd <gitroot>/ 
    docker build -t cmpe272assignment -f docker/Dockerfile .
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

