#!/bin/bash
# Restart emulator script
# Author: Max.Chiu

. /etc/profile 
. ~/.bash_profile 

ps -ef | grep qemu-system-x86 | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
sleep 30
nohup /root/project/android/script/emulator.sh 2>&1 &