#!/bin/bash
OLD_IFS="$IFS"
IFS=" "
label1="0 1 0 0 0"
label2="0 0 1 0 0"
label3="1 0 0 0 0"
label4="0 0 0 0 1"
label5="0 0 0 1 0"
cat general.log hitlibrary.log blasting.log general.log slowlinks.log | awk 'BEGIN{srand()}{b[rand()NR]=$0}END{for(x in b)print b[x]}' | while read line
do
	
	array=($line)
	IFS="$OLD_IFS"
	time=${array[0]}
	stamp=${array[1]}
	timestamp=$time" "$stamp
	ip=${array[2]}
	cookie=${array[3]}
	request_completion=${array[4]}  #ok
	status=${array[5]} #404
	request_time=${array[6]} #0.003
	body_bytes_sent=${array[7]} #4429



# guan yu 4429
	str=$body_bytes_sent
	sum=0
	index=0
	length=${#str}
	
	while [ ${index} -lt ${length} ]
	do
		let sum=10*sum+${str:$index:1}
		let index+=1
	done
#guan yu time
	st=$request_time
	su=0
	in=0
	le=${#st}

	while [ ${in} -lt ${le} ]
	do
	let su=10*su+${st:$in:1}>>/dev/null 2>&1
	let in+=1
	done

tip="\"\""

if [ "$su" -gt 30000 ];then
label=$label2  #man lian jie
elif [ "$su" -gt 1000 ];then
label=$label3 #DDOS
elif [ "$sum" = "4429" ];then
label=$label4
elif [ "$cookie" = "$tip" ];then
label=$label5
else label=$label1
fi



echo $timestamp $ip $cookie $request_completion $status $request_time $body_bytes_sent $label >> test_data.txt
done
