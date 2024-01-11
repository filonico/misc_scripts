#!/bin/bash

# $1 = fasta file to onelinerize

FILENAME="${1%.*}"
FILEEXTENSION="${1##*.}"

awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' $1 | tail -n +2 > "$FILENAME".ol."$FILEEXTENSION"
