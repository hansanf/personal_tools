#!/bin/bash
# 统计指定进程的内存和cpu使用情况
# Replace <PID> with the actual PID you want to monitor
pid=$1

# Check if the PID exists
if ! ps -p $pid > /dev/null; then
  echo "PID $pid does not exist"
  exit 1
fi

# Loop to continuously monitor the memory and CPU usage
while true; do
  # Get the memory and CPU usage of the specified PID
  mem=$(ps -p $pid -o rss | tail -n 1)
  mem_mb=$(echo "scale=2; $mem/1024" | bc -l)
  cpu=$(ps -p $pid -o %cpu | tail -n 1)

  # Save the memory and CPU usage to a file
  echo "$(date +%Y-%m-%d\ %H:%M:%S) Memory usage: $mem_mb MB, CPU usage: $cpu%" >> pid_stats_${pid}.log

  # Check if the PID still exists
  if ! ps -p $pid > /dev/null; then
    echo "PID $pid no longer exists"
    exit 1
  fi

  # Wait for 0.5 seconds before checking again
  sleep 0.5
done
