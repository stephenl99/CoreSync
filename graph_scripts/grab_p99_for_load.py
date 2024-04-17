import os
import pandas
import numpy as np
import glob
import csv

load = "600k"

directories = os.listdir()
directories.sort()

for dir in directories:
    # print(dir)
    # continue
    if load in dir:
        os.chdir(dir)
        files = glob.glob("*{}*.csv".format(load))
        for f in files:
            p99 = pandas.read_csv(f)["p99"]
            print(f + ":  {}".format(int(p99[0])))
            # exit()
        os.chdir("..")