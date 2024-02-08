#!/bin/bash
# Run emulator script
# Author: Max.Chiu

FILE=/sdcard/rok.jpg
adb shell rm -f $FILE
adb shell screencap -p $FILE
adb pull $FILE
adb shell rm -f $FILE