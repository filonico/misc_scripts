#!/bin/bash

# $1 = tar.gz file you want to tar gunzip

tar -xvzf "$1" "$(dirname $1)" && rm -rf $1
