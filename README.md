### Usage
#### shell
[echo_branch.sh](shell/echo_branch.sh)  
  列出当前各个目录的repo分支
  ```bash echo_bransh.sh```   

[ps_mem_cpu.sh](shell/ps_mem_cpu.sh)  
  统计指定进程的内存和cpu使用情况   
  ```bash ps_mem_cpu.sh PID```

#### python
[plot_cpu_mem.py](python/plot_cpu_mem.py)   
  对 ps_mem_cpu.sh 的结果进行可视化   
```python plot_cpu_mem.py --log_nam=pid_stats_20057.txt --res_dir=./result```   

[re_fetch_name_fps.py](re_fetch_name_fps)   
  用正则表达式方式对日志中的字段进行提取，提取耗时、fps等   

[jtop_logger.py](python/jtop_logger.py)  
  jetson stats(jtop) 的官方例子，记录整个平台的资源情况   

[jtop_ploter.py](python/jtop_ploter.py)  
  将 jtop_logger.py 所保存的 log.csv 内容画成曲线图   

