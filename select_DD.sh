#!/usr/bin/env bash

# Function made to reject phases whose weight is less than a user given arg

# Parse argument

input_file=$1
weight_lim=$2

# Process

awk -v weight=$weight_lim '{
if (NF==4 && $3<=weight)
	next
else
	print $0
}' $input_file
