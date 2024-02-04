#!/bin/bash
# Rok Title script
# Author: Max.Chiu

RECROD_FILE=record.txt

echo "Start rok title script"
while true; do
	while read LINE; do
	  echo "####################################################################"
	  server=`echo $LINE | jq -r '.server'`
	  x=`echo $LINE | jq -r '.x'`
	  y=`echo $LINE | jq -r '.y'`
	  title=`echo $LINE | jq -r '.title'`
		
	  source /root/miniconda2/bin/activate rok && cd /root/Max/project/rok && python main.py --api true --server $server --x $x --y $y --title $title
	  sed -i '1,1d' $RECROD_FILE
	  break
	done < $RECROD_FILE
	sleep 1
done