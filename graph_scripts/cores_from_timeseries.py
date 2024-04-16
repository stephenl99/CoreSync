import os
import pandas
import numpy as np
import glob
import csv

metrics = ["timestamp", "num_cores", "credit_pool", "credit_used"]
fields = ["offered_load","avg_cores","avg_credit_pool","avg_credit_issued"]
field_string = "offered_load,avg_cores,avg_credit_pool,avg_credit_issued\n"
# if you change this, reflect it in csv header write as well

load = "400k"
loads = ["400k", "500k", "600k", "700k", "800k", "900k", "1000k", "1100k", "1200k", "1300k", "1400k", "1600k", "2000k" "3000k"]
load_nums = [400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1600000, 2000000, 3000000]
# parking_scales = [0.1, 0.2, 0.4, 0.6, 0.8, 1.2, 1.4]
parking_scales = [0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4]
conns = 100
nodes = 11
breakwater_target = 80
bw_thresh = breakwater_target * 2
avg_service_time = 10
# simple
# ias
# utilization_range_0.75_0.95
# delay_range_0.5_1.0
# delay_range_1.0_4.0
scheduler = "utilization_range_0.75_0.95"
# parking_scale = 1.4
parking_on = False
spinning = False
after_warmup_len = 4000000
output_dir = "combined_timeseries"

if not parking_on:
    parking_scales = [0] # just make list 1 item long

def generate_csv(parking_scale):
    if parking_on and spinning:
        print("breakwater parking and spinning are enabled, are you sure about this?")
        exit()

    parking = "_park_{}".format(parking_scale) if parking_on else ""
    spin = "guaranteed_spinning" if spinning else ""

    files = []

    for l in loads:
        f = glob.glob("ts_breakwater_*{}_{}_*{}conns_{}nodes_{}{}.csv".format(spin, l, conns, nodes, scheduler, parking))
        files.append(f[0])

    # for f in files:
    #     print(f)
    combined_data = []
    print("files like: " + files[0])
    for i,f in enumerate(files):
        # print(f)
        df = pandas.read_csv(f)
        Data = df[metrics]
        Data = np.array(Data)
        last_timestamp = Data[-1,0]
        mask = (Data[:,0] > (last_timestamp - after_warmup_len))
        Data = Data[mask,:] # remove rows that are during the warmup period
        combined_data.append((load_nums[i], np.average(Data[:,1]), np.average(Data[:,2]), np.average(Data[:,3]))) # avg of second col, which is cores

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if spinning:
        spin = "_" + spin
    outfile_name = "{}/combined_timeseries_{}_{}{}{}.csv".format(output_dir, breakwater_target, scheduler, parking, spin)
    if os.path.exists(outfile_name):
        print("error, file existed already: ")
        print(outfile_name)
    with open(outfile_name, "w+") as outfile:
        # csvwriter = csv.writer(outfile)
        # csvwriter.writerow(fields)
        outfile.write(field_string)
        for entry in combined_data:
            outfile.write("{:.4f},{:.4f},{:.4f},{:.4f}\n".format(entry[0], entry[1], entry[2], entry[3]))

for ps in parking_scales:
    generate_csv(ps)