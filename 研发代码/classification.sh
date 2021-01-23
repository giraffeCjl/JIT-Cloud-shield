#!/bin/sh
cat /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log | while read line
do
        #echo "${line}"
        array=($line)
        array8="${array[8]#*[}"
        array12="${array[12]%]*}"
        if [ $array8 \> ${array[9]} ] && [ $array8 \> ${array[10]} ] && [ $array8 \> ${array[11]} ] && [ $array8 \> $array12 ]
        then
                echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/ddos.log
        elif [ ${array[10]} \> $array8 ] && [ ${array[10]} \> ${array[9]} ] && [ ${array[10]} \> ${array[11]} ] && [ ${array[10]} \> $array12 ]
        then
                echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/slowlinks.log
        elif [ ${array[11]} \> $array8 ] && [ ${array[11]} \> ${array[9]} ] && [ ${array[11]} \> ${array[10]} ] && [ ${array[11]} \> $array12 ]
        then
                echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/blasting.log
        elif [ $array12 \> $array8 ] && [ $array12 \> ${array[9]} ] && [ $array12 \> ${array[10]} ] && [ $array12 \> ${array[11]} ]
        then
                echo "${line}" >>/home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/hitlibrary.log
        fi
done

