#!/bin/bash
# Run emulator script
# Author: Max.Chiu

./emulator/emulator -avd android30 -noaudio -no-boot-anim -gpu off -no-window -http-proxy http://192.168.88.140:1080

DEVICE=""
if [ ! "$1" == "" ]
then
  echo echo "DEVICE:$1"
  DEVICE="-s $1"
fi

#settings put global http_proxy 192.168.88.140:1080  
# 端口转发
ncat -c "ncat 127.0.0.1 5555" -l 9999 --keep-open
# 打开网页
adb shell am start -a android.intent.action.VIEW -d http://www.baidu.com
adb shell input tap 640 640
adb shell input tap 400 640


# 同意隐私
adb shell input tap 750 630
# QQ登录
adb shell input tap 660 270
# 同意其他登录
adb shell input tap 760 400
# 再次QQ登录
adb shell input tap 660 270

# QQ界面
# 同意QQ隐私
adb shell input tap 420 780
# QQ主界面登录
adb shell input tap 500 1180
# QQ扫码登录
adb shell input tap 250 1120

# 手机登录
# 同意隐私
adb shell input tap 680 640
# 输入手机
adb shell input tap 125 100
adb shell input text 15220039797
adb shell input tap 640 200
# 同意隐私1
adb shell input tap 125 140
# 同意隐私2
adb shell input tap 660 420

# 输入验证码
adb shell input tap 125 140
adb shell input text 462796
adb shell input tap 640 200


# ROK出错确定
adb shell input tap 640 450
# ROK踢出确定
adb shell input tap 640 500

# 设置
adb shell input tap 50 50
adb shell input tap 990 570
adb shell input tap 700 380
# 切换账号
adb shell input tap 640 680