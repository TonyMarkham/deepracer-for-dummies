#!/usr/bin/env bash

SCRIPT='realpath $0'
SCRIPTPATH='dirname $SCRIPT'

#export ROBOMAKER_COMMAND="./run.sh build distributed_training.launch"
export ROBOMAKER_RUN_TYPE=distributed_training

docker-compose -f "$SCRIPTPATH/../../docker/docker-compose.yml up -d
echo 'waiting for containers to start up...'

#sleep for 20 seconds to allow the containers to start
sleep 15

echo 'attempting to pull up sagemaker logs...'
gnome-terminal -x sh -c "docker logs -f $(docker ps | awk ' /sagemaker/ { print $1 }')"

echo 'attempting to open vnc viewer...'
gnome-terminal -x sh -c "echo vncviewer;vncviewer localhost:8080"
