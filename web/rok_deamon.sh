#!/bin/bash
# Rok deamon script
# Author: Max.Chiu

ps -ef | grep rok.sh | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {}
sleep 10
#nohup /root/Max/project/rok/web/rok.sh > /root/Max/project/rok/web/rok.log 2>&1 &
nohup /root/Max/project/rok/web/rok_api.sh > /root/Max/project/rok/web/rok.log 2>&1 &