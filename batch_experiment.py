#!/usr/bin/env python3

import paramiko
import os
from time import sleep
from util import *
import config_remote
from datetime import datetime
import random

conns = [100]
loads = [400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1600000, 2000000]
breakwater_targets = [80]
algorithms = ["breakwater"]
schedulers = ["simple", "ias", "spin"] # "range_policy"]
delay_ranges = [[0.5, 1], [1, 4]]
utilization_ranges = [[0.75, 0.95]]
load_factors = [1.0, 0.9, 1.1] # going to do one additional run before running this where BREAKWATER_CORE_PARKING is off.
# need to do individual load runs in order to grab the timeseries each time.
# uncertain of the best way to do this besides looping over loads AND over these loadfactors- will probably take forever

algorithm = "breakwater"
scheduler = "simple"
connections = 100
service_time = 10
breakwater_target = 80
service_distribution = "exp"
offered_load = 850000
range_loads = 0 # can comment out in code to use the multiple same load behavior
loadshift = 0
spin_server = 0
num_cores_server = 18
num_cores_lc = 16
num_cores_lc_guaranteed = 0
caladan_threshold = 10
slo = 200
count = 1

caladan_interval = 10

sched_delay = 0
sched_utilization = 0
delay_lower = 0.5
delay_upper = 1.0
utilization_lower = 0.75
utilization_upper = 0.95

# 1 is true, 0 is false
avoid_large_downloads = 1
breakwater_parking = 1

current_load_factor = 1.0

def call_experiment():
    global count
    print("experiment number: {}".format(count))
    # if count < 3:
    #     count += 1
    #     return
    # if count > 4:
    #     exit()
    # if count == 6:
    #     count += 1
    #     return
    count += 1
    # 5 per line
    config_remote.PARAM_EXP_FLAG = False  # set to True at end of the param synthetic file
    failure_code = os.system("python3 param_synthetic_antagonist.py {} {:d} {:d} {:d} {}"\
              " {:d} {:d} {:d} {:d} {:d}"\
              " {:d} {:d} {:d} {:d} {:d}"\
              " {} {:d} {:f} {:f} {:d}"\
              " {:f} {:f} {:f} {:d}"\
              " {}".format(
              algorithm, connections, service_time, breakwater_target, service_distribution,
              offered_load, loadshift, spin_server, num_cores_server, num_cores_lc,
              num_cores_lc_guaranteed, caladan_threshold, slo, avoid_large_downloads, range_loads,
              scheduler, sched_delay, delay_lower, delay_upper, sched_utilization,
              utilization_lower, utilization_upper, current_load_factor, caladan_interval,
              breakwater_parking
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
    global breakwater_parking
    
    for s in schedulers:
        scheduler = s
        for l in loads:
            offered_load = l
            if s == "spin":
                scheduler = "simple"
                spin_server = 1
                num_cores_lc_guaranteed = 16
                breakwater_parking = 0
                call_experiment()
                spin_server = 0
                num_cores_lc_guaranteed = 0
                breakwater_parking = 1
            else:    
                for lf in load_factors:
                    current_load_factor = lf
                    call_experiment()
                
                    

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

    # for a in algorithms:
    #     algorithm = a
    #     for c in conns:
    #         connections = c
    #         for l in load_factors:
    #             current_load_factor = l
    #             # offered_load = l, for l in loads
    #             for i in range(2):
    #                 if i == 0:
    #                     spin_server = 0
    #                     num_cores_lc_guaranteed = 0
    #                 else:
    #                     spin_server = 1
    #                     num_cores_lc_guaranteed = num_cores_lc
    #                 if algorithm != "breakwater":
    #                     if not spin_server:
    #                         for s in schedulers:
    #                             scheduler = s
    #                             if s == "range_policy":
    #                                 caladan_interval = 5
    #                                 for range_s in ["utilization", "delay"]:
    #                                     if range_s == "delay":
    #                                         for d in delay_ranges:
    #                                             delay_lower = d[0]
    #                                             delay_upper = d[1]
    #                                             sched_delay = 1
    #                                             call_experiment()
    #                                             sched_delay = 0
    #                                     elif range_s == "utilization":
    #                                         for u in utilization_ranges:
    #                                             utilization_lower = u[0]
    #                                             utilization_upper = u[1]
    #                                             sched_utilization = 1
    #                                             call_experiment()
    #                                             sched_utilization = 0
    #                             else:
    #                                 # should call ias and simple
    #                                 caladan_interval = 10
    #                                 call_experiment()
    #                     else:
    #                         scheduler = "simple"
    #                         call_experiment()
    #                     continue
    #                 for t in breakwater_targets:
    #                     breakwater_target = t
    #                     # call_experiment()
    #                     if not spin_server:
    #                         for s in schedulers:
    #                             scheduler = s
    #                             if s == "range_policy":
    #                                 caladan_interval = 5
    #                                 for range_s in ["utilization", "delay"]:
    #                                     if range_s == "delay":
    #                                         for d in delay_ranges:
    #                                             delay_lower = d[0]
    #                                             delay_upper = d[1]
    #                                             sched_delay = 1
    #                                             call_experiment()
    #                                             sched_delay = 0
    #                                     elif range_s == "utilization":
    #                                         for u in utilization_ranges:
    #                                             utilization_lower = u[0]
    #                                             utilization_upper = u[1]
    #                                             sched_utilization = 1
    #                                             call_experiment()
    #                                             sched_utilization = 0
    #                             else:
    #                                 caladan_interval = 10
    #                                 call_experiment()
    #                     else:
    #                         if l != load_factors[0]:
    #                             continue
    #                         caladan_interval = 10
    #                         scheduler = "simple"
    #                         call_experiment()
                                
                    

if __name__ == "__main__":
    main()




