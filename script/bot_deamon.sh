#!/bin/bash
# Rok bot deamon script
# Author: Max.Chiu

ps -ef | grep "python main.py --api true --run_type request_bot" | grep -v grep | awk '{print $2}'| xargs -I {} kill {}
sleep 10
nohup /root/Max/project/rok/script/bot.sh > /root/Max/project/rok/script/bot.log 2>&1 &