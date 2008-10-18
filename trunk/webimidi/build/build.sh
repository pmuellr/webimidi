#!/bin/sh

VERSION="0.1"
INSTALLABLE=webimidi-$VERSION.tar.gz

rm $INSTALLABLE

cd ../..

tar -cvf webimidi/build/webimidi-0.1.tar.gz  \
   --exclude '*.pyc' \
   --exclude '*/.project' \
   --exclude '*/.pydevproject' \
   --exclude '*/.svn' \
   --exclude '*/build' \
   --exclude '*/test' \
   webimidi
 