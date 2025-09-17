# CoreSync

This repository includes the code for [CoreSync (ICNP '25)](https://saeed.github.io/files/coresync-icnp25.pdf).

## General instructions to setup and run the tests

1. Deploy the nodes in the cluster
   * The easiest way to reproduce the paper result is using Cloudlab xl170 cluster. You
     can find a pre-configured disk image with `urn:publicid:IDN+utah.cloudlab.us+image+creditrpc-PG0:breakwater-xl170-2`.
     The Cloudlab profile for the same experiment environment (11 xl170 machines are
     connected to a single switch) as the paper can be found [here](https://www.cloudlab.us/p/CreditRPC/breakwater-compact/0).
2. SSH setup
   * Create SSH public-private key pairs on all the nodes using `ssh-keygen -t rsa`
   * Add the `~/.ssh/id_rsa.pub` of the node, where we are going to clone this
     repository and run the tests from (for e.g., node-1), to all the other nodes'
     `~/.ssh/authorized_keys`, including itself.
3. Clone this repository (on node-1)
   * `git clone git@github.com:GT-ANSR-Lab/CoreSync.git`
4. Init submodules (on node-1)
   * `./init_submodules.sh`
5. Update `config_remote.py` (on node-1)
   * Update `NODES` with the DNS names or IP addresses of the nodes in your test setup
      * `NODES[0]` is the server, rest of the nodes are the clients
      * `NODES[1]` is the master client, rest of the clients are secondary clients
   * Update `USERNAME` with the one that has access to all the nodes
   * Update `KEY_LOCATION` with the path to the private key `~/.ssh/id_rsa`
6. Install the required dependencies and scripts on all the nodes (from node-1)
   * `./setup_remote_caladan.py`
7. Run the tests (from node-1)
   * `./run_synthetic.py`


## ICNP 2025 artifact test scripts

`icnp_2025_scripts` directory gives the scripts for each result described in the paper.
The scripts are named according to the section they are discussed in the paper. For e.g.,
the results for *exponentially distributed synthetic workload with an average of 10us* is
discussed in section 4-B of the paper. Consequently the script name for that result is
`section_4B_exp_10us_run_test.py`.

One can run the test scripts for individual evaluation sections we have discussed in the paper.
But a single root script, `run_all_tests.sh` is provided to run all the tests at the same time.
One must update the `OUTPUT_DIR` variable to point to the directory where the results should be
dumped.

## CoreSync config details

CoreSync is implemented on top of Caladan and Breakwater. One could pick any core allocation
policy while starting the IOKernel and could technically pick any credit-based overload controller
implemented over Caladan. However, the applications that require CoreSync coordination between
the core allocator and the overload controller need to set `coresync_r` Caladan config option
to the desired *CoreSync parameter R (i.e., the proportionality parameter)*. This option instructs
the Caladan runtime to enable CoreSync for that specific application, with the provided
proportionality parameter.
