#!/usr/bin/env python3

import paramiko
import os
from time import sleep, time
from util import *
from config_remote import *
from datetime import datetime
import random
import sys

if len(sys.argv) < 2:
    print("usage: param_run_synthetic_antagonist.py <policy>")
    sys.exit(1)


################################
### Experiemnt Configuration ###
################################

POLICY = sys.argv[1]

if POLICY.lower() == "static":
    SCHEDULER = "simple"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = True
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "shenango":
    SCHEDULER = "simple"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "caladan1":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "caladan2":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 5
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "caladan3":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 10
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "util_range":
    SCHEDULER = "simple range_policy"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = True
    utilization_lower = 0.75
    utilization_upper = 0.95
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "delay_range1":
    SCHEDULER = "simple range_policy"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = True
    delay_lower = 0.5          # Derived from the SLO and service time
    delay_upper = 1            # Derived from the SLO and service time
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "delay_range2":
    SCHEDULER = "simple range_policy"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = True
    delay_lower = 1            # Derived from the SLO and service time
    delay_upper = 4           # Derived from the SLO and service time
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = False
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "coresync1":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = True
    CORESYNC_R = 10      # Derived from the number of flows
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "coresync2":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = True
    CORESYNC_R = 20      # Derived from the number of flows
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "coresync3":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = True
    CORESYNC_R = 50      # Derived from the number of flows
    print(f"{POLICY} has been chosen.")
elif POLICY.lower() == "coresync4":
    SCHEDULER = "ias"
    OVERLOAD_ALG = "breakwater"
    CALADAN_INTERVAL = 5
    CALADAN_THRESHOLD = 5
    CALADAN_SCHED_POLL = 2
    SPIN_SERVER = False
    DELAY_RANGE = False
    UTILIZATION_RANGE = False
    CORESYNC_ENABLE = True
    CORESYNC_R = 100      # Derived from the number of flows
    print(f"{POLICY} has been chosen.")
else:
    raise ValueError("Invalid policy chosen. Please choose between [static, shenango, caladan, delay_range, util_range, coresync]")

# The number of client connections
NUM_CONNS = 100

# List of offered load
CAPACITY = 4000000
OFFERED_LOADS = [ int((CAPACITY * i )/100) for i in range(10, 160, 10) ] # 10% to 150% in steps of 10%


# loadshift = 1 for load shifts in netbench.cc
LOADSHIFT = 0

# Average service time (in us)
ST_AVG = 1

# Service time distribution
#    exp: exponential
#    const: constant
#    bimod: bimodal
ST_DIST = "bimod"

# SLO = 10 * (average RPC processing time + network RTT)
NET_RTT = 10
slo = 110

# make sure these match in bw_config.h
BW_TARGET = 45
BW_THRESHOLD = 90
BREAKWATER_TIMESERIES = False

ENABLE_DIRECTPATH = True
DISABLE_WATCHDOG = False

NUM_CORES_LC = 16
NUM_CORES_LC_GUARANTEED = 0
NUM_CORES_ANTON = 16
NUM_CORES_CLIENT = 16

"""
First, we design a queueing-based policy called delay
range which attempts to maintain a specified average queue-
ing delay across all cores within an application. Every core-
allocation interval (every 5 μs), the simulation checks the
average queueing delay. If it is below the specified lower
bound, a core is revoked; if it is above the upper bound, a core
is added. Similarly, with our utilization range policy, a core
is added or removed whenever the average CPU utilization
over the past interval (fraction of time spent handling tasks)
falls outside the specified range.
"""

AVOID_LARGE_DOWNLOADS = False

DOWNLOAD_ALL_TASKS = False

IAS_DEBUG = False

ERIC_CSV_NAMING = True

CSV_NAME_DIR = True

# Antagonist paramters
ENABLE_ANTAGONIST = False
ANTON_SHM_KEY = 0x1234
ANTON_THREADS = 18
ANTON_WORK_UNITS = 10
ANTON_RANDOM_SEED = random.randint(0, 4294967295)
ANTON_MEMSIZE = 4090880
ANTON_WORK_PARAM = "randmem:{:d}:{:d}".format(ANTON_MEMSIZE, ANTON_RANDOM_SEED)

