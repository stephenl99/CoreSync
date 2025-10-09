###
### config_remote.py - configuration for remote servers
###
# First node is lead client, second i think is server
NODES = [
    "hp099.utah.cloudlab.us",
    "hp059.utah.cloudlab.us",
    "hp043.utah.cloudlab.us",
    "hp111.utah.cloudlab.us",
    "hp192.utah.cloudlab.us",
    "hp041.utah.cloudlab.us",
    "hp018.utah.cloudlab.us",
    "hp006.utah.cloudlab.us",
    "hp067.utah.cloudlab.us",
    "hp013.utah.cloudlab.us",
    "hp198.utah.cloudlab.us"
    
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
USERNAME = "slinder"
KEY_LOCATION = "/users/slinder/.ssh/id_rsa"

# Location of Shenango to be installed. With "", Shenango
# will be installed in the home direcotry
ARTIFACT_PARENT = ""

KERNEL_NAME = "caladan"

### End of config ###

ARTIFACT_PATH = ARTIFACT_PARENT
if ARTIFACT_PATH != "":
    ARTIFACT_PATH += "/"
ARTIFACT_PATH += "bw_caladan_memcached"


