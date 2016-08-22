#!/bin/bash

while true
do
	dispStr=$(python feeder.py)

	echo "$dispStr"
	sleep 0.1 
done
