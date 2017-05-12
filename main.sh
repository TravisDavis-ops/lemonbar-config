#!/bin/sh

dir=$(dirname $0)
bash $dir/lemonbar.sh | bash button_handler.sh
