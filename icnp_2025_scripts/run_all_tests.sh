#!/bin/bash

echo "####################################################"
echo "        Running Section 4-B (exponential 10us) Tests"
echo "####################################################"
sudo ./section_4B_exp_10us_run_test.py

echo "####################################################"
echo "        Running Section 4-B (bimodal 10us) Tests"
echo "####################################################"
sudo ./section_4B_bimod_10us_run_test.py

echo "####################################################"
echo "        Running Section 4-B (exponential 1us) Tests"
echo "####################################################"
sudo ./section_4B_exp_1us_run_test.py

echo "####################################################"
echo "        Running Section 4-B (bimodal 1us) Tests"
echo "####################################################"
sudo ./section_4B_bimod_1us_run_test.py

echo "####################################################"
echo "        Running Section 4-C (memcached) Tests"
echo "####################################################"
sudo ./section_4C_memcached_run_test.py

echo "####################################################"
echo "        Running Section 4-D (R sensitivity) Tests"
echo "####################################################"
sudo ./section_4D_R_sensitivity_run_test.py

echo "####################################################"
echo "        Running Section 4-D (clients sensitivity) Tests"
echo "####################################################"
sudo ./section_4D_num_clients_sensitivity_run_test.py
