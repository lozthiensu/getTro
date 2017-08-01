now=$(date +"%T")
logFile="logGroup.txt"
echo "Start at : $now" >> $logFile
python3 /Users/Kakalot/stkt/getFB/main.py >> $logFile
now=$(date +"%T")
echo "End at : $now" >> $logFile
echo " " >> $logFile
echo " " >> $logFile
