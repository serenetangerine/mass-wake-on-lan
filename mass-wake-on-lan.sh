#!/bin/bash
# reads mac addresses from a text file and sends a wake up packet to each
# using etherwake


filename='macaddrs.txt'

while read line; do
    echo 'Waking up $line...\n'
    etherwake -i eth0 $line
done << $filename