############################
### End of configuration ###
############################

# Update the config
print("modifying bw_config.h values for target and threshold")
cmd = "sed -i \'s/#define SBW_DELAY_TARGET.*/#define SBW_DELAY_TARGET\\t\\t\\t{:d}/g\'"\
        " ../configs/bw_config.h".format(BW_TARGET)
execute_local(cmd)
cmd = "sed -i \'s/#define SBW_DROP_THRESH.*/#define SBW_DROP_THRESH\\t\\t\\t{:d}/g\'"\
        " ../configs/bw_config.h".format(BW_THRESHOLD)
execute_local(cmd)

cmd = "sed -i \'s/#define SBW_LATENCY_BUDGET.*/#define SBW_LATENCY_BUDGET\\t\\t\\t{:d}/g\'"\
        " ../configs/bw2_config.h".format(BW_THRESHOLD)
execute_local(cmd)

# Update the code to enable downloading all tasks
if DOWNLOAD_ALL_TASKS:
    cmd = "sed -i \'s/#define ENABLE_DOWNLOAD_ALL_TASKS.*/#define ENABLE_DOWNLOAD_ALL_TASKS\\t\\t\\t true/g\'"\
        " ../replace/netbench.cc"
    execute_local(cmd)
else:
    cmd = "sed -i \'s/#define ENABLE_DOWNLOAD_ALL_TASKS.*/#define ENABLE_DOWNLOAD_ALL_TASKS\\t\\t\\t false/g\'"\
        " ../replace/netbench.cc"
    execute_local(cmd)

# Verify configs #
if OVERLOAD_ALG not in ["protego", "breakwater", "seda", "dagor", "nocontrol"]:
    print("Unknown overload algorithm: " + OVERLOAD_ALG)
    exit()

if ST_DIST not in ["exp", "const", "bimod"]:
    print("Unknown service time distribution: " + ST_DIST)
    exit()

### Function definitions ###
def generate_shenango_config(is_server ,conn, ip, netmask, gateway, num_cores,
        directpath, spin, disable_watchdog, latency_critical=False, guaranteed_kthread=0, antagonist="none"):
    config_name = ""
    config_string = ""
    if is_server:
        config_name = "server.config"
        config_string = "host_addr {}".format(ip)\
                      + "\nhost_netmask {}".format(netmask)\
                      + "\nhost_gateway {}".format(gateway)\
                      + "\nruntime_kthreads {:d}".format(num_cores)
        if latency_critical:
            config_string += "\nruntime_priority lc"
            # config_string += "\nruntime_ht_punish_us 10000" # paper says "infinite" for memcached. Defaulting to 0 so
        else:
            config_string += "\nruntime_priority be"
        config_string += "\nruntime_guaranteed_kthreads {:d}".format(guaranteed_kthread)
        config_string += "\nruntime_qdelay_us {:d}".format(CALADAN_THRESHOLD)
        if DELAY_RANGE:
            config_string += "\nruntime_qdelay_lower_thresh_ns {:d}".format(int(delay_lower*1000))
            config_string += "\nruntime_qdelay_upper_thresh_ns {:d}".format(int(delay_upper*1000))
        if UTILIZATION_RANGE:
            config_string += "\nruntime_util_lower_thresh {:f}".format(utilization_lower)
            config_string += "\nruntime_util_upper_thresh {:f}".format(utilization_upper)
        if CORESYNC_ENABLE and antagonist == "none" and OVERLOAD_ALG == "breakwater":
            config_string += "\ncoresync_r {:d}".format(CORESYNC_R)
    else:
        config_name = "client.config"
        config_string = "host_addr {}".format(ip)\
                      + "\nhost_netmask {}".format(netmask)\
                      + "\nhost_gateway {}".format(gateway)\
                      + "\nruntime_kthreads {:d}".format(num_cores)

    if antagonist != "none":
        config_name = antagonist
        # config_string += "\nenable_gc 1"

    if spin:
        config_string += "\nruntime_spinning_kthreads {:d}".format(num_cores)
    else:
        config_string += "\nruntime_spinning_kthreads 0"

    if directpath:
        config_string += "\nenable_directpath 1"

    if disable_watchdog:
        config_string += "\ndisable_watchdog 1"

    cmd = "cd ~/{} && echo \"{}\" > {} "\
            .format(ARTIFACT_PATH,config_string, config_name)

    return execute_remote([conn], cmd, True)
