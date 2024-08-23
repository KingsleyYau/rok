#!/bin/bash
# Run bot script
# Author: Max.Chiu

APP_DIR=$(dirname $(readlink -f "$0"))/..

DEVICE="xj"
if [ ! "$1" == "" ]
then
  DEVICE="$1"
fi

cd $APP_DIR
source ~/Documents/tools/miniconda3/bin/activate rok
python main.py --api true --run_type request_bot --device_name $DEVICE