#!/bin/sh
date=$(date -d "now" +%Y-%m-%d)
cat /home/ELK/ELK/nginxlog/predictdata/result-2018-04-11-20-30/*_0|awk -F " " '{print $3}' >> /home/ELK/ELK/result/ips.log
cat /home/ELK/ELK/nginxlog/predictdata/result-2018-04-11-20-30/*_2|awk -F " " '{print $3}' >> /home/ELK/ELK/result/ips.log
cat /home/ELK/ELK/nginxlog/predictdata/result-2018-04-11-20-30/*_3|awk -F " " '{print $3}' >> /home/ELK/ELK/result/ips.log
cat /home/ELK/ELK/nginxlog/predictdata/result-2018-04-11-20-30/*_4|awk -F " " '{print $3}' >> /home/ELK/ELK/result/ips.log
cat /home/ELK/ELK/result/ips.log | sort | uniq -c | sort -nr>> /home/ELK/ELK/result/ip_uniq.log
cat /home/ELK/ELK/result/ip_uniq.log | sort -k1 -nr >> /home/ELK/ELK/result/blacklist.log
grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' /home/ELK/ELK/result/blacklist.log | awk '{print "ipset add blacklist",$0}'|sh
iptables -I INPUT -m set --match-set blacklist src -p tcp --destination-port 2417 -j DROP
