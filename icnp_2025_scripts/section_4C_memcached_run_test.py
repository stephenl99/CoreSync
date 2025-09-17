#!/usr/bin/env python3

import os
from time import sleep, time
import sys

# Directory to store the test results
OUTPUT_DIR = "/path/to/your/directory"

# Remove the output directory if it exists
os.system("sudo rm -rf {}".format(OUTPUT_DIR))

# Create the output directory
os.system("sudo mkdir -p {}".format(OUTPUT_DIR))

# Core allocation policies to test
POLICIES = [
    "shenango",
    "caladan1",
    "util_range",
    "delay_range1",
    "coresync1",
    "coresync2",
    "coresync3",
    "coresync4",
]

# Run the tests
for policy in POLICIES:
    # Remove the output directory if it exists
    os.system("sudo rm -rf ./outputs")

    # Run the test case
    os.system("sudo ./section_4C_memcached_param_script.py {}".format(policy))

    # Move the results for the test case to results directory
    os.system("sudo mkdir -p {}/{}".format(OUTPUT_DIR, policy))
    os.system("sudo mv ./outputs/* {}/{}".format(OUTPUT_DIR, policy))
