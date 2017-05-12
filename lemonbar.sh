#!/bin/bash

# Colors
# First two digits contrl transparency
BG_COLOR='#E6002b36'
# BG_COLOR='#002b36'
FG_COLOR='#839496'

dir=$(dirname $0)

bash $dir/feeder.sh | lemonbar -g 1920x25+0+0 -p -f Nexa-10 -f FontAwesome-10 -F$FG_COLOR -B$BG_COLOR 
