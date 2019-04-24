#!/bin/bash

## Entry point for Docker image. 
## Command options supported: 
## unittest - Runs the unit tests
## bash - Runs the bash shell
## startserver - Runs the servers (DB and web servers)

echo `pwd`
#echo "$#"

if [ "$#" -ne 0 ]; then
    command=$1

    #echo "Option was $1"
    case $command in
        "unittest")
            /bin/bash test/unittests/test_run_all.sh
        ;;
        "bash") 
            /bin/bash
        ;;
        "startserver")
            /bin/bash setup/startservers.sh
        ;;
        *)
            echo "Unknown option Exiting"
            exit -1
        ;;
    esac
else
    # Default is to start the servers
    setup/startservers.sh
fi

