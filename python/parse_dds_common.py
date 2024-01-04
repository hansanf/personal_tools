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

# version 3
# update : remove same frame with sync_timestamp
# update info: 20230720

# I20230603 11:47:15.460953 20896 control_subscriber.cc:682] [ControlRuntask:RunTask] cost = 58 ms
# grep [ControlRuntask:RunTask]
def get_lines(file_name, patterns):
     lg={}
     with open(file_name, 'r') as f:
        lines = f.readlines()

        for pat in patterns:
            logs = [line for line in lines if pat in line]
            lg[pat] = logs
     return lg

def get_one_pattern_lines(file_name, pattern):
     with open(file_name, 'r') as f:
        lines = f.readlines()

     logs = [line for line in lines if pattern in line]
     return logs

# return a tuple of (stamp, cost), the stamp is unix timestamp seconds as float
def parse_control_algo(lines):
    costs=[]
    for line in lines:
        sp = line.split()
        if len(sp) != 9:
            continue

        cost=int(sp[7])

        if cost < 0:
            raise Exception("cost < 0")
        
        log_date = sp[0]
        log_time = sp[1]

        # date time string to unix timestamp seconds
        stamp=time.mktime(time.strptime(log_date+" "+log_time, "I%Y%m%d %H:%M:%S.%f"))

        costs.append((stamp, cost))

    return costs

# return a tuple of (stamp, cost), the stamp is unix timestamp seconds as float
def parse_control_fps(lines):
    costs=[]
    for line in lines:
        sp = line.split()
        if len(sp) != 10:
            continue

        cost=float(sp[9])

        if cost < 0:
            raise Exception("fps < 0")
        
        log_date = sp[0]
        log_time = sp[1]

        # date time string to unix timestamp seconds
        stamp=time.mktime(time.strptime(log_date+" "+log_time, "I%Y%m%d %H:%M:%S.%f"))

        costs.append((stamp, cost))

    return costs

def print_cost(pattern, costs, level=0, printheader=False, isfps=False):
    spends = [x[1] for x in costs]
    if len(spends) <= 0:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return
    # to numpy array
    spends = np.array(spends)

    # get the top 90% cost
    spends_90 = np.percentile(spends, 90)
    # get the top 95% cost
    spends_95 = np.percentile(spends, 95)
    var = np.var(spends)
    # descending order
    # spends.sort(reverse=True)

    # get the average cost in the spends_90
    spends_90_avg = np.mean(spends[spends >= spends_90])
    spends_95_avg = np.mean(spends[spends >= spends_95])
    # get the full average cost in the spends
    
    spends_avg = np.mean(spends)

    if printheader:
       print("---------------------------------------------------")


    task_desp="[{}]".format(pattern)
    task_desp=task_desp.ljust(20)[0:20]
    # print(len(task_desp))

    if isfps:
        content="--MEANS: {:6.1f}fps 90th: {:6.1f}fps 95th: {:6.1f}fps MIN: {:6.1f}fps MAX: {:6.1f}fps VAR: {:6.1f} ITEMS: {}".format(spends_avg, spends_90,spends_95, np.min(spends), np.max(spends), var, len(spends))
    else:
        content="--MEANS: {:6.1f}ms  90th: {:6.1f}ms  95th: {:6.1f}ms  MIN: {:6.1f}ms  MAX: {:6.1f}ms  VAR: {:6.1f} ITEMS: {}".format(spends_avg, spends_90,spends_95, np.min(spends), np.max(spends), var, len(spends))
    while level > 0:
        task_desp = "  "+task_desp
        level -= 1

    print(task_desp, content)


# sub: [topic] [fps] [e2e-latency] [full-latency]
#        LOG(INFO) << latency_name << " frame ID: " << frame_id
#                  << " recv_timestamp_ms: " << recv_timestamp_ms
#                  << " sync_timestamp_ms: " << sync_timestamp_ms
#                  << " timestamp_ms: " << fast_done_time
#                  << " former dds latency: " << now - fast_done_time
#                  << " all former dds latency: " << now - sync_timestamp_ms
#                  << " former dds latency with algo cost: " << now - recv_timestamp_ms
#                  << " former algo cost: " << fast_done_time - recv_timestamp_ms;

# pub: [topic] [fps] [e2e-cost] [algo-cost] 
#      LOG(INFO) << latency_name << " frame ID: " << frame_id
#                                << " recv_timestamp_ms: " <<  recv_timestamp_ms
#                                << " sync_timestamp_ms: " << sync_timestamp_ms
#                                << " timestamp_ms: " << timestamp_ms
#                                << " e2e cost " << now - sync_timestamp_ms
#                                << " algo cost:  " << now - recv_timestamp_ms;

