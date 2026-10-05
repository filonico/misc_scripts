#!/bin/bash

# Usage: tarzip.sh <directory>
# Creates <directory>.tar.gz whose top-level entry is the directory's own name,
# verifies it, then deletes the original directory.

set -o pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

dir="${1%/}"    # strip one trailing slash

if [ ! -d "$dir" ]; then
    echo "Error: '$dir' is not a directory." >&2
    exit 1
fi

parent="$(dirname -- "$dir")"
name="$(basename -- "$dir")"
outname="$dir.tar.gz"

if tar -cvf - -C "$parent" -- "$name" | gzip -v -9 > "$outname" \
   && tar -tzf "$outname" > /dev/null; then
    rm -rf -- "$dir"
else
    echo "Error: archive creation or verification failed; '$dir' was not deleted." >&2
    rm -f -- "$outname"
    exit 1
fi
