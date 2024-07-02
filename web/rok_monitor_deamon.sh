#!/bin/bash
# Rok deamon script
# Author: Max.Chiu

ps -ef | grep rok_monitor.sh | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
ps -ef | grep "python -u main.py --api_monitor true" | grep -v grep | awk '{print $2}'| xargs -I {} kill {}
sleep 10
nohup /root/Max/project/rok/web/rok_monitor.sh > /root/Max/project/rok/web/rok_monitor.log 2>&1 &