#!/usr/bin/python
#coding:utf-8
import re
import numpy as np
import matplotlib.pyplot as plt
import argparse
import datetime

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_name", default="krider_multiperception_car.INFO_nv2", type=str, help='log name')
    # parser.add_argument("--grep_name", default="FAKE_CAPTURE", type=str, help='module name')
    parser.add_argument("--plot", default=True, type=bool, help='plot switch')
    parser.add_argument("--res_dir", default="./result/", type=str, help="restult dir")

    opt = parser.parse_args()
    return opt

def plot(x, y, x_name="x", y_name="y", title="figure", label="", save_name=""):
    # plt.figure(figsize=(6,4))
    # plt.plot(x,y,color="blue",linewidth=1 )
    plt.plot(x, y, label=label)
    plt.xlabel(x_name) #xlabel、ylabel：分别设置X、Y轴的标题文字。
    plt.ylabel(y_name)
    plt.title(title) # title：设置子图的标题。
    plt.legend()
    # plt.ylim(-1.1,1.1)# xlim、ylim：分别设置X、Y轴的显示范围。
    if len(save_name):
        plt.savefig(save_name, bbox_inches='tight')
    else:
        plt.show()

opt = options()
log_name=opt.log_name
fake_caputures = []
decode_imgs = []
percept_fpss = []
cam0_fpss = []
cam1_fpss = []
pub_fpss = []

fake_capture_timestamps = []
decode_img_timestamps = []
percept_fps_timestamps = []
cam0_fps_timestamps = []
cam1_fps_timestamps = []
pub_fps_timestamps = []
with open(log_name, 'r') as f:
    for line in f:
        # match = re.search(r'FAKE_CAPTURE : (\d+)us', line)
        # if match:
        #     fake_caputures.append(int(match.group(1)))
        #     parts = line.split()
        #     timestamp = datetime.datetime.strptime(parts[0].lstrip("I") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
        #     fake_capture_timestamps.append(timestamp)

        match = re.search(r'DECODE_IMG : (\d+)us', line)
        if match:
            decode_imgs.append(int(match.group(1)))
            parts = line.split()
            timestamp = datetime.datetime.strptime(parts[0].lstrip("I") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
            decode_img_timestamps.append(timestamp)
        
# Calculate the percentiles
# fake_caputures_50th = np.percentile(fake_caputures, 50)
# fake_caputures_90th = np.percentile(fake_caputures, 90)
# fake_caputures_99th = np.percentile(fake_caputures, 99)

decode_imgs_50th = np.percentile(decode_imgs, 50)
decode_imgs_90th = np.percentile(decode_imgs, 90)
decode_imgs_99th = np.percentile(decode_imgs, 99)
  
print(f'decode_img 50th percentile: {decode_imgs_50th:.2f} us')
print(f'decode_img 90th percentile: {decode_imgs_90th:.2f} us')
print(f'decode_img 99th percentile: {decode_imgs_99th:.2f} us')

plot(decode_img_timestamps, decode_imgs, "Log Time", "Time (us)", "Decode Image Time", "Decode", opt.res_dir + "decode_time_cost.jpg")           