### End of function definition ###

NUM_AGENT = len(AGENTS)
print ("number of agents: {:d}".format(NUM_AGENT))

# configure Shenango IPs for config
# TODO does each app on shenango need a unique server ip?
antagonist_ip = "192.168.1.7"
server_ip = "192.168.1.200"
client_ip = "192.168.1.100"
agent_ips = []
netmask = "255.255.255.0"
gateway = "192.168.1.1"

for i in range(NUM_AGENT):
    agent_ip = "192.168.1." + str(101 + i)
    agent_ips.append(agent_ip)

k = paramiko.RSAKey.from_private_key_file(KEY_LOCATION)
# connection to server
server_conn = paramiko.SSHClient()
server_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
server_conn.connect(hostname = SERVERS[0], username = USERNAME, pkey = k)

# connection to client
client_conn = paramiko.SSHClient()
client_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client_conn.connect(hostname = CLIENT, username = USERNAME, pkey = k)

# connections to agents
agent_conns = []
for agent in AGENTS:
    agent_conn = paramiko.SSHClient()
    agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    agent_conn.connect(hostname = agent, username = USERNAME, pkey = k)
    agent_conns.append(agent_conn)

# Clean-up environment
print("Cleaning up machines...")
cmd = "sudo killall -9 netbench & sudo killall -9 iokerneld && sudo killall -9 stress_shm_query"\
      " && sudo killall -9 stress"
execute_remote([server_conn, client_conn] + agent_conns,
               cmd, True, False)
sleep(1)

# Remove temporary output
cmd = "cd ~/{} && rm output.csv output.json antagonist.csv".format(ARTIFACT_PATH)
execute_remote([server_conn, client_conn], cmd, True, False)

# Distribuing config files
print("Distributing configs...")
# - server
cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../configs/*.h"\
        " {}@{}:~/{}/{}/breakwater/src/ >/dev/null"\
        .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
execute_local(cmd)
# - client
cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../configs/*.h"\
        " {}@{}:~/{}/{}/breakwater/src/ >/dev/null"\
        .format(KEY_LOCATION, USERNAME, CLIENT, ARTIFACT_PATH, KERNEL_NAME)
execute_local(cmd)
# - agents
for agent in AGENTS:
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../configs/*.h"\
            " {}@{}:~/{}/{}/breakwater/src/ >/dev/null"\
            .format(KEY_LOCATION, USERNAME, agent, ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

# adding to server
if IAS_DEBUG:
    print("Replacing ias.h")
    # - server
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/ias.h"\
            " {}@{}:~/{}/{}/iokernel/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

if True:
    print("replacing bw_server.c")
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/bw_server.c"\
            " {}@{}:~/{}/{}/breakwater/src/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

    print("replacing runtime defs.h")
    cmd = "sed -i \'s/#define RUNTIME_SCHED_MIN_POLL_US.*/#define RUNTIME_SCHED_MIN_POLL_US\\t\\t\\t{:d}/g\'"\
          " ../replace/defs.h".format(CALADAN_SCHED_POLL)
    execute_local(cmd)
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/defs.h"\
            " {}@{}:~/{}/{}/runtime/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

    print("replacing runtime sched.c")
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/sched.c"\
            " {}@{}:~/{}/{}/runtime/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

    print("replacing runtime kthread.c")
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/kthread.c"\
            " {}@{}:~/{}/{}/runtime/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

    print("replacing runtime cfg.c")
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/cfg.c"\
            " {}@{}:~/{}/{}/runtime/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

