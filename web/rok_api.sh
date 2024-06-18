#!/bin/bash
# Rok Title script
# Author: Max.Chiu

RECROD_FILE=/root/Max/project/rok/web/record.txt

function Clean() {
  SELF_PID=$$
  ROK_PID=`ps -ef | grep "python -u main.py --api_deamon true" | grep -v grep | awk '{if($1~/[0-9]+/) print $2}'`
  echo "$SELF_PID Clean"
  if [ ! "$ROK_PID" == "" ];then
    echo "$SELF_PID kill $ROK_PID"
  fi
  #ps -ef | grep "python -u main.py --api true" | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
}
trap 'Clean; exit' SIGTERM

echo "Start rok title script"
source /root/miniconda2/bin/activate rok && cd /root/Max/project/rok && python -u main.py --api_deamon true --api_deamon_file /root/Max/project/rok/web/record.txt