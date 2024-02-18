#!/bin/bash
# Run emulator script
# Author: Max.Chiu

DEVICE=""
if [ ! "$1" == "" ]
then
  echo echo "DEVICE:$1"
  DEVICE="-s $1"
fi

# 打开设置
adb $DEVICE shell input tap 50 50
adb $DEVICE shell input tap 990 570
adb $DEVICE shell input tap 700 380
# 切换账号
adb $DEVICE shell input tap 640 680
# 同意隐私
adb $DEVICE shell input tap 125 140
# 输入手机
adb $DEVICE shell input tap 125 100
adb $DEVICE shell input text 15220039797
adb $DEVICE shell input tap 640 200
# 输入验证码
adb $DEVICE shell input tap 125 140
adb $DEVICE shell input text 15220039797
adb $DEVICE shell input tap 640 200