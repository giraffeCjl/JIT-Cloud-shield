#!/bin/sh
touch /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/Readfile
touch /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/addresult
touch /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log
a=`cat /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/Readfile`
skip=${a}
dd if=/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/result.log of=/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/addresult bs=1 skip=${skip}
a1=`wc -c /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/addresult | awk '{print $1}'`
sum=`expr $a + $a1`
echo $sum > /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/Readfile
cat /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/addresult | while read line
do
	#echo "${line}"
	array=($line)
	array8="${array[8]#*[}"
	array12="${array[12]%]*}"
	if [ $array8 \> ${array[9]} ]
	then
		echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log
	elif [ ${array[10]} \> ${array[9]} ]
	then
		echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log
	elif [ ${array[11]} \> ${array[9]} ]
	then
		echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log
	elif [ $array12 \> ${array[9]} ]
	then
		echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log
	fi
done
if test -s /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log; then
       bash /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/classification.sh 
       bash /home/ELK/ELK/intercept.sh
fi
