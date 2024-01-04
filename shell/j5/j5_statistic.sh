#!/usr/bin/bash

multiperception_log="krider_multiperception_car.INFO"
bpu_log="bpu.log"
cpu_log="cpu.log"
ddr_log="ddr.log"

# 感知 alog cost 统计
min=$(cat ${multiperception_log} |grep Algo |grep cost | awk '{print $9}'|sort -n |head -n 1)
max=$(cat ${multiperception_log} |grep Algo |grep cost | awk '{print $9}'|sort -n |tail -n 1)
avg=$(cat ${multiperception_log} |grep Algo |grep cost | awk '{sum += $9} END {avg = sum / NR; print avg}')
echo "algo cost:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}" 

# 感知 alog fps 统计
min=$(cat ${multiperception_log} |grep Algo |grep fps | awk '{print $10}'|sort -n |head -n 1)
max=$(cat ${multiperception_log} |grep Algo |grep fps | awk '{print $10}'|sort -n |tail -n 1)
avg=$(cat ${multiperception_log} |grep Algo |grep fps | awk '{sum += $10} END {avg = sum / NR; print avg}')
echo "algo fps:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}" 

################### bpu ######################
min=$(cat ${bpu_log} |grep BPU -A 1 |grep 0| awk '{print $2}'|sort -n |head -n 1)
max=$(cat ${bpu_log} |grep BPU -A 1 |grep 0| awk '{print $2}'|sort -n |tail -n 1)
avg=$(cat ${bpu_log} |grep BPU -A 1 |grep 0| awk '{sum += $2} END {avg = sum / NR; print avg}')
echo "bpu core 0:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"

min=$(cat ${bpu_log} |grep BPU -B 1 |grep 1| awk '{print $2}'|sort -n |head -n 1)
max=$(cat ${bpu_log} |grep BPU -B 1 |grep 1| awk '{print $2}'|sort -n |tail -n 1)
avg=$(cat ${bpu_log} |grep BPU -B 1 |grep 1| awk '{sum += $2} END {avg = sum / NR; print avg}')
echo "bpu core 1:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"

################### ddr ######################
min=$(cat ${ddr_log} |grep "Read"| awk '{print $5}' | sort -n | head -n 1)
max=$(cat ${ddr_log} |grep "Read"| awk '{print $5}' | sort -n | tail -n 1)
avg=$(cat ${ddr_log} |grep "Read"| awk '{sum += $5} END {avg = sum / NR; print avg}')
echo "bpu ddr read bandwidth:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"

min=$(cat ${ddr_log} |grep "Write"| awk '{print $5}' | sort -n | head -n 1)
max=$(cat ${ddr_log} |grep "Write"| awk '{print $5}' | sort -n | tail -n 1)
avg=$(cat ${ddr_log} |grep "Write"| awk '{sum += $5} END {avg = sum / NR; print avg}')
echo "bpu ddr write bandwidth:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"

min=$(cat ${ddr_log} |grep "Read"| awk '{print $3}' | sort -n | head -n 1)
max=$(cat ${ddr_log} |grep "Read"| awk '{print $3}' | sort -n | tail -n 1)
avg=$(cat ${ddr_log} |grep "Read"| awk '{sum += $3} END {avg = sum / NR; print avg}')
echo "cpu ddr read bandwidth:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"

min=$(cat ${ddr_log} |grep "Write"| awk '{print $3}' | sort -n | head -n 1)
max=$(cat ${ddr_log} |grep "Write"| awk '{print $3}' | sort -n | tail -n 1)
avg=$(cat ${ddr_log} |grep "Write"| awk '{sum += $3} END {avg = sum / NR; print avg}')
echo "cpu ddr write bandwidth:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"

################### cpu ######################
min=$(cat ${cpu_log} |grep "krider_multiperception_main_car"| awk '{print $7}' | sort -n | head -n 1)
max=$(cat ${cpu_log} |grep "krider_multiperception_main_car"| awk '{print $7}' | sort -n | tail -n 1)
avg=$(cat ${cpu_log} |grep "krider_multiperception_main_car"| awk '{sum += $7} END {avg = sum / NR; print avg}')
echo "cpu utilization:"
echo "最小值: ${min}  最大值: ${max}  平均值: ${avg}"
