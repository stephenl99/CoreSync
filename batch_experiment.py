#!/usr/bin/env python3

import paramiko
import os
from time import sleep
from util import *
import config_remote
from datetime import datetime
import random

conns = [100]
loads = [0]
breakwater_targets = [80]
algorithms = ["breakwater"]
schedulers = ["simple", "ias", "range_policy"]
delay_ranges = [[0.5, 1], [1, 4]]
utilization_ranges = [[0.75, 0.95]]
load_factors = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

algorithm = "breakwater"
scheduler = "simple"
connections = 100
service_time = 10
breakwater_target = 80
service_distribution = "exp"
offered_load = 850000
range_loads = 1 # commented out in code anyway for now to default to this multiple same load behavior
loadshift = 0
spin_server = 0
num_cores_server = 18
num_cores_lc = 16
num_cores_lc_guaranteed = 0
caladan_threshold = 10
slo = 200
count = 1

caladan_interval = 5

sched_delay = 0
sched_utilization = 0
delay_lower = 0.5
delay_upper = 1.0
utilization_lower = 0.75
utilization_upper = 0.95

# 1 is true, 0 is false
avoid_large_downloads = 1

current_load_factor = 1.0

def call_experiment():
    global count
    print("experiment number: {}".format(count))
    if count < 6:
        count += 1
        return
    count += 1
    # 5 per line
    config_remote.PARAM_EXP_FLAG = False  # set to True at end of the param synthetic file
    failure_code = os.system("python3 param_synthetic_antagonist.py {} {:d} {:d} {:d} {}"\
              " {:d} {:d} {:d} {:d} {:d}"\
              " {:d} {:d} {:d} {:d} {:d}"\
              " {} {:d} {:f} {:f} {:d}"\
              " {:f} {:f} {:f}".format(
              algorithm, connections, service_time, breakwater_target, service_distribution,
              offered_load, loadshift, spin_server, num_cores_server, num_cores_lc,
              num_cores_lc_guaranteed, caladan_threshold, slo, avoid_large_downloads, range_loads,
              scheduler, sched_delay, delay_lower, delay_upper, sched_utilization,
              utilization_lower, utilization_upper, current_load_factor
              ))
    if failure_code != 0:
        print("sys call failed, look at console or log")
        exit()
    print("algorithm: {}".format(algorithm))
    print("spinning: {}\nscheduler: {}\nsched_delay: {}".format(spin_server, scheduler, sched_delay))
    print("bw target: {}\ndelay_lower: {}\nutilization_lower {}".format(breakwater_target, delay_lower, utilization_lower))
    print("sleeping for 5 seconds before next connection\n\n")
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
    global current_load_factor
    
    
    # for s in ["spinning", "simple", "ias", "range_policy"]:
    #     scheduler = s
    #     for lf in load_factors:
    #         current_load_factor = lf
    #         # if s == "spinning" and (lf == 1.0 or lf == 1.1 or lf == 1.2):
    #         #     continue
    #         if s == "spinning":
    #             scheduler = "simple"
    #             spin_server = 1
    #             num_cores_lc_guaranteed = num_cores_lc
    #             sched_utilization = 0
    #         elif s == "range_policy":
    #             spin_server = 0
    #             num_cores_lc_guaranteed = 0
    #             sched_utilization = 1
    #         else:
    #             spin_server = 0
    #             num_cores_lc_guaranteed = 0
    #             sched_utilization = 0
    #         call_experiment()

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
                        num_cores_lc_guaranteed = num_cores_lc
                    if algorithm != "breakwater":
                        if not spin_server:
                            for s in schedulers:
                                scheduler = s
                                if s == "range_policy":
                                    for range_s in ["utilization", "delay"]:
                                        if range_s == "delay":
                                            for d in delay_ranges:
                                                delay_lower = d[0]
                                                delay_upper = d[1]
                                                sched_delay = 1
                                                call_experiment()
                                                sched_delay = 0
                                        elif range_s == "utilization":
                                            for u in utilization_ranges:
                                                utilization_lower = u[0]
                                                utilization_upper = u[1]
                                                sched_utilization = 1
                                                call_experiment()
                                                sched_utilization = 0
                                else:
                                    # should call ias and simple
                                    call_experiment()
                        else:
                            scheduler = "simple"
                            call_experiment()
                        continue
                    for t in breakwater_targets:
                        breakwater_target = t
                        # call_experiment()
                        if not spin_server:
                            for s in schedulers:
                                scheduler = s
                                if s == "range_policy":
                                    for range_s in ["utilization", "delay"]:
                                        if range_s == "delay":
                                            for d in delay_ranges:
                                                delay_lower = d[0]
                                                delay_upper = d[1]
                                                sched_delay = 1
                                                call_experiment()
                                                sched_delay = 0
                                        elif range_s == "utilization":
                                            for u in utilization_ranges:
                                                utilization_lower = u[0]
                                                utilization_upper = u[1]
                                                sched_utilization = 1
                                                call_experiment()
                                                sched_utilization = 0
                                else:
                                    call_experiment()
                        else:
                            scheduler = "simple"
                            call_experiment()
                                
                    

if __name__ == "__main__":
    main()




