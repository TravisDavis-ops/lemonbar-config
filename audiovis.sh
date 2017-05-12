#!/bin/bash

dir=$(dirname $0)

termite -t audiovis-popup -c $dir/termite_config -e ./$dir/spectrum-analyzer/main &
