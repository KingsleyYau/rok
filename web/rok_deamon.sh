#!/bin/bash
# Rok deamon script
# Author: Max.Chiu

ps -ef | grep rok_api.sh | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
ps -ef | grep "python -u main.py --api_deamon true" | grep -v grep | awk '{print $2}'| xargs -I {} kill {}
sleep 10
#nohup /root/Max/project/rok/web/rok.sh > /root/Max/project/rok/web/rok.log 2>&1 &
nohup /root/Max/project/rok/web/rok_api.sh > /root/Max/project/rok/web/rok.log 2>&1 &