#!/usr/bin/env bash

input_file=$1
georef=$2

### Check if rays2txt exist

if ! type rays2txt.py > /dev/null 2>&1; then
	echo "Add rays2txt.y first in your .bashrc"
	exit
fi

### Transform .dat to .xyz file

rays2txt.py $1 $2 | awk '{if (length($0)>30) print $1,$2,$3}'
