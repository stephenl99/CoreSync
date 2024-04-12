import os
import sys
import shutil

if not os.path.exists("bw_timeseries_csvs"):
    os.makedirs("bw_timeseries_csvs")
for current_dir in os.listdir():
    if current_dir == "overall_csvs" or current_dir == "bw_timeseries_csvs" or not ("conns" in current_dir):
        continue
    os.chdir(current_dir)
    for f in os.listdir():
        if "timeseries" in f:
            shutil.copy(f, "../bw_timeseries_csvs/ts_{}".format(current_dir + ".csv"))
            print(current_dir)
    os.chdir("..")
print("done")