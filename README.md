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
..1. To build the docker image.
```bash
    cd <gitroot>/ 
    docker build -t cmpe272assignment -f docker/Dockerfile .
```

..2. To Run 
 Interactive mode
    docker run -it --rm cmpe272assignment
 Run the server with local files. 
    From the docker dir: 
        docker run  --rm -v `pwd`/..:/root/app/ -p 80:80/tcp cmpe272assignment
        Run the server with prepackaged application files. 
        docker run  --rm  -p 80:80/tcp cmpe272assignment

# Git Cheatsheat
- http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf
http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf
