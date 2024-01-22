#!/usr/bin/env python3
import os
import paramiko
from util import *
from config_remote import *

k = paramiko.RSAKey.from_private_key_file(KEY_LOCATION)

# config check
if len(NODES) < 1:
    print("[ERROR] There is no server to configure.")
    exit()

# change default shell to bash
print("Changing default shell to bash...")
conns = []
for server in NODES:
    server_conn = paramiko.SSHClient()
    server_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    server_conn.connect(hostname = server, username = USERNAME, pkey = k)
    conns.append(server_conn)

execute_remote(conns, "sudo usermod -s /bin/bash {}".format(USERNAME), True, False)

for conn in conns:
    conn.close()

# connections to servers
conns = []
for server in NODES:
    server_conn = paramiko.SSHClient()
    server_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    server_conn.connect(hostname = server, username = USERNAME, pkey = k)
    conns.append(server_conn)

# clean up machines
print("Cleaning up machines...")
cmd = "sudo killall -9 cstate"
execute_remote(conns, cmd, True, False)

cmd = "sudo killall -9 iokerneld"
execute_remote(conns, cmd, True, False)

cmd = "sudo rm -rf ~/{}".format(ARTIFACT_PATH)
execute_remote(conns, cmd, True, False)

# distributing code-base
print("Distributing sources...")
repo_name = (os.getcwd().split('/'))[-1]
# - server
for server in NODES:
    cmd = "rsync -azh -e \"ssh -i {} -o StrictHostKeyChecking=no"\
            " -o UserKnownHostsFile=/dev/null\" --progress --exclude outputs/ ../{}/"\
            " {}@{}:~/{} >/dev/null"\
            .format(KEY_LOCATION, repo_name, USERNAME, server, ARTIFACT_PATH)
    execute_local(cmd)

# excute caladan build scripts
print("Executing caladan build all and build client scripts for main server node. Will make submodules and most components.")
cmd = "cd ~/{}/{} && ./build_all.sh".format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote(server_conn, cmd, True)

print("Executing caladan build client script for other connections")
cmd = "cd ~/{}/{} && ./build_client.sh".format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote(server_conn, cmd, True)

# settting up machines
# NOTE Inho has his own setup script here, it does also call the caladan setup script
print("Setting up machines...")
cmd = "cd ~/{}/{}/breakwater && sudo ./scripts/setup_machine.sh"\
        .format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote(conns, cmd, True)

print("Building Breakwater...")
cmd = "cd ~/{}/{}/breakwater && make clean && make -j16 &&"\
        " make -C bindings/cc".format(ARTIFACT_PATH, KERNEL_NAME)
execute_remote(conns, cmd, True)

# print("Setting up memcahced...")
# cmd = "cd ~/{}/shenango-memcached && ./version.sh && autoreconf -i"\
#         " && ./configure --with-shenango=../{}"\
#         .format(ARTIFACT_PATH, KERNEL_NAME)
# execute_remote(conns, cmd, True)

print("Done.")
