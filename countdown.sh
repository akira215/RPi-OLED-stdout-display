#!/bin/bash

# This is a test script to run with oled.py running 

echo -ne "Counter" > /tmp/oled-display/line1

echo -ne "timer" > /tmp/oled-display/line2

exit

secs=$((60))
while [ $secs -gt 0 ]; do
   # Writing in a RAM file
   echo -ne "$secs" > /tmp/oled-display/line2
   sleep 1
   : $((secs--))
done

echo "cls" > /tmp/oled-display/line2