#!/bin/bash
#check_docker_client=`docker ps`
docker ps 2> /dev/null
if [ $? -ne 1 ]; then
    echo "docker daemon properly configured"
else
    echo "docker daemon was not properly configured, is the service running?"
    exit
fi

(cd util/dockerfiles/cppcheck/ && docker build . -t cppcheck)
(cd util/dockerfiles/flawfinder/ && docker build . -t flawfinder)
(cd util/dockerfiles/clang-analyzer/ && docker build . -t clang-analyzer)
(cd util/dockerfiles/frama-c/ && docker build . -t frama-c)


