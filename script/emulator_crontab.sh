#!/bin/bash
# Restart emulator script
# Author: Max.Chiu

. /etc/profile 
. ~/.bash_profile 

ps -ef | grep "ncat -c" | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {}
sleep 10
nohup ncat -c "ncat 127.0.0.1 5555" -4 -l 9999 --keep-open >/dev/null 2>&1 &

ps -ef | grep qemu-system-x86 | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
sleep 30
nohup /root/project/android/script/emulator.sh 2>&1 &