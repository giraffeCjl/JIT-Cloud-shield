#!/bin/sh
cat /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log|awk -F " " '{print $3}' >> /home/ELK/ELK/result/ips.log
cat /home/ELK/ELK/result/ips.log | sort | uniq -c | sort -nr>> /home/ELK/ELK/result/ip_uniq.log
cat /home/ELK/ELK/result/ip_uniq.log | sort -k1 -nr >> /home/ELK/ELK/result/blacklist.log
grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' /home/ELK/ELK/result/blacklist.log | awk '{print "ipset add blacklist",$0}'|sh
iptables -I INPUT -m set --match-set blacklist src -p tcp --destination-port 2417 -j DROP
rm -rf /home/ELK/ELK/nginxlog/predictdata/pre-result/resultlog/attackip.log
