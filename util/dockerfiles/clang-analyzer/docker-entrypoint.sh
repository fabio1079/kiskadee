#!/bin/bash

useradd -ms /bin/bash kiskadee -u $KISKADEE_UID
chown -R kiskadee:kiskadee /src
chmod -R 755 /src
cd /src

cd $1

if [ -f configure ]; then
  scan-build ./configure
fi

if [ -f Makefile -o -f makefile ]; then
  scan-build make
fi
