#!/usr/bin/env python

import sys
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import math

second_in_us = 1000000
rasterize = False

def main_plot():
    pass

def parse_all_tasks():
    df = pd.read_csv("all_tasks.csv")
    Data = df[['start_us', 'duration_us']]
    completed_tasks_data = np.array(Data)
    completed_tasks_data[:,0] /= second_in_us

    latency_99 = completed_tasks_data.copy()
    # sort by second column
    # a[a[:, 1].argsort()]
    latency_99 = latency_99[latency_99[:,1].argsort()]
    idx = int(len(latency_99) * 0.99)
    latency_99 = latency_99[idx:]
    # resort back by timestamp
    latency_99[latency_99[:,0].argsort()]


    """ 
    PLOTTING
    """
    
    fig, (plt1, plt2, plt3, plt4) = plt.subplots(4, 1, figsize=(20,20))
    fig.suptitle("time_series", fontsize=22, y=1.0)
    fig.tight_layout()
    # x_range = [0, 100000]
    """
    PLOT 1
    """
    plt1.tick_params(axis='both', which='major', labelsize=18)

    # plt1.axis(xmin=x_range[0], xmax=x_range[1])
    # plt1.axis(ymin=50, ymax=101)
    plt1.grid(which='major', color='black', linewidth=1.0)
    plt1.grid(which='minor', color='grey', linewidth=0.2)
    plt1.minorticks_on()
    # plt.ylim(ymin=0)

            
    plt1.plot(completed_tasks_data[:,0], completed_tasks_data[:,1], rasterized=rasterize)

    plt1.set_xlabel('Time (s)', fontsize=18)
    plt1.set_ylabel('latencies (us)', fontsize=18)
    # plt1.legend(fontsize=18)


    """
    PLOT 2
    """
    plt2.tick_params(axis='both', which='major', labelsize=18)

    # plt2.axis(xmin=x_range[0], xmax=x_range[1])
    
    plt2.grid(which='major', color='black', linewidth=1.0)
    plt2.grid(which='minor', color='grey', linewidth=0.2)
    plt2.minorticks_on()
    # plt.ylim(ymin=0)

            
    plt2.scatter(latency_99[:,0], latency_99[:,1], rasterized=rasterize, alpha=0.2)

    plt2.axis(ymin=0)
    plt2.set_xlabel('Time (s)', fontsize=18)
    plt2.set_ylabel('99th latency (us)', fontsize=18)
    #plt2.legend(fontsize=18)
    
    # plt.show()

    # print(completed_tasks_data[0:3])

def parse_drops_server():
    pass

def parse_drops_client():
    pass



def main():
    parse_all_tasks()

if __name__ == '__main__':
    main()