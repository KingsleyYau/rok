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

# 角色
adb $DEVICE shell input tap 560 380
# 角色1
adb $DEVICE shell input tap 400 240
# 角色2
adb $DEVICE shell input tap 800 240
# 切换角色 确定
adb $DEVICE shell input tap 800 500

# 账号
adb $DEVICE shell input tap 700 380
# 切换账号
adb $DEVICE shell input tap 640 680

# 首次
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

# 切换
# 同意隐私
adb $DEVICE shell input tap 185 220
# 输入手机
adb $DEVICE shell input tap 185 140
adb $DEVICE shell input text 15220039797
adb $DEVICE shell input tap 640 300
# 输入验证码
adb $DEVICE shell input tap 185 220
adb $DEVICE shell input text 15220039797
adb $DEVICE shell input tap 640 300

###################################
# 封号界面,账号管理
adb $DEVICE shell input tap 800 460
