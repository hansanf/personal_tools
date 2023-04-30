#!/usr/bin/python
#coding:utf-8
# 正则表达式提取日志字段
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
    # if len(save_name):
    #     plt.savefig(save_name,dpi=120,bbox_inches='tight')
    # else:
    #     plt.show()

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

        # match = re.search(r'DECODE_IMG : (\d+)us', line)
        # if match:
        #     decode_imgs.append(int(match.group(1)))
        #     parts = line.split()
        #     timestamp = datetime.datetime.strptime(parts[0].lstrip("I") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
        #     decode_img_timestamps.append(timestamp)
        
        match = re.search(r'Algo fps = (\d+\.\d+)', line)
        if match:
            percept_fpss.append(float(match.group(1)))
            parts = line.split()
            timestamp = datetime.datetime.strptime(parts[0].lstrip("W") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
            percept_fps_timestamps.append(timestamp)
        
        match = re.search(r'cam: 0, fps = (\d+\.\d+)', line)
        if match:
            cam0_fpss.append(float(match.group(1)))
            parts = line.split()
            timestamp = datetime.datetime.strptime(parts[0].lstrip("W") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
            cam0_fps_timestamps.append(timestamp)
                     
        match = re.search(r'cam: 1, fps = (\d+\.\d+)', line)
        if match:
            cam1_fpss.append(float(match.group(1)))
            parts = line.split()
            timestamp = datetime.datetime.strptime(parts[0].lstrip("W") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
            cam1_fps_timestamps.append(timestamp)
            
        match = re.search(r'DynamicCameraFrameInfo topic fps = (\d+\.\d+)', line)
        if match:
            pub_fpss.append(float(match.group(1)))
            parts = line.split()
            timestamp = datetime.datetime.strptime(parts[0].lstrip("I") + ' ' + parts[1].split(".")[0], '%Y%m%d %H:%M:%S')
            pub_fps_timestamps.append(timestamp)
            
# Calculate the percentiles
# fake_caputures_50th = np.percentile(fake_caputures, 50)
# fake_caputures_90th = np.percentile(fake_caputures, 90)
# fake_caputures_99th = np.percentile(fake_caputures, 99)

# decode_imgs_50th = np.percentile(decode_imgs, 50)
# decode_imgs_90th = np.percentile(decode_imgs, 90)
# decode_imgs_99th = np.percentile(decode_imgs, 99)

percept_fpss_50th = np.percentile(percept_fpss, 50)
percept_fpss_90th = np.percentile(percept_fpss, 90)
percept_fpss_99th = np.percentile(percept_fpss, 99)

cam0_fpss_50th = np.percentile(cam0_fpss, 50)
cam0_fpss_90th = np.percentile(cam0_fpss, 90)
cam0_fpss_99th = np.percentile(cam0_fpss, 99)

cam1_fpss_50th = np.percentile(cam1_fpss, 50)
cam1_fpss_90th = np.percentile(cam1_fpss, 90)
cam1_fpss_99th = np.percentile(cam1_fpss, 99)

pub_fpss_50th = np.percentile(pub_fpss, 50)
pub_fpss_90th = np.percentile(pub_fpss, 90)
pub_fpss_99th = np.percentile(pub_fpss, 99)

# Print the results
# print('Cost Time: ')
# print(f'fake_caputure  50th percentile: {fake_caputures_50th:.2f} us')
# print(f'fake_caputure  90th percentile: {fake_caputures_90th:.2f} us')
# print(f'fake_caputure  99th percentile: {fake_caputures_99th:.2f} us')
  
# print(f'decode_img  50th percentile: {decode_imgs_50th:.2f} us')
# print(f'decode_img  90th percentile: {decode_imgs_90th:.2f} us')
# print(f'decode_img  99th percentile: {decode_imgs_99th:.2f} us')

print(f'perception fps 50th percentile: {percept_fpss_50th:.2f} hz')
print(f'perception fps 90th percentile: {percept_fpss_90th:.2f} hz')
print(f'perception fps 99th percentile: {percept_fpss_99th:.2f} hz')

print(f'camera0 fps 50th percentile: {cam0_fpss_50th:.2f} hz')
print(f'camera0 fps 90th percentile: {cam0_fpss_90th:.2f} hz')
print(f'camera0 fps 99th percentile: {cam0_fpss_99th:.2f} hz')

print(f'camera1 fps 50th percentile: {cam1_fpss_50th:.2f} hz')
print(f'camera1 fps 90th percentile: {cam1_fpss_90th:.2f} hz')
print(f'camera1 fps 99th percentile: {cam1_fpss_99th:.2f} hz')

print(f'pub topic fps 50th percentile: {pub_fpss_50th:.2f} hz')
print(f'pub topic fps 90th percentile: {pub_fpss_90th:.2f} hz')
print(f'pub topic fps 99th percentile: {pub_fpss_99th:.2f} hz')


# plot(decode_img_timestamps, decode_imgs, "Log Time", "Time (us)", "Decode Image Time", "Decode")           

plot(percept_fps_timestamps, percept_fpss, "Log Time", "perception fps", "Perf With Time", "MultiPerception Algo Fps", "")           
plot(cam0_fps_timestamps, cam0_fpss, "Log Time", "cam0 fps", "Perf With Time", "Camera0 Fps", "")           
plot(cam1_fps_timestamps, cam1_fpss, "Log Time", "cam1 fps", "Perf With Time", "Camera1 Fps", "")           
plot(pub_fps_timestamps, pub_fpss, "Log Time", "pub fps", "Perf With Time", "Pub topic Fps", "")           

# plt.show()
plt.savefig(opt.res_dir+"multiperception_fps.jpg", bbox_inches='tight')