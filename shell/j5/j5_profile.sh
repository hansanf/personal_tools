#!/usr/bin/bash

nohup bash bpu_profile.sh >/dev/null &
bpu_pid=$!
nohup bash ddr_profile.sh >/dev/null &
ddr_pid=$!
nohup bash cpu_profile.sh >/dev/null &
cpu_pid=$!

sleep 1
echo "${bpu_pid} ${ddr_pid} ${cpu_pid}"
kill -9 ${bpu_pid} ${ddr_pid} ${cpu_pid}