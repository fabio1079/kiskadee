#!/bin/sh

# get all header files in the given path
HEADERS=`find $1 | grep '\.h$' | sed 's/\/[^/]\+\.h$//' | sort -u | sed 's/^/-I /' | tr '\n' ' '`

# get all C files in the given path
SOURCES=`find $1 | grep '\.c$' | tr '\n' ' '`

frama-c -cpp-extra-args="$HEADERS" $SOURCES
