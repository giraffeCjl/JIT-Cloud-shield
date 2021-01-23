#!/bin/bash
time=$(date "+%Y-%m-%d %H:%M:%S")
grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' /home/ELK/ELK/result/blacklist.log | awk '{print "ipset add blacklist",$0}'|sh
iptables -I INPUT -m set --match-set blacklist src -p tcp --destination-port 2417 -j DROP
echo "Banned the following IP addresses on $time"|mail -a /home/ELK/ELK/result/blacklist.log -v -s "Warning Message" -r chenjiale1997627@126.com 1359698758@qq.com
