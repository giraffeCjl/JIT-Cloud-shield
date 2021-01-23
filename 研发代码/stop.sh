source_log_path=/home/ELK/ELK/nginxlog/predictdata
dest_log_path=/home/ELK/ELK/nginxlog/predictdata
yesterday=$(date -d "1 days ago" +%Y%m%d)
code=$(jps | grep -i "Main" | awk '{print $1}')
kill -9 $code
#mv ${source_log_path}/access.log ${dest_log_path}/nginx_access_${yesterday}.log


