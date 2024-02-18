#!/bin/bash
# Run emulator script
# Author: Max.Chiu

DEVICE=""
if [ ! "$1" == "" ]
then
  echo "DEVICE:$1"
  DEVICE="-s $1"
fi

FILE=/sdcard/rok.jpg
adb $DEVICE shell rm -f $FILE
adb $DEVICE shell screencap -p $FILE
adb $DEVICE pull $FILE
adb $DEVICE shell rm -f $FILE