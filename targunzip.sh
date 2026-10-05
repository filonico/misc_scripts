#!/bin/bash

# Usage: targunzip.sh file.tar.gz
# Extracts the archive into its own directory, then deletes the archive
# only if extraction succeeded.

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file.tar.gz>" >&2
    exit 1
fi

archive="$1"

if [ ! -f "$archive" ]; then
    echo "Error: '$archive' is not a file or does not exist." >&2
    exit 1
fi

dest="$(dirname -- "$archive")"

if tar -xvzf "$archive" -C "$dest"; then
    rm -f -- "$archive"
else
    echo "Error: extraction failed, '$archive' was not deleted." >&2
    exit 1
fi
