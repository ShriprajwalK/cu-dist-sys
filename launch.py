#!/usr/bin/python3
import subprocess

# The script you want to run
script_path_1 = "client_seller/client_seller.py"
#script_path_2 = "client_buyer/client_buyer.py"

# Number of parallel instances
num_instances = 1

processes = []

for _ in range(num_instances):
    # Launch the script and add the process to the list
    # Ensure python3 is the correct command to launch Python on your system
    process = subprocess.Popen(["python3", script_path_1])
    #process = subprocess.Popen(["python3", script_path_2])
    processes.append(process)

# Wait for all processes to complete
for process in processes:
    process.wait()
