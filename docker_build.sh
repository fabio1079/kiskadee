#!/bin/bash
#check_docker_client=`docker ps`
docker ps 2> /dev/null
if [ $? -ne 1 ]; then
    echo "docker daemon properly configured. Building images..."
else
    echo "docker daemon was not properly configured, is the service running?"
    exit
fi

pushd util/dockerfiles;
for analyzer in `ls`; do
  pushd $analyzer;
  docker build . -t $analyzer;
  popd
done
