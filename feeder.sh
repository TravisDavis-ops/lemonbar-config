#!/bin/bash

dir=$(dirname $0)

while true
do
	dispStr=$(python $dir/feeder.py)

	echo "$dispStr"
	sleep 0.1 
done
