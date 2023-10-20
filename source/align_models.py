#
# The following script performs the following tasks
# 1. Creates "align" directory within the project directory
# 2. Read poses of images from "image_poses.txt" from within the directory "output_dataset_txt"
# 3. Modifies lines and stores them in "ground_truth_geo_registration.txt" within "aligning" directory

# Section: 0
# Import modules
#===================================================================================
#===================================================================================
#===================================================================================
import os
import sys

print("Section: 0 - align_models.py")
print("Import modules")
#===================================================================================
#===================================================================================
#==================================================================================

# Section: 1
# Creates "align" directory
#===================================================================================
#===================================================================================
#===================================================================================
# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python align_models.py <path_to_project>")
    sys.exit(1)

# Get the directory path of the project from the command-line argument
path_to_dir = sys.argv[1]

# Create the 'aligning' directory inside 'path_to_dir'
aligning_dir = os.path.join(path_to_dir, "align")
os.makedirs(aligning_dir, exist_ok=True)

print("Section: 1 - align_models.py")
print('Created "align" directory')
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 2
# Read poses of images from "image_poses.txt" from within the directory "output_dataset_txt"
#===================================================================================
#===================================================================================
#===================================================================================
# Construct the path to 'image_poses.txt' inside 'output_dataset_txt'
image_poses_path = os.path.join(path_to_dir, "output_dataset_txt", "image_poses.txt")

# Check if 'image_poses.txt' exists
if not os.path.exists(image_poses_path):
    print("Error: 'image_poses.txt' does not exist in 'output_dataset_txt'")
    sys.exit(1)

# Read the content of 'image_poses.txt' line by line, ignoring the first line
with open(image_poses_path, 'r') as file:
    lines = file.readlines()[1:]

print("Section: 2 - align_models.py")
print('Read poses of images from "image_poses.txt')
# Section: 3
# Modifies lines and stores them in "ground_truth_geo_registration.txt" within "aligning" directory
#===================================================================================
#===================================================================================
#===================================================================================
# Process and store all lines in a single file
with open(os.path.join(aligning_dir, 'ground_truth_geo_registration.txt'), 'w') as output_file:
    for line in lines:
        # Split the line by commas and take the first four arguments
        values = line.strip().split(',')[:4]
        
        # Modify the first argument
        first_arg = values[0]
        parts = first_arg.split('_')
        if len(parts) == 2:
            prefix, number_ext = parts
            number, ext = os.path.splitext(number_ext)
            modified_first_arg = f"{number.zfill(6)}.png"
            values[0] = modified_first_arg

        # Join the first four arguments with spaces and add a newline
        modified_line = ' '.join(values) + '\n'
        
        # Write the modified line to the output file
        output_file.write(modified_line)

print("Section: 3 - align_models.py")
print('Modified lines and stored in "ground_truth_geo_registration.txt"')    

