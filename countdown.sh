#!/bin/bash

# This is a test script to run with oled.py running 
echo -ne "Counter" > /dev/shm/line1

secs=$((60))
while [ $secs -gt 0 ]; do
   # Writing in a RAM file
   echo -ne "$secs" > /dev/shm/line2
   sleep 1
   : $((secs--))
done

echo "cls" > /dev/shm/output