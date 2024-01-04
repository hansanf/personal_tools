#!/usr/bin/env python3

'''
from jetson stats github
监控整个 jetson platform 的性能
usage:
case1: 直接用 python3 执行

case2：
1. sudo su
2. export PYTHONPATH=/usr/local/lib/python3.6/dist-packages
3. 要用python3 
4. 保存的csv文件用jtop_ploter.py 画成曲线图
'''

from jtop import jtop, JtopException
import csv
import argparse

parser = argparse.ArgumentParser(description='Simple jtop logger')
# Standard file to store the logs
parser.add_argument('--file', action="store", dest="file", default="log.csv")
args = parser.parse_args()

if __name__ == "__main__":
    print("Simple jtop logger")
    print("Saving log on {file}".format(file=args.file))
    try:
        with jtop() as jetson:
            # Make csv file and setup csv
            with open(args.file, 'w') as csvfile:
                stats = jetson.stats
                # Initialize cws writer
                writer = csv.DictWriter(csvfile, fieldnames=stats.keys())
                # Write header
                writer.writeheader()
                # Write first row
                writer.writerow(stats)
                # Start loop
                while jetson.ok():
                    stats = jetson.stats
                    #print(stats['GPU'])
                    # Write row
                    writer.writerow(stats)
                    print("Log at {time}".format(time=stats['time']))
    except JtopException as e:
        print(e)
    except KeyboardInterrupt:
        print("Closed with CTRL-C")
    except IOError:
        print("I/O error")
# EOF