# Generating config files
print("Generating config files...")
generate_shenango_config(True, server_conn, server_ip, netmask, gateway,
                         NUM_CORES_LC, ENABLE_DIRECTPATH, SPIN_SERVER, DISABLE_WATCHDOG,
                         latency_critical=True, guaranteed_kthread=NUM_CORES_LC_GUARANTEED)
generate_shenango_config(True, server_conn, antagonist_ip, netmask, gateway,
                         NUM_CORES_ANTON, ENABLE_DIRECTPATH, False, DISABLE_WATCHDOG,
                         latency_critical=False, guaranteed_kthread=0, antagonist="antagonist.config")
generate_shenango_config(False, client_conn, client_ip, netmask, gateway,
                         NUM_CORES_CLIENT, ENABLE_DIRECTPATH, True, False)
for i in range(NUM_AGENT):
    generate_shenango_config(False, agent_conns[i], agent_ips[i], netmask,
                             gateway, NUM_CORES_CLIENT, ENABLE_DIRECTPATH, True, False)

# - server
cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/netbench.cc"\
        " {}@{}:~/{}/{}/breakwater/apps/netbench/ >/dev/null"\
        .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
execute_local(cmd)
# - client
cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/netbench.cc"\
        " {}@{}:~/{}/{}/breakwater/apps/netbench/ >/dev/null"\
        .format(KEY_LOCATION, USERNAME, CLIENT, ARTIFACT_PATH, KERNEL_NAME)
execute_local(cmd)
# - agents
for agent in AGENTS:
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/netbench.cc"\
        " {}@{}:~/{}/{}/breakwater/apps/netbench/ >/dev/null"\
        .format(KEY_LOCATION, USERNAME, agent, ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

if ENABLE_ANTAGONIST:
    # - server
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no ../replace/stress.cc"\
            " {}@{}:~/{}/{}/apps/netbench/"\
            .format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, KERNEL_NAME)
    execute_local(cmd)

if BREAKWATER_TIMESERIES:
    cmd = "cd ~/{}/{}/breakwater && sed -i \'s/#define SBW_TS_OUT.*/#define SBW_TS_OUT\\t\\t\\t true/\'"\
        " src/bw_server.c".format(ARTIFACT_PATH, KERNEL_NAME)
    execute_remote([server_conn], cmd)
else:
    cmd = "cd ~/{}/{}/breakwater && sed -i \'s/#define SBW_TS_OUT.*/#define SBW_TS_OUT\\t\\t\\t false/\'"\
        " src/bw_server.c".format(ARTIFACT_PATH, KERNEL_NAME)
    execute_remote([server_conn], cmd)

# Rebuild Shanango
print("Building Shenango/Caladan...")
cmd = "cd ~/{}/{} && make clean && make && make -C bindings/cc"\
        .format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote([server_conn, client_conn] + agent_conns, cmd, True)

# Build Breakwater
print("Building Breakwater...")
cmd = "cd ~/{}/{}/breakwater && make clean && make && make -C bindings/cc"\
        .format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote([server_conn, client_conn] + agent_conns, cmd, True)

# Build Netbench
print("Building netbench...")
cmd = "cd ~/{}/{}/breakwater/apps/netbench && make clean && make"\
        .format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote([server_conn, client_conn] + agent_conns, cmd, True)

# Execute IOKernel
iok_sessions = []
print("starting server IOKernel")
cmd = "cd ~/{}/{} && sudo ./iokerneld {} interval {:d} 2>&1 | ts %s > iokernel.node-0.log".format(ARTIFACT_PATH, KERNEL_NAME, SCHEDULER, CALADAN_INTERVAL)
iok_sessions += execute_remote([server_conn], cmd, False)

