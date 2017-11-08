#!/bin/sh

useradd -ms /bin/bash kiskadee -u $KISKADEE_UID
chown -R kiskadee:kiskadee /src
chmod -R 755 /src
cd /src

# get all header files in the given path
HEADERS=`find . | grep '\.h$' | sed 's/\/[^/]\+\.h$//' | sort -u | sed 's/^/-I /' | tr '\n' ' '`

# get all C files in the given path
SOURCES=`find . | grep '\.c$' | tr '\n' ' '`

frama-c -cpp-extra-args="$HEADERS" $SOURCES
