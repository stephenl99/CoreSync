#!/usr/bin/env python3

import os
from time import sleep, time
import sys

if len(sys.argv) < 2:
    print("usage: section_4D_R_sensitivity_run_test.py <output_dir>")
    sys.exit(1)

# Directory to store the test results
OUTPUT_DIR = "{}/{}".format(sys.argv[1], "section_4D_R_sensitivity")


# Remove the output directory if it exists
os.system("sudo rm -rf {}".format(OUTPUT_DIR))

# Create the output directory
os.system("sudo mkdir -p {}".format(OUTPUT_DIR))

# Core allocation policies to test
POLICIES = [
    "coresync_5",
    "coresync_10",
    "coresync_15",
    "coresync_20",
    "coresync_50",
    "coresync_100",
]

# Run the tests
for policy in POLICIES:
    # Remove the output directory if it exists
    os.system("sudo rm -rf ./outputs")

    # Run the test case
    os.system("sudo ./section_4D_R_sensitivity_param_script.py {}".format(policy))

    # Move the results for the test case to results directory
    os.system("sudo mkdir -p {}/{}".format(OUTPUT_DIR, policy))
    os.system("sudo mv ./outputs/* {}/{}".format(OUTPUT_DIR, policy))
