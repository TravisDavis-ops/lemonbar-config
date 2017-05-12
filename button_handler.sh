#!/bin/bash

dir=$(dirname "$0")
state="off"

while read -r data
do
	# Check if lemonbar output is vis_toggle
	if [[ $data == "vis_toggle" ]]
	then
		if [[ $state == "off" ]]
		then
			bash "$dir/audiovis.sh"
			state="on"
		else
			pid=$(ps aux | grep "termite.*spectrum-analyzer\/main" | awk '{print $2}')
			kill "$pid"
			state="off"
		fi	
	fi
done
