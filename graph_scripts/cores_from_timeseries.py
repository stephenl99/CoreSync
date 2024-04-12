import os
import pandas
import numpy as np
import glob

metrics = ["num_cores"]

load = "400k"
loads = [400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1600000, 2000000]
conns = 100
nodes = 11
breakwater_target = 80
bw_thresh = breakwater_target * 2
avg_service_time = 10
# simple
# ias
# utilization_range
# delay_range_0.5_1.0
# delay_range_1.0_4.0
scheduler = "simple"
parking = "_park_0.9"

for l in loads:
    files = glob.glob("ts_breakwater_*{}_*{}conns_{}nodes_{}{}.csv".format(l, conns, nodes, scheduler, parking))
    for f in files:
        print(f)

