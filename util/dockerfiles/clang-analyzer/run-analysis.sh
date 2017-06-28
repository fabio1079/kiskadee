#!/bin/sh

cd $1

if [ -f configure ]; then
  scan-build ./configure
fi

if [ -f Makefile -o -f makefile ]; then
  scan-build make
fi