def find_lines(pattern, lines):
    logs = [line for line in lines if pattern in line]
    return logs

def find_pub_lines(lines):
    pattern = "<<<PUB>>>"
    return find_lines(pattern, lines)

def find_pub_e2e_cost_line(lines):
    pattern = "e2e cost"
    return find_lines(pattern, lines)

def pub_e2e_cost_line_by_topic_name(lines):
        groups = {}
        topic_idx = 9
        for line in lines:
            sp = line.split()
            if sp[7] == "Shm":
                topic_idx = 10
            else:
                topic_idx = 9
            
            topic = sp[topic_idx]
            # if the dir latency_userdata/mount_server[log_topic] not exist, create it
            if topic not in groups:
                groups[topic] = []

            # add to userdata/mount_server
            groups[topic].append(line)

        return groups

def pub_fps_by_topic_name(lines):
        groups = {}
        topic_idx = 6
        for line in lines:
            sp = line.split()
            topic = sp[topic_idx]
            # if the dir latency_userdata/mount_server[log_topic] not exist, create it
            if topic not in groups:
                groups[topic] = []

            # add to userdata/mount_server
            groups[topic].append(line)

        return groups

def parse_pub_fps_line(topic, lines):
    infos={}
    infos["fps"]=[]
    fpss=infos["fps"]
    sps_len = 20
    fps_idx = 13

    for line in lines:
        sp = line.split()
        if len(sp) != sps_len:
            continue
        
        log_date = sp[0]
        log_time = sp[1]
        fps = float(sp[fps_idx])

        # date time string to unix timestamp seconds
        stamp=time.mktime(time.strptime(log_date+" "+log_time, "I%Y%m%d %H:%M:%S.%f"))

        fpss.append((stamp, fps))

    return infos

def write_to_csv(filename, stamp_val, e2e_val):
    if os.path.exists(filename):
        strWrite = "";
    else:
        strWrite = "sync_time,e2e_cost\n";
        
    with open(filename, 'a') as file:
        strWrite += str(stamp_val) + "," + str(e2e_val) + "\n"
        file.write(strWrite)

def parse_pub_e2e_cost_line(topic, lines):
    infos={}
    infos["e2e_cost"]=[]
    infos["algo_cost"]=[]
    e2e_cost=infos["e2e_cost"]
    algo_cost=infos["algo_cost"]
    sps_len_dyn = 26
    sps_len_shm = 27
    e2e_cost_idx = 22
    algo_cost_idx = 25
    sync_stamp_idx = 17
    sync_userdata/mount_server = {}

    for line in lines:
        sp = line.split()
        if (len(sp) == sps_len_dyn):
            e2e_cost_idx_real = e2e_cost_idx
            algo_cost_idx_real = algo_cost_idx
            sync_stamp_idx_real = sync_stamp_idx
        elif (len(sp) == sps_len_shm) :
            e2e_cost_idx_real = e2e_cost_idx + 1
            algo_cost_idx_real = algo_cost_idx + 1
            sync_stamp_idx_real = sync_stamp_idx + 1
        else:
            continue

        log_date = sp[0]
        log_time = sp[1]
        sync_stamp = sp[sync_stamp_idx_real]
        if sync_stamp not in sync_userdata/mount_server:
            sync_userdata/mount_server[sync_stamp] = 1
            # print("sync_stamp", sync_stamp)
        else:
            continue

        e2e = int(sp[e2e_cost_idx_real])
        algo = int(sp[algo_cost_idx_real])

        # date time string to unix timestamp seconds
        stamp=time.mktime(time.strptime(log_date+" "+log_time, "I%Y%m%d %H:%M:%S.%f"))

        e2e_cost.append((stamp, e2e))
        algo_cost.append((stamp, algo))

        file_name = topic[:-1]
        write_to_csv(file_name + "_e2e_cost.csv", sync_stamp, e2e)

    return infos

def find_sub_lines(lines):
    pattern = "<<< SUB >>>"
    return find_lines(pattern, lines)


def find_sub_e2e_cost_line(lines):
    pattern = "e2e cost"
    return find_lines(pattern, lines)

def sub_e2e_cost_line_by_topic_name(lines):
        groups = {}
        topic_idx = 9
        for line in lines:
            sp = line.split()
            topic = sp[topic_idx]
            # if the dir latency_userdata/mount_server[log_topic] not exist, create it
            if topic not in groups:
                groups[topic] = []

            # add to userdata/mount_server
            groups[topic].append(line)


        print(groups.keys())
        return groups

