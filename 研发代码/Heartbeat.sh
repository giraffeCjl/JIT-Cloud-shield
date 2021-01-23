#!/usr/bin/sh
. /etc/profile
. ~/.bash_profile
while (true)
do
touch /home/ELK/ELK/nginxlog/predictdata/readfile /home/ELK/ELK/nginxlog/predictdata/heartbeat.log
a=`cat /home/ELK/ELK/nginxlog/predictdata/readfile`
skip=$a
#从上一次读取的地方开始复制到新文件
dd if=/home/ELK/ELK/nginxlog/predictdata/access.log of=/home/ELK/ELK/nginxlog/predictdata/heartbeat.log bs=1 skip=$skip
#获取新增加内容的字节数  
a1=`wc -c /home/ELK/ELK/nginxlog/predictdata/heartbeat.log | awk '{print $1}'`
#获取总共需要skip 的字节数  
sum=`expr $a + $a1`
#记录到偏移量文件中，供下次读取  
echo $sum>/home/ELK/ELK/nginxlog/predictdata/readfile
cat /home/ELK/ELK/nginxlog/predictdata/heartbeat.log >> /home/ELK/ELK/nginxlog/predictdata/test.log
echo "predict" 
/root/anaconda3/bin/python3 /home/ELK/ELK/nginxlog/predictdata/predict.py >> /root/Desktop/cjl.log
echo "predict"
bash /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackresult.sh
sleep 1m
done
