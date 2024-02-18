#!/bin/bash
# Run emulator script
# Author: Max.Chiu

DEVICE=""
if [ ! "$1" == "" ]
then
  echo "DEVICE:$1"
  DEVICE="-s $1"
fi

adb $DEVICE shell am force-stop com.lilithgames.rok.offical.cn
adb $DEVICE shell am start -n com.lilithgames.rok.offical.cn/com.harry.engine.MainActivity