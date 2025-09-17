###
### config_remote.py - configuration for remote servers
###

NODES = [
    "node-0.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-1.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-2.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-3.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-4.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-5.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-6.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-7.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-8.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-9.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
    "node-10.bhaskar3-268223.cc-profiler-pg0.utah.cloudlab.us",
]

# Public domain or IP of server
SERVERS = NODES[0:1]
# Public domain or IP of intemediate
INTNODES = []
# Public domain or IP of client and agents
CLIENTS = NODES[1:]
# Public domain or IP of client
CLIENT = CLIENTS[0]
AGENTS = CLIENTS[1:]

# Public domain or IP of monitor
MONITOR = ""

# Username and SSH credential location to access
# the server, client, and agents via public IP
USERNAME = "bhaskar3"
KEY_LOCATION = "/users/bhaskar3/.ssh/id_rsa"

# Location of Shenango to be installed. With "", Shenango
# will be installed in the home direcotry
ARTIFACT_PARENT = ""

KERNEL_NAME = "caladan"

### End of config ###

ARTIFACT_PATH = ARTIFACT_PARENT
if ARTIFACT_PATH != "":
    ARTIFACT_PATH += "/"
ARTIFACT_PATH += "bw_caladan_memcached"


