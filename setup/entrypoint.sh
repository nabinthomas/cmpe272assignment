#!/bin/bash

## Entry point for Docker image. 
##      Command options supported: 
##          unittest - Runs the unit tests
##          bash - Runs the bash shell
##          startserver - Runs the servers (DB and web servers)

echo `pwd`
#echo "$#"

if [ "$#" -eq 2 ]; then
    command=$2
    CLIENT_SECRET=$1
    echo "CLIENT SECRET IS [$CLIENT_SECRET]"
    mkdir -p /root/app/server/config/
    echo "CLIENT_SECRET=$CLIENT_SECRET" >> /root/app/server/config/settings.cfg

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
    echo "Usage: docker run .....params.... <auth0clientsecret> startserver "
    echo "OR"
    echo "Usage: docker run .....params.... <auth0clientsecret> unittest"
fi

