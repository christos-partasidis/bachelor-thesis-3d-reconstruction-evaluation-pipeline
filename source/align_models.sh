#!/bin/bash

# Section: 0
# Read latest.txt
#==================================================================
#==================================================================
#==================================================================
echo ""
echo "Section: 0 - align_models.sh"
echo "Read latest.txt"
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
#==================================================================
#==================================================================
#==================================================================

# THE FOLLOWING SECTION IS USED TO RUN THE SCRIPT
# Section: 1
# Run align_models.py
#==================================================================
#==================================================================
#==================================================================
echo ""
echo "Section: 1 - align_models.sh"
echo "Run align_models.py"
path_to_project="../projects/$latest_data"

echo "Path to project: $path_to_project"

python3.10 align_models.py $path_to_project
#==================================================================
#==================================================================
#==================================================================

# Section: 2
# Run colmap model_aligner
#==================================================================
#==================================================================
#==================================================================
echo ""
echo "Section: 2 - align_models.sh"
echo "Run colmap model_aligner"

# Constructing the input_path

# Get the current directory path
current_dir=$(realpath .)

# Construct input_path
input_path=$(realpath "$current_dir/../projects/$latest_data/0")

# Construct output_path
output_path=$(realpath "$current_dir/../projects/$latest_data/align")

# Construct ref_images_path
ref_images_path=$(realpath "$current_dir/../projects/$latest_data/align/ground_truth_geo_registration.txt")

# Print input_path
echo "input_path: $input_path"

# Print output_path
echo "output_path: $output_path"

# Print ref_images_path
echo "ref_images_path: $ref_images_path"

colmap model_aligner --input_path $input_path --output_path $output_path --ref_images_path $ref_images_path --ref_is_gps no --robust_alignment_max_error 0.1

