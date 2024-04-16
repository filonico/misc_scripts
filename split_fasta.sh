#!/bin/bash

# $1 = fasta file
# $2 = number of sequences for each file

FILENAME="${1%.*}"
EXTENSION="${1##*.}"

awk -v filename="$FILENAME" -v extension="$EXTENSION" -v no_seqs="$2" '
    BEGIN { n_seq=0; }
    {
        if (n_seq % no_seqs == 0) {
            file = sprintf("%s_%d.%s", filename, n_seq, extension);
        }
        print >> file;
        n_seq++;
        next;
    }
    {
        print >> file;
    }
' < $1
