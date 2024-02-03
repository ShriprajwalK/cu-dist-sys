#!/bin/bash

python_file="client_buyer.py"
input_file="commands.txt"

# Check if the Python file and input file exist
if [ ! -f "$python_file" ]; then
  echo "Error: Python file not found at $python_file"
  exit 1
fi

if [ ! -f "$input_file" ]; then
  echo "Error: Input file not found at $input_file"
  exit 1
fi

# Execute the Python file with predefined input
echo "hi"
python "$python_file" < "$input_file"