def parse_sub_e2e_cost_line(topic, lines):
    infos={}
    infos["former dds latency"]=[]
    infos["all former dds latency"]=[]
    infos["former dds latency with algo cost"]=[]
    infos["former algo cost"]=[]
    former_dds_latency=infos["former dds latency"]
    all_former_dds_latency=infos["all former dds latency"]
    former_dds_latency_with_algo_cost=infos["former dds latency with algo cost"]
    former_algo_cost=infos["former algo cost"]
    sps_len = 39
    former_dds_latency_idx = 22
    all_former_dds_latency_idx = 27
    former_dds_latency_with_algo_cost_idx = 34
    former_algo_cost_idx = 38

    for line in lines:
        sp = line.split()
        if len(sp) != sps_len:
            continue
        
        log_date = sp[0]
        log_time = sp[1]
        v1 = int(sp[former_dds_latency_idx])
        v2 = int(sp[all_former_dds_latency_idx])
        v3 = int(sp[former_dds_latency_with_algo_cost_idx])
        v4 = int(sp[former_algo_cost_idx])

        # date time string to unix timestamp seconds
        stamp=time.mktime(time.strptime(log_date+" "+log_time, "I%Y%m%d %H:%M:%S.%f"))

        former_dds_latency.append((stamp, v1))
        all_former_dds_latency.append((stamp, v2))
        former_dds_latency_with_algo_cost.append((stamp, v3))
        former_algo_cost.append((stamp, v4))

    return infos

def parse_log(file_name):
    pub_logs = get_one_pattern_lines(file_name, "<<< PUB >>>")
    pub_e2e_logs=pub_e2e_cost_line_by_topic_name(pub_logs)
    for topic, logs in pub_e2e_logs.items():
        if topic != 'planning_output_topic,':
          continue
        infos = parse_pub_e2e_cost_line(topic, logs)
        e2e = []
        for a in range(0, len(infos["e2e_cost"])):
          e2e.append(infos["e2e_cost"][a][1])
        
        print("[MODULE]:", os.path.basename(file_name).ljust(20)[0:20])
        print("  [PUB]")
        print("    [TOPIC]", topic)
        print_cost("[pub][e2e-cost] ", infos["e2e_cost"], level=3)
        print_cost("[pub][algo_cost]", infos["algo_cost"], level=3)


    sub_logs = get_one_pattern_lines(file_name, "<<< SUB >>>")
    sub_e2e_logs=sub_e2e_cost_line_by_topic_name(sub_logs)
    for topic, logs in sub_e2e_logs.items():
        # if topic != "geely_chassis_topic":
        #     continue

        infos = parse_sub_e2e_cost_line(topic, logs)
        print("[MODULE]:", os.path.basename(file_name).ljust(20)[0:20])
        print("  [SUB]")
        print("    [TOPIC]", topic)
        print_cost("[sub][former dds latency] ", infos["former dds latency"], level=3)
        print_cost("[sub][all former dds latency]", infos["all former dds latency"], level=3)
        print_cost("[sub][former dds latency with algo cost]", infos["former dds latency with algo cost"], level=3)
        print_cost("[sub][former algo cost]", infos["former algo cost"], level=3)
        # print(infos["former algo cost"])


    fps_logs = get_one_pattern_lines(file_name, "Fast Fps topic fps =")
    pub_fps_logs=find_lines("pub", fps_logs)
    pub_info = pub_fps_by_topic_name(pub_fps_logs)
    for topic, logs in pub_info.items():
        infos = parse_pub_fps_line(topic, logs)
        print("[MODULE]:", os.path.basename(file_name).ljust(20)[0:20])
        print("  [PUB]")
        print("    [TOPIC]", topic)
        print_cost("[pub][fps] ", infos["fps"], level=3, isfps=True)

    return
    
    patterns = ["<<<PUB>>>"]
    lg = get_lines(file_name, patterns)

    # print(len(lg["[ControlRuntask:RunTask]"]))
    # print(len(lg["McuControl function call fps"]))
    costs = parse_control_algo(lg["[ControlRuntask:RunTask]"])
    fpss=parse_control_fps(lg["McuControl function call fps"])

    # print(len(costs))
    # print(len(fpss))
    print_cost("[ControlRuntask:RunTask]", costs, 0, True)
    print_cost("McuControl Algo fps", fpss, 0, False, True)

argparser = argparse.ArgumentParser(description='parse fusion6v5r log')
argparser.add_argument('-i', dest='input_file', type=str, help='log file name', 
                       default="/Users/fengguoqing/Documents/code/personal_tools/python/split_krider_planning20230906-161549.10077")


if __name__ == "__main__":
    args = argparser.parse_args()
    if args.input_file is None:
        print("log file name is None")
        sys.exit(1)

    parse_log(args.input_file)
