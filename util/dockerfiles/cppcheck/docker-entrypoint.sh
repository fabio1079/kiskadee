#!/bin/bash

useradd -ms /bin/bash kiskadee -u $KISKADEE_UID
chown -R kiskadee:kiskadee /src
chmod -R 755 /src
cd /src
cppcheck --enable=all --xml-version=2 --quiet .
