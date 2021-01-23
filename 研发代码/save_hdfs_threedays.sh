#!/bin/sh
JAVA_HOME=/root/Desktop/jdk1.8.0_152
CLASSPATH=.:$JAVA_HOME/lib.tools.jar
PATH=$JAVA_HOME/bin:$PATH
export JAVA_HOME CLASSPATH PATH
export HADOOP_HOME=/home/ELK/ELK/hadoop
export PATH=${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:$PATH
date1=$(date -d -3day +%Y-%m-%d)
i=0
arrays=$(hadoop fs -ls /user/logstash/ | awk -F ' ' '{print $8}')
for version in ${arrays[*]}
do
a=$version
b=${a##*=}
if [ "$b" \< "$date1" ];
then
old_version[$i]=$version
i=$i+1
fi
done
for verse in ${old_version[@]}
do
  hadoop fs -rmr $verse
done
