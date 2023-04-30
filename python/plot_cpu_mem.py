#!/usr/bin/env python
#coding:utf-8
# 对 shell/ps_mem_cpu.sh 结果进行可视化
import numpy as np
import matplotlib.pyplot as plt
import datetime
import argparse

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_name", default="pid_stats_20057.txt", type=str, help='log name')
    parser.add_argument("--res_dir", default="./result/", type=str, help="restult dir")
    opt = parser.parse_args()
    return opt

opt = options()
log_name=opt.log_name
# Read the data from the file
with open(log_name, 'r') as f:
    lines = f.readlines()

# Parse the data into lists
timestamps = []
mem_usages = []
cpu_usages = []
for line in lines:
    parts = line.split()
    try:
      timestamp = datetime.datetime.strptime(parts[0] + ' ' + parts[1], '%Y-%m-%d %H:%M:%S')
      mem_usage = float(parts[4])
      cpu_usage = float(parts[8].rstrip('%'))
      timestamps.append(timestamp)
      mem_usages.append(mem_usage)
      cpu_usages.append(cpu_usage)
    except Exception as e :
      print(line)
      print(e)

# Calculate the percentiles
mem_50th = np.percentile(mem_usages, 50)
mem_90th = np.percentile(mem_usages, 90)
mem_99th = np.percentile(mem_usages, 99)
cpu_50th = np.percentile(cpu_usages, 50)
cpu_90th = np.percentile(cpu_usages, 90)
cpu_99th = np.percentile(cpu_usages, 99)

# Print the results
print(f'mem usage 50th percentile: {mem_50th:.2f} MB')
print(f'mem usage 90th percentile: {mem_90th:.2f} MB')
print(f'mem usage 99th percentile: {mem_99th:.2f} MB')
print(f'cpu usage 50th percentile: {cpu_50th:.2f} %')
print(f'cpu usage 90th percentile: {cpu_90th:.2f} %')
print(f'cpu usage 99th percentile: {cpu_99th:.2f} %')

# Plot the data
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time')
ax1.set_ylabel('Memory usage (MB)', color=color)
ax1.plot(timestamps, mem_usages, color=color, label="Memory")
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='lower left')
ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('CPU usage (%)', color=color)
ax2.plot(timestamps, cpu_usages, color=color, label="CPU")
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

fig.tight_layout()
# plt.show()
plt.savefig(opt.res_dir+"mem_cpu.jpg", bbox_inches='tight')


