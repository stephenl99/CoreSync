import os
import pandas
import numpy as np
import glob
import csv



parking_scales = [0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
core_credit_ratios = [5, 10, 12, 14, 15, 16, 18, 20, 22, 24, 30]
load = "600k" # doing ~600k or 700k for 10 us, what should it be for 1us? ~2 mil?
ts_index = 2 # because this will change easily... and I don't think I can grab a row so easily, since it's dictated by a floating value
overall_index = 2

vary_parking = False
vary_core_credit_ratio = True

# print out initial headers
print("just not doing spin, doing it manually now since it's annoying, wait we don't need spin anyway, due to the static core line")
schedulers = ["ias", "simple", "utilization", "delay_1.0_4.0", "delay_0.5_1.0"]
parking_schedulers = ["ias", "simple"]
fields = []
if vary_parking:
    for s in parking_schedulers:
        for ps in parking_scales:
            fields.append(s + "_{}".format(ps))
elif vary_core_credit_ratio:
    for s in parking_schedulers:
        for ccr in core_credit_ratios:
            fields.append(s + "_{}".format(ccr))
# fields += schedulers
fields.sort()
# print(fields)
csv_header = ",".join(fields) + "\n"

outfile = open("efficiency.csv", "w+")
outfile.write(csv_header)


# need to be in the combined_timeseries dir
os.chdir("bw_timeseries_csvs/combined_timeseries")

files = os.listdir()
files.sort()
print("make sure file order matches your effieciency.csv order!")
values = []
for f in files:
    if "spin" in f:
        continue
    # print(f)
    # continue
    pd = pandas.read_csv(f)
    val = pd.loc[ts_index, "avg_cores"]
    print(f + ": ", val)
    values.append("{:.4f}".format(val))
outfile.write(",".join(values) + "\n")

# needs to be in the overall csvs folder
os.chdir("../../overall_csvs")
directories = os.listdir()
directories.sort()

# single directory version, NON range load
# for dir in directories:
#     # print(dir)
#     # continue
#     if load in dir:
#         os.chdir(dir)
#         files = glob.glob("*{}*.csv".format(load))
#         for f in files:
#             p99 = pandas.read_csv(f)["p99"]
#             print(f + ":  {}".format(int(p99[0])))
#             # exit()
#         os.chdir("..")
# overall csvs version, RANGE LOADS
print("make sure file order matches your effieciency.csv order!")
values = []
for f in directories:
    if "spin" in f:
        continue
    p99 = pandas.read_csv(f)["p99"]
    val = int(p99[overall_index])
    print(f + ":  {}".format(val))
    values.append("{}".format(val))
    # exit()
outfile.write(",".join(values) + "\n")