print("starting client/agent IOKernel")
cmd = "cd ~/{}/{} && sudo ./iokerneld simple 2>&1 | ts %s > iokernel.node-1.log".format(ARTIFACT_PATH, KERNEL_NAME)
iok_sessions += execute_remote([client_conn], cmd, False)

count = 2
for agent_node in agent_conns:
    cmd = "cd ~/{}/{} && sudo ./iokerneld simple 2>&1 | ts %s > iokernel.node-{:d}.log".format(ARTIFACT_PATH, KERNEL_NAME, count)
    iok_sessions += execute_remote([agent_node], cmd, False)
    count += 1
sleep(1)

# Output files info
curr_date = datetime.now().strftime("%m_%d_%Y")
curr_time = datetime.now().strftime("%H-%M-%S")
output_dir = "outputs/{}".format(curr_date)
if not os.path.isdir(output_dir):
   os.makedirs(output_dir)
run_dir = output_dir + "/" + curr_time
if not os.path.isdir(run_dir):
   os.makedirs(run_dir)

idx = 1
for offered_load in OFFERED_LOADS:

    print("Load = {:d}".format(offered_load))
    # Execute netbench application
    # - server
    print("\tExecuting netbench server...")
    cmd = "cd ~/{} && sudo ./{}/breakwater/apps/netbench/netbench"\
            " {} server.config server >stdout.out 2>&1"\
            .format(ARTIFACT_PATH, KERNEL_NAME, OVERLOAD_ALG)
    server_session = execute_remote([server_conn], cmd, False)
    server_session = server_session[0]
    sleep(1)

    # - client
    print("\tExecuting netbench client...")
    client_agent_sessions = []
    cmd = "cd ~/{} && sudo ./{}/breakwater/apps/netbench/netbench"\
            " {} client.config client {:d} {:f} {} {:d} {:d} {:d} {:d} {} {:d}"\
            " >stdout.out 2>&1".format(ARTIFACT_PATH, KERNEL_NAME, OVERLOAD_ALG, NUM_CONNS,
                    ST_AVG, ST_DIST, slo, NUM_AGENT, offered_load, LOADSHIFT, server_ip, 1)
    client_agent_sessions += execute_remote([client_conn], cmd, False)
    sleep(1)

    # - agent
    print("\tExecuting netbench agents...")
    cmd = "cd ~/{} && sudo ./{}/breakwater/apps/netbench/netbench"\
            " {} client.config agent {} {:d} >stdout.out 2>&1"\
            .format(ARTIFACT_PATH, KERNEL_NAME, OVERLOAD_ALG, client_ip, LOADSHIFT)
    client_agent_sessions += execute_remote(agent_conns, cmd, False)

    # Wait for some traffic begin
    sleep(3)

    # Start the antagonist
    if ENABLE_ANTAGONIST:
        # Start the antagonist server
        print("\tStarting server antagonist shared memory server...")
        cmd = "cd ~/{} && sudo ./{}/apps/netbench/stress antagonist.config init {:d} " \
              "{:d}".format(ARTIFACT_PATH, KERNEL_NAME, ANTON_SHM_KEY, ANTON_THREADS)
        server_stress_session = execute_remote([server_conn], cmd, False)
        sleep(1)
        # Start the antagonist
        print("\tStarting server antagonist...")
        cmd = "cd ~/{} && sudo ./{}/apps/netbench/stress antagonist.config work {:d} {:d} {:d}"\
                " {}".format(ARTIFACT_PATH, KERNEL_NAME, ANTON_SHM_KEY, ANTON_THREADS, ANTON_WORK_UNITS, ANTON_WORK_PARAM)
        server_stress_session += execute_remote([server_conn], cmd, False)
        anton_start_time = time()

    # Wait for some time before fetching antagonist stats
    sleep(3)

    if ENABLE_ANTAGONIST:
        # Dump the antagonist throughput
        anton_end_time = time()
        anton_duration = anton_end_time - anton_start_time
        print("\tFetching antagonist throughput...")
        cmd = "cd ~/{} && sudo ./{}/apps/netbench/stress antagonist.config dump {:d} " \
              "{:d} {:f} >> antagonist.csv 2>&1".format(ARTIFACT_PATH, KERNEL_NAME, ANTON_SHM_KEY, ANTON_THREADS, anton_duration)
        execute_remote([server_conn], cmd)
        sleep(1)
        # kill antagonist sessions
        print("\tKilling server antagonist...")
        cmd = "sudo killall -9 stress"
        execute_remote([server_conn], cmd, True, False) # TODO
        for sess in server_stress_session:
            sess.recv_exit_status()

    # Wait for client and agents
    print("\tWaiting for netbench client and agents...")
    for client_agent_session in client_agent_sessions:
        client_agent_session.recv_exit_status()

    # Kill server
    print("\tKilling netbench server...")
    cmd = "sudo killall -9 netbench"
    execute_remote([server_conn], cmd, True)
    server_session.recv_exit_status()

    sleep(1)

    # Collect the timeseries
    if BREAKWATER_TIMESERIES:
        print("Grabbing bw_server timeseries...")
        cmd = "mkdir -p {}/{}".format(run_dir, idx)
        execute_local(cmd)
        cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no {}@{}:~/{}/timeseries.csv {}/{}"\
              " >/dev/null".format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, run_dir, idx)
        execute_local(cmd)
        with open("{}/{}/timeseries.csv".format(run_dir, idx)) as original:
            data = original.read()
        execute_local("rm {}/{}/timeseries.csv".format(run_dir, idx))
        with open("{}/{}/timeseries.csv".format(run_dir, idx), "w+") as modified:
            modified.write("timestamp,credit_pool,credit_used,num_pending,num_drained,num_active,num_sess,delay,num_cores,avg_st,successes\n" + data)

    if DOWNLOAD_ALL_TASKS and not AVOID_LARGE_DOWNLOADS:
        print("Fetching raw output (all non rejected tasks)...")
        cmd = "mkdir -p {}/{}".format(run_dir, idx)
        execute_local(cmd)
        cmd = "rsync -azh --info=progress2 -e \"ssh -i {} -o StrictHostKeyChecking=no -o"\
              " UserKnownHostsFile=/dev/null\" {}@{}:~/{}/all_tasks.csv {}/{}".format(KEY_LOCATION,
                                                                                      USERNAME, CLIENT, ARTIFACT_PATH, run_dir, idx)
        execute_local(cmd)

    idx += 1

# Kill IOKernel
cmd = "sudo killall -9 iokerneld"
execute_remote([server_conn, client_conn] + agent_conns, cmd, True)

# Wait for IOKernel sessions
for iok_session in iok_sessions:
    iok_session.recv_exit_status()

# Close connections
server_conn.close()
client_conn.close()
for agent_conn in agent_conns:
    agent_conn.close()

# Create output directory
if not os.path.exists("outputs"):
    os.mkdir("outputs")

# Move output.csv and output.json
print("Collecting outputs...")
cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no {}@{}:~/{}/output.csv ./"\
        " >/dev/null".format(KEY_LOCATION, USERNAME, CLIENT, ARTIFACT_PATH)
execute_local(cmd)

output_prefix = "{}".format(OVERLOAD_ALG)
eric_prefix = "{}".format(OVERLOAD_ALG)

if OVERLOAD_ALG == "breakwater":
    eric_prefix += "_{:d}_{:d}".format(BW_TARGET, BW_THRESHOLD)
    output_prefix += "_{:d}_{:d}".format(BW_TARGET, BW_THRESHOLD)

if NUM_CORES_LC_GUARANTEED > 0:
    eric_prefix += "_guaranteed"

if SPIN_SERVER:
    output_prefix += "_spin"
    eric_prefix += "_spinning"

if DISABLE_WATCHDOG:
    output_prefix += "_nowd"

if ENABLE_ANTAGONIST:
    output_prefix += "_antagonist"
    eric_prefix += "_antagonist"
output_prefix += "_{:d}cores".format(NUM_CORES_LC)
output_prefix += "_{:d}load".format(OFFERED_LOADS[0])
# Assuming 16 cores consistently for now, so not adding cores to prefix
if LOADSHIFT:
    eric_prefix += "_loadshift"
else:
    eric_prefix += "_{:d}k".format(int(OFFERED_LOADS[0] / 1000))

eric_prefix += "_{:d}cores".format(NUM_CORES_LC)
eric_prefix += "_{:d}conns".format(NUM_CONNS)
eric_prefix += "_{:d}nodes".format(len(NODES))
if UTILIZATION_RANGE:
    eric_prefix += "_utilization_range_{}_{}".format(utilization_lower, utilization_upper)
elif DELAY_RANGE:
    eric_prefix += "_delay_range_{}_{}".format(delay_lower, delay_upper)
else:
    eric_prefix += "_{}".format(SCHEDULER)

output_prefix += "_{}_{:d}_nconn_{:d}".format(ST_DIST, ST_AVG, NUM_CONNS)

# Print Headers
header = "num_clients,offered_load,throughput,goodput,cpu"\
        ",min,mean,p50,p90,p99,p999,p9999,max"\
        ",reject_min,reject_mean,reject_p50,reject_p99"\
        ",p1_credit,mean_credit,p99_credit"\
        ",p1_q,mean_q,p99_q,mean_stime,p99_stime,server:rx_pps,server:tx_pps"\
        ",server:rx_bps,server:tx_bps,server:rx_drops_pps,server:rx_ooo_pps"\
        ",server:cupdate_rx_pps,server:ecredit_tx_pps,server:credit_tx_cps"\
        ",server:req_rx_pps,server:req_drop_rate,server:resp_tx_pps"\
        ",client:min_tput,client:max_tput"\
        ",client:ecredit_rx_pps,client:cupdate_tx_pps"\
        ",client:resp_rx_pps,client:req_tx_pps"\
        ",client:credit_expired_cps,client:req_dropped_rps"

cmd = "echo \"{}\" > {}/{}.csv".format(header, run_dir, curr_time + "-" + output_prefix)
execute_local(cmd)

cmd = "cat output.csv >> {}/{}.csv".format(run_dir, curr_time + "-" + output_prefix)
execute_local(cmd)

if ERIC_CSV_NAMING:
    cmd = "mv {}/{}.csv {}/{}.csv".format(run_dir, curr_time + "-" + output_prefix, run_dir, eric_prefix)
    execute_local(cmd)

if ENABLE_ANTAGONIST:
    print("Fetching antagonist output")
    cmd = "rsync -azh --info=progress2 -e \"ssh -i {} -o StrictHostKeyChecking=no -o"\
          " UserKnownHostsFile=/dev/null\" {}@{}:~/{}/antagonist.csv {}/".format(KEY_LOCATION, 
                                                                                        USERNAME, SERVERS[0], ARTIFACT_PATH, run_dir)
    execute_local(cmd)

# Remove temp outputs
cmd = "rm output.csv"
execute_local(cmd, False)


# TODO put these all in one folder on server so I can just fetch with one command
if not IAS_DEBUG or not AVOID_LARGE_DOWNLOADS:
    print("iokernel log node 0")
    cmd = "rsync -azh --info=progress2 -e \"ssh -i {} -o StrictHostKeyChecking=no -o"\
        " UserKnownHostsFile=/dev/null\" {}@{}:~/{}/caladan/iokernel.node-0.log {}/".format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, run_dir)
    execute_local(cmd)

print("stdout node 0")
cmd = "rsync -azh --info=progress2 -e \"ssh -i {} -o StrictHostKeyChecking=no -o"\
        " UserKnownHostsFile=/dev/null\" {}@{}:~/{}/stdout.out {}/ >/dev/null".format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, run_dir)
execute_local(cmd)

cmd = "mv {}/stdout.out {}/stdout_server.out".format(run_dir, run_dir)
execute_local(cmd)

print("iokernel log node 1")
cmd = "rsync -azh --info=progress2 -e \"ssh -i {} -o StrictHostKeyChecking=no -o"\
        " UserKnownHostsFile=/dev/null\" {}@{}:~/{}/caladan/iokernel.node-1.log {}/ >/dev/null".format(KEY_LOCATION, USERNAME, CLIENT, ARTIFACT_PATH, run_dir)
execute_local(cmd)

print("stdout client node 1")
cmd = "rsync -azh --info=progress2 -e \"ssh -i {} -o StrictHostKeyChecking=no -o"\
        " UserKnownHostsFile=/dev/null\" {}@{}:~/{}/stdout.out {}/ >/dev/null".format(KEY_LOCATION, USERNAME, CLIENT, ARTIFACT_PATH, run_dir)
execute_local(cmd)

print("gathering config options for this experiment")
config_dir = run_dir + "/config"
if not os.path.isdir(config_dir):
   os.makedirs(config_dir)

cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no {}@{}:~/{}/server.config {}/"\
        " >/dev/null".format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, config_dir)
execute_local(cmd)
cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no {}@{}:~/{}/client.config {}/"\
        " >/dev/null".format(KEY_LOCATION, USERNAME, CLIENT, ARTIFACT_PATH, config_dir)
execute_local(cmd)
if ENABLE_ANTAGONIST:
    cmd = "scp -P 22 -i {} -o StrictHostKeyChecking=no {}@{}:~/{}/antagonist.config {}/"\
        " >/dev/null".format(KEY_LOCATION, USERNAME, SERVERS[0], ARTIFACT_PATH, config_dir)
    execute_local(cmd)
cmd = "cp ../configs/bw_config.h {}/ && cp ../configs/bw2_config.h {}/".format(config_dir, config_dir)
execute_local(cmd)
script_config = "overload algorithm: {}\n".format(OVERLOAD_ALG)
script_config += "number of nodes: {}\n".format(len(NODES))
script_config += "number of connections: {}\n".format(NUM_CONNS)
script_config += "service time distribution: {}\n".format(ST_DIST)
script_config += "average service time: {}\n".format(ST_AVG)
script_config += "offered load: {}\n".format(OFFERED_LOADS[0])
script_config += "server cores: {}\n".format(NUM_CORES_LC)
script_config += "LC cores: {}\n".format(NUM_CORES_LC)
script_config += "LC guaranteed cores: {}\n".format(NUM_CORES_LC_GUARANTEED)
if SPIN_SERVER:
    script_config += "server cores spinning for LC\n"
script_config += "client cores: {}\n".format(NUM_CORES_CLIENT)
script_config += "caladan threshold: {}\n".format(CALADAN_THRESHOLD)
if ENABLE_ANTAGONIST:
    script_config += "antagonist threads: {}, work_unit {}, command line arg: {}\n".format(ANTON_THREADS, ANTON_WORK_UNITS, ANTON_WORK_PARAM)
script_config += "RTT: {}\n".format(NET_RTT)
script_config += "SLO: {}\n".format(slo)
script_config += "Connections: {:d}\n".format(NUM_CONNS)
script_config += "loadshift: {}\n".format(LOADSHIFT)
script_config += "scheduler: {}\n".format(SCHEDULER)
script_config += "allocation interval: {}\n".format(CALADAN_INTERVAL)
if CORESYNC_ENABLE:
    script_config += "coresync R: {}\n".format(CORESYNC_R)

cmd = "echo \"{}\" > {}/script.config".format(script_config, config_dir)
execute_local(cmd)

# produce the cores if applicable
if IAS_DEBUG and not AVOID_LARGE_DOWNLOADS:
    print("creating cores csv")
    cmd = "cd {} && python3 ../../../graph_scripts/create_corecsv.py".format(run_dir)
    execute_local(cmd)

if CSV_NAME_DIR:
    os.chdir(output_dir)
    if os.path.isdir(eric_prefix):
        print("error, desired directory name is already an output directory")
        exit()
    os.rename(curr_time, eric_prefix)
    os.chdir("..")

print("Done.")
