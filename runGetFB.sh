#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/troNhanh/getTro
now=$(date +"%T")
logFile="logRun.txt"
echo "Start at : $now" >> $logFile
python3.6 /home/troNhanh/getTro/main.py >> $logFile
now=$(date +"%T")
echo "End at : $now" >> $logFile
echo " " >> $logFile
echo " " >> $logFile
