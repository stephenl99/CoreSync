#!/usr/bin/env python3

import paramiko
import os
from time import sleep
from util import *
from config_remote import *
from datetime import datetime
import random

conns = [100]
loads = [850000, 1500000]
breakwater_targets = [10, 30, 50, 80]
algorithms = ["nocontrol", "breakwater"]
schedulers = ["simple", "ias", "range_policy"]
delay_ranges = [[0.5, 1], [1, 4]]
utilization_ranges = [[0.75, 0.95]]

algorithm = "breakwater"
scheduler = "simple"
connections = 100
service_time = 10
breakwater_target = 10
service_distribution = "exp"
offered_load = 850000
range_loads = 1
loadshift = 0
spin_server = 0
num_cores_server = 18
num_cores_lc = 16
num_cores_lc_guaranteed = 16
caladan_threshold = 10
slo = 200
count = 1

caladan_interval = 5

sched_delay = 0
sched_utilization = 0
delay_lower = 0.5
delay_upper = 1
utilization_lower = 0.75
utilization_upper = 0.95

# 1 is true, 0 is false
avoid_large_downloads = 1

def call_experiment():
    global count
    print("experiment number: {}".format(count))
    # if count < 16:
    #     count += 1
    #     return
    count += 1
    # 5 per line
    os.system("python3 param_synthetic_antagonist.py {} {:d} {:d} {:d} {}"\
              " {:d} {:d} {:d} {:d} {:d}"\
              " {:d} {:d} {:d} {:d} {:d}"\
              " ".format(
              algorithm, connections, service_time, breakwater_target, service_distribution,
              offered_load, loadshift, spin_server, num_cores_server, num_cores_lc,
              num_cores_lc_guaranteed, caladan_threshold, slo, avoid_large_downloads, range_loads,
              scheduler, sched_delay, delay_lower, delay_upper, sched_utilization,
              utilization_lower, utilization_upper
              ))
    print("sleeping for 5 seconds before next connection")
    sleep(5)
    # just for testing
    # exit()

def main():
    global algorithm
    global connections
    global service_time
    global breakwater_target
    global service_distribution
    global offered_load
    global loadshift
    global spin_server
    global num_cores_server
    global num_cores_lc
    global num_cores_lc_guaranteed
    global caladan_threshold
    global slo
    global scheduler
    global delay_ranges
    global utilization_ranges
    global caladan_interval
    global delay_lower
    global delay_upper
    global utilization_lower
    global utilization_upper
    global sched_delay
    global sched_utilization

    for a in algorithms:
        algorithm = a
        for c in conns:
            connections = c
            for l in loads:
                offered_load = l
                for i in range(2):
                    if i == 0:
                        spin_server = 0
                        num_cores_lc_guaranteed = 0
                    else:
                        spin_server = 1
                        num_cores_lc_guaranteed = 16
                    if algorithm != "breakwater":
                        if not spin_server:
                            for s in schedulers:
                                if s == "range_policy":
                                    for range_s in ["delay", "utilization"]:
                                        if range_s == "delay":
                                            for d in delay_ranges:
                                                delay_lower = d[0]
                                                delay_upper = d[1]
                                                call_experiment()
                                        elif range_s == "utilization":
                                            for u in utilization_ranges:
                                                utilization_lower = u[0]
                                                utilization_upper = u[1]
                                                call_experiment()
                        else:
                            call_experiment()
                        continue
                    for t in breakwater_targets:
                        breakwater_target = t
                        # call_experiment()
                        if not spin_server:
                            for s in schedulers:
                                if s == "range_policy":
                                    for range_s in ["delay", "utilization"]:
                                        if range_s == "delay":
                                            for d in delay_ranges:
                                                delay_lower = d[0]
                                                delay_upper = d[1]
                                                call_experiment()
                                        elif range_s == "utilization":
                                            for u in utilization_ranges:
                                                utilization_lower = u[0]
                                                utilization_upper = u[1]
                                                call_experiment()
                        else:
                            call_experiment()
                                
                    

if __name__ == "__main__":
    main()




