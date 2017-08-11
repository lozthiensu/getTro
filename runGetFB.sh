now=$(date +"%T")
logFile="logRun.txt"
echo "Start at : $now" >> $logFile
python3.6 main.py >> $logFile
now=$(date +"%T")
echo "End at : $now" >> $logFile
echo " " >> $logFile
echo " " >> $logFile
