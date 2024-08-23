#!/bin/bash
# Run emulator script
# Author: Max.Chiu

APP_DIR=$(dirname $(readlink -f "$0"))/..

NAME=""
if [ ! "$1" == "" ]
then
  #echo "DEVICE:$1"
  NAME="$1"
fi


DEVICES_CONFIG=$APP_DIR/save/devices_config.json
IP=`cat "$DEVICES_CONFIG" | tr -d '\n' | jq --arg NAME "$NAME" -r -c '.[] | select(.name==$NAME) | .ip'`
PORT=`cat "$DEVICES_CONFIG" | tr -d '\n' | jq --arg NAME "$NAME" -r -c '.[] | select(.name==$NAME) | .port'`

DEVICE="-s $IP:$PORT"


FILE=/sdcard/screen.jpg
adb $DEVICE shell rm -f $FILE

CMD="adb $DEVICE shell screencap -p $FILE"
echo "$CMD"
$CMD

adb $DEVICE pull $FILE capture/$NAME.jpg
adb $DEVICE shell rm -f $FILE