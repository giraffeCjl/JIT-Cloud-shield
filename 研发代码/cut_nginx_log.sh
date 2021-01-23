#!/bin/sh
source_log_path=/home/ELK/ELK/nginxlog/predictdata
dest_log_path=/home/ELK/ELK/nginxlog/predictdata
beforeyesterday=$(date -d "2 days ago" +%Y%m%d)
yesterday=$(date -d "1 days ago" +%Y%m%d)
find /home/ELK/ELK/nginxlog/predictdata/ -type f -name "*.log" -exec rm -rf "${dest_log_path}/nginx_access_${beforeyesterday}.log" \;
mv ${source_log_path}/access.log /home/ELK/ELK/nginxlog/nginx_access_${yesterday}.log
mv /home/ELK/ELK/nginxlog/nginx_access_${yesterday}.log ${dest_log_path}/nginx_access_${yesterday}.log
