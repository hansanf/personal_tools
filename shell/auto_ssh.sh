#!/bin/bash  
HOST_INFO=user_info.txt  
# HOST_INFO=("nvidia_12 10.31.1.12 nvidia nvidia 22")
# HOST_INFO=("${HOST_INFO[@]}" nvidia_71 10.31.1.71 nvidia nvidia 22)

# for ip in $(awk '{print $2}' $HOST_INFO) 
# do  
#     user=$(awk -v I="$ip" 'I==$2{print $3}' $HOST_INFO) #if I==$2 打印$3
#     pass=$(awk -v I="$ip" 'I==$2{print $4}' $HOST_INFO)  
#     expect login.exp $ip $user $pass $1  
# done  

# 通过host_name 找到对应的ip user passwd port 那一行的内容
function find_item()
{
  dst_host_name=$1
  for host_name in $(awk '{print $1}' $HOST_INFO); do
    # 通过 host_name获取其所在行的所有内容
    line_content=$(awk -v I="$host_name" 'I==$1{print $0}' $HOST_INFO)
    if [[ $dst_host_name == $host_name ]]; then
      echo "$line_content"
    fi
  done
}

dst_item=$(find_item "nvidia_12")
ip=$(echo $dst_item | awk '{print $2}')
user=$(echo $dst_item | awk '{print $3}')
passwd=$(echo $dst_item | awk '{print $4}')
port=$(echo $dst_item | awk '{print $5}')

echo "ip=$ip"
echo "user=$user"
echo "passwd=$passwd"
echo "port=$port"

expect login.exp $ip $user $passwd $port
