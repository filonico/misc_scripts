#!/bin/bash

# $1 = directory you want to tar gzip

if [ "${1: -1}" == "/" ]
then
	OUTNAME="${1::-1}".tar.gz
else
	OUTNAME="$1".tar.gz
fi

tar -cvf - "$1" | gzip -v -9 - > $OUTNAME && rm -rf "$1"
