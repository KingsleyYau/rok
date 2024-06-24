#!/bin/bash
# Rok Title script
# Author: Max.Chiu

RECROD_FILE=/root/Max/project/rok/web/record.txt

function Clean() {
  SELF_PID=$$
  ROK_PID=`ps -ef | grep "python -u main.py --api_deamon true" | grep -v grep | awk '{print $2}'`
  echo "$SELF_PID Clean"
  if [ ! "$ROK_PID" == "" ];then
    echo "$SELF_PID kill $ROK_PID"
    kill -9 $ROK_PID
  fi
  #ps -ef | grep "python -u main.py --api true" | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
}
trap 'Clean; exit' SIGTERM SIGQUIT

echo "Start rok title script"
source /root/miniconda2/bin/activate rok && cd /root/Max/project/rok && python -u main.py --api_deamon true --api_deamon_file /root/Max/project/rok/web/record.txt --api_deamon_file_last /root/Max/project/rok/web/record_last.txt