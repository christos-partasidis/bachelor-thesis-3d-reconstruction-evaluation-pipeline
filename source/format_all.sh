#!/bin/bash

# Get the parent directory of the current directory
parent_dir=$(dirname "$(pwd)")

# Path to the "latest.txt" file in the "projects" directory
latest_file="$parent_dir/projects/latest.txt"

# Check if the file exists
if [ -f "$latest_file" ]; then
    # Read the first line of the file, remove white spaces, and store it in a variable
    latest_data=$(head -n 1 "$latest_file" | tr -d '[:space:]')
    
    # Print the data for verification
    echo "Data from latest.txt: $latest_data"
else
    echo "File $latest_file not found."
    exit 1
fi

# Call the colmap_to_format script with the latest_data as an argument
python3.10 colmap_to_format.py "$latest_data"

# Call the vulkan_to_format script with the latest_data as an argument
python3.10 vulkan_to_format.py "$latest_data"













