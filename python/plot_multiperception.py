      
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time
import math
import datetime
import os
import collections
import argparse
import glob
import numpy as np

# I20230801 11:26:00.038748 11866 multiperception.cc:665] [PerceptionPerf Model:RunSync] RunSync time cost: 80 ms
# I20230603 11:47:20.634276  2284 multiperception.cc:610] [PerceptionPerf Model:RunSync] RunSync cost: 165 ms
# grep RunSync
def get_lines(file_name, patterns):
     lg={}
     with open(file_name, 'r') as f:
        lines = f.readlines()

        for pat in patterns:
            logs = [line for line in lines if pat in line]
            lg[pat] = logs
     return lg

# return a tuple of (stamp, cost), the stamp is unix timestamp seconds as float
def parse_runsync(lines):
    costs=[]
    for line in lines:
        sp = line.split()
        if len(sp) != 11:
            continue

        cost=int(sp[9])

        if cost < 0:
            raise Exception("cost < 0")
        
        log_date = sp[0]
        log_time = sp[1]

        # date time string to unix timestamp seconds
        stamp=time.mktime(time.strptime(log_date+" "+log_time, "I%Y%m%d %H:%M:%S.%f"))

        costs.append((stamp, cost))

    return costs
        

def parse_log(file_name):
    patterns = ["RunSync"]
    lg = get_lines(file_name, patterns)
    costs = parse_runsync(lg["RunSync"])
    
    # get the top 10% cost
    spends = [x[1] for x in costs]
    # to numpy array
    spends = np.array(spends)

    # get the top 90% cost
    spends_90 = np.percentile(spends, 90)
    # get the top 95% cost
    spends_95 = np.percentile(spends, 95)
    # descending order
    # spends.sort(reverse=True)

    # get the average cost in the spends_90
    spends_90_avg = np.mean(spends[spends > spends_90])
    spends_95_avg = np.mean(spends[spends > spends_95])
    # get the full average cost in the spends
    spends_avg = np.mean(spends)

    log_base=os.path.basename(file_name)
    print("---------------------------------------------------")
    print("[INFO][PROCESS]: process file: ", log_base)
    print("max: {} ms, min: {} ms, top_95: {:.1f} ms, top_90 ms: {:.1f}, means: {:.1f}".format(np.max(spends), np.min(spends), spends_95, spends_90, spends_avg))
    print("---------------------------------------------------")


argparser = argparse.ArgumentParser(description='parse multiperception log')
argparser.add_argument('-i', dest='input_file', type=str, help='log file name', default="/Users/fengguoqing/Documents/code/personal_tools/python/krider_multiperception_car.log")


if __name__ == "__main__":
    args = argparser.parse_args()
    if args.input_file is None:
        print("log file name is None")
        sys.exit(1)

    parse_log(args.input_file)

    