#
# The following script performs the following
# 0. Importing modules and reading arguments
# 1. Run multiple times compare_voxel_grids_all.py but change the bound each time



# Section: 0
## Importing modules and reading arguments
#===================================================================================
#===================================================================================
#===================================================================================
import subprocess
import sys
import os

# Get the path to the current script
script_path = sys.argv[0]
# Get the name
script_name = os.path.basename(script_path)

print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 0 | " + script_name)
print("Importing modules and reading arguments\n")

print("Reading arguments")

if len(sys.argv) < 3 or len(sys.argv) > 5:
    print("Length of arguments: ", len(sys.argv))
    print("Usage: python compare_voxel_grids_all_multiple.py 1<path_to_project> 2<voxel_size> 3<random_colors_TF>(true or false) 4<color_map_value>")
    print("path_to_project: provide the path to the project (that contains colmap_a_cropped_objects and gt_cropped_objects)")
    print("voxel_size: provide the voxel size of the voxel grids")
    print("bound (statically set): static values have been set")
    print("random_colors_TF (optional): true -> random colors to voxel grids reconstructed to show matching voxels and distance coloring, false (default) -> original colors")
    print("color_map_value (optional): color mapping of distances is done using matplotlib and they are a lot of options")
    print("e.g. viridis (default): Low - Blue / High - Yellow, RdY1Gn: Low - Green / High - Red")
    sys.exit(1)

# 1. Read path to project
path_to_project = sys.argv[1]

# Check if project directory exists
if not os.path.exists(path_to_project):
    print(f"The project directory '{path_to_project}' does not exist. Please provide a valid path.")
    sys.exit(1)

# 2. Read voxel size
# It is used when converting centers to point cloud and creating the corresponding voxel grid
# Attempt to convert voxel_size to a float
try:
    voxel_size = float(sys.argv[2])
except ValueError:
    print("Error: voxel_size (second argument) must be a valid float")
    sys.exit(1)

# 3. Read random_colors_TF
# True: the final voxel grids will have random colors,
# False: the final voxel grids will have original colors
random_colors_TF = False # default value

# Check if random_colors_TF is provided
if len(sys.argv) >= 4:
    random_colors_str = sys.argv[3]
    # Check if the string is "False" and assign the boolean value
    if random_colors_str.lower() == "true":
        random_colors_TF = True

    # Check if the string is "False" and assign the boolean value
    elif random_colors_str.lower() == "false":
        random_colors_TF = False

    else:
        # Handle the case where the input is neither "True" nor "False"
        raise ValueError("Error: random_colors_TF (forth argument) must be either true or false.")

# 4. Read color_map_value
# viridis:  Low:Blue, High: Yellow
# RdYlGn_r: Low:Green, Red - High
# check matplotlib doc for other
color_map_value = "viridis" # default value

if len(sys.argv) == 5:
    color_map_value = sys.argv[4]

# Print read arguments
print("==============================================================================================")
print("Read arguments")
print("1. path_to_project: ", path_to_project)
print("2. voxel_size: ", voxel_size)
print("3. random_colors_TF: ", random_colors_TF)
print("4. color_map_value: ", color_map_value)
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 1
## Run multiple times compare_voxel_grids_all.py but change the bound each time
#===================================================================================
#===================================================================================
#===================================================================================
# List of values for the third argument
#third_argument_values = [0.05, 0.1, 0.2, 0.7, 0.9, 1.2, 1.5, 2.0, 2.5, 3.0]
third_argument_values = [0.2, 0.3, 0.4, 0.7, 0.9, 1.2, 1.5, 2.0, 2.5, 3.0]

# Construct command to execute
base_compare_all_command = f"python3.10 compare_voxel_grids_all.py {path_to_project}"

# Loop through the third argument values and execute the command
for third_arg_value in third_argument_values:
    # Build the full command with the current third argument value
    full_compare_all_command= f"{base_compare_all_command} {voxel_size} {third_arg_value} {random_colors_TF} {color_map_value}"
    
    print(f"Running command: {full_compare_all_command}")
    
    # Execute the command
    try:
        result = subprocess.run(full_compare_all_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Print the command's output
        print(result.stdout)

        # Check if the command terminated normally (return code 0)
        if result.returncode == 0:
            print("Command terminated normally.")
        else:
            # The command returned a non-zero exit code, indicating an error
            print(f"Command terminated with an error (return code {result.returncode}).")
            print(f"The following command caused the exit: {full_compare_all_command}") 
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
        print(f"The following command caused the exit: {full_compare_all_command}")
        sys.exit(1)

print("Successfull termination: compare_voxel_grid_all_multiple.py")
#===================================================================================
#===================================================================================
#===================================================================================




