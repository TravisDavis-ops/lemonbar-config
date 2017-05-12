#!/bin/bash

top -bn 2 -d 0.01 | grep '^%Cpu' | tail -n 8 | awk '{print $4}' | sed 's/\[.*$//'
