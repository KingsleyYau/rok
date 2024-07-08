#!/bin/bash
# Rok Ranking script
# Author: Max.Chiu

function Clean() {
  SELF_PID=$$
  ROK_PID=`ps -ef | grep "python -u main.py --device_name dt --api true --run_type ranking" | grep -v grep | awk '{print $2}'`
  echo "$SELF_PID Clean"
  if [ ! "$ROK_PID" == "" ];then
    echo "$SELF_PID kill $ROK_PID"
    kill -9 $ROK_PID
  fi
  #ps -ef | grep "python -u main.py --api true" | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
}
trap 'Clean; exit' SIGTERM SIGQUIT

echo "Start rok ranking script"
source /root/miniconda2/bin/activate rok && cd /root/Max/project/rok && python -u main.py --device_name xj --api true --run_type ranking