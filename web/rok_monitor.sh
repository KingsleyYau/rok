#!/bin/bash
# Rok Monitor script
# Author: Max.Chiu

function Clean() {
  SELF_PID=$$
  ROK_PID=`ps -ef | grep "python -u main.py --api_monitor true" | grep -v grep | awk '{print $2}'`
  echo "$SELF_PID Clean"
  if [ ! "$ROK_PID" == "" ];then
    echo "$SELF_PID kill $ROK_PID"
    kill -9 $ROK_PID
  fi
  #ps -ef | grep "python -u main.py --api true" | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
}
trap 'Clean; exit' SIGTERM SIGQUIT

echo "Start rok title script"
source /root/miniconda2/bin/activate rok && cd /root/Max/project/rok && python -u main.py --api_monitor true --api_monitor_file /root/Max/project/rok/web/monitor_file.json --device_name dt