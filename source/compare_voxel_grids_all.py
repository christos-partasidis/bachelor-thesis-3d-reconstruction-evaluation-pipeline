#
# The following script performs the following
# 0. Import modules and read arguments
# 1. Defining functions
# 2. Configuration
# 3. Read gt and colmap voxelized .ply files
# 4. Runs compare_voxel_grid_gt.py and compare_voxel_grid_colmap.py
#    for voxelized cropped objects found in the project


## Section: 0
## Import modules and read arguments
#===================================================================================
#===================================================================================
#===================================================================================
import os
import sys
import subprocess

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

if len(sys.argv) < 4 or len(sys.argv) > 6:
    print("Length of arguments: ", len(sys.argv))
    print("Usage: python compare_voxel_grids_all.py 1<path_to_project> 2<voxel_size>  3<bound> 4<random_colors_TF>(true or false) 5<color_map_value>")
    print("path_to_project: provide the path to the project (that contains colmap_a_cropped_objects and gt_cropped_objects)")
    print("voxel_size: provide the voxel size of the voxel grids")
    print("bound: provide the bound parameter that will be used to search around the center for matching and distance (+-bound)")
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


# 3. Read bound
# It us used for searching the area around a center both for matching and distance
# Attempt to convert bound (forth argument) to a float
try:
    bound = float(sys.argv[3])
except ValueError:
    print("Error: bound (third argument) must be a valid float.")
    sys.exit(1)

# 4. Read random_colors_TF
# True: the final voxel grids will have random colors,
# False: the final voxel grids will have original colors
random_colors_TF = False # default value

# Check if random_colors_TF is provided
if len(sys.argv) >= 5:
    random_colors_str = sys.argv[4]
    # Check if the string is "False" and assign the boolean value
    if random_colors_str.lower() == "true":
        random_colors_TF = True

    # Check if the string is "False" and assign the boolean value
    elif random_colors_str.lower() == "false":
        random_colors_TF = False

    else:
        # Handle the case where the input is neither "True" nor "False"
        raise ValueError("Error: random_colors_TF (forth argument) must be either true or false.")

# 5. Read color_map_value
# viridis:  Low:Blue, High: Yellow
# RdYlGn_r: Low:Green, Red - High
# check matplotlib doc for other
color_map_value = "viridis" # default value

if len(sys.argv) == 6:
    color_map_value = sys.argv[5]

# Print read arguments
print("==============================================================================================")
print("Read arguments")
print("1. path_to_project: ", path_to_project)
print("2. voxel_size: ", voxel_size)
print("3. bound: ", bound)
print("4. random_colors_TF: ", random_colors_TF)
print("5. color_map_value: ", color_map_value)
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 1
## Defining functions
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 1 | " + script_name)
print("Defining functions\n")

def find_voxelized_ply_files(directory_path):
    voxelized_ply_files = []

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".ply") and file.endswith("voxelized.ply"):
                # Combine the root and file to get the full path
                full_path = os.path.join(root, file)
                voxelized_ply_files.append(full_path)

    return voxelized_ply_files
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 2
## Configuration
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 2 | " + script_name)
print("Configuration\n")
# Debug Mode: True to run in debug mode, False to run in normal mode
debug = False # For visualizations
debug2 = False # For terminal prints

# Construct path to gt cropped objects directory
path_to_gt_cropped = os.path.join(path_to_project, "gt_cropped_objects")

# Check if ground truth cropped objects directory exists
if not os.path.exists(path_to_gt_cropped):
    print(f"The ground truth cropped objects directory '{path_to_gt_cropped}' does not exist. Please create one and place")
    print("the ground truth cropped objects (recommended: follow the main pipeline of the github repository)")
    sys.exit(1)

# Construct path to colmap cropped objects directory
path_to_colmap_cropped = os.path.join(path_to_project, "colmap_a_cropped_objects")

# Check if colmap cropped objects directory exists
if not os.path.exists(path_to_colmap_cropped):
    print(f"The colmap cropped objects directory '{path_to_colmap_cropped}' does not exist. Please create one and place")
    print("the colmap cropped objects (recommend: follow the main pipeline of the github repository)")
    sys.exit(1)
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 3
## Read gt and colmap voxelized .ply files
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 3 | " + script_name)
print("Read gt and colmap voxelized .ply files\n")
# Call the function to find the ground truth voxelized .ply files
voxelized_gt_ply_files = find_voxelized_ply_files(path_to_gt_cropped)

print("==============================================================================================")
print("ground truth: Found voxelized ply files")
# Print the list of full paths to ground truth voxelized .ply files
for file_path in voxelized_gt_ply_files:
    print(file_path)
    print("\n\n")

# Call the function to find the colmap voxelized .ply files
voxelized_colmap_ply_files = find_voxelized_ply_files(path_to_colmap_cropped)

print("==============================================================================================")
print("colmap: Found voxelized ply files")
# Print the list of full paths to colmap voxelized .ply files
for file_path in voxelized_colmap_ply_files:
    print(file_path)
    print("\n\n")

# Check if equal amount of cropped objects where found
print("Checking if equal amount of cropped objects where found in ground truth and colmap")
number_of_gt_cropped_objects = len(voxelized_gt_ply_files)
number_of_colmap_cropped_objects = len(voxelized_colmap_ply_files)
if number_of_gt_cropped_objects != number_of_colmap_cropped_objects:
    print("#number_of_gt_cropped_objects != #number_of_colmap_cropped_objects")
    print("Please check the corresponding directories and check whether a file is missing")
    sys.exit(1)
else:
    print("Equal amount found")

# Check if all correspondences exist
print("Checking if all correspondences exist")
# Replace _gt_ with _colmap_ from the path files of ground truth to perform the equality test
# and extract only the name from the paths
modified_voxelized_gt_ply_files = set(path.split("/")[-1].replace("_gt_", "_colmap_") for path in voxelized_gt_ply_files)
modified_voxelized_colmap_ply_files = set(path.split("/")[-1] for path in voxelized_colmap_ply_files)

# Initialize a variable to identify the test result
test_passed = True

for modified_path in modified_voxelized_gt_ply_files:
    
    if modified_path not in modified_voxelized_colmap_ply_files:
        test_passed = False
        modified_path_missing = modified_path
        break

if test_passed:
    print("All voxelized .ply correspondences found")
else:
    print(f"A voxelized .ply correspondence is missing for {modified_path_missing}")
    sys.exit(1)
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 4
## Runs compare_voxel_grid_gt.py and compare_voxel_grid_colmap.py
## for voxelized cropped objects found in the project
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 4 | " + script_name)
print("Runs compare_voxel_grid_gt.py and compare_voxel_grid_colmap.py")
print("for voxelized cropped objects found in the project\n")

for i in range(len(voxelized_gt_ply_files)):
    print(f"Iteration: {i}\n")
    
    # Construct the paths
    gt_path = voxelized_gt_ply_files[i]
    colmap_path = voxelized_gt_ply_files[i].replace("gt_cropped_objects", "colmap_a_cropped_objects")
    colmap_path = colmap_path.replace("_gt_", "_colmap_")

    # Print paths
    print("ground truth path:", gt_path)
    print("\n")
    print("colmap path:", colmap_path)
    print("\n")

    # Construct commands to execute
    run_gt_command = f"python3.10 compare_voxel_grid_gt.py {gt_path} {colmap_path} {voxel_size} {bound} {random_colors_TF} {color_map_value}"
    run_colmap_command = f"python3.10 compare_voxel_grid_colmap.py {gt_path} {colmap_path} {voxel_size} {bound} {random_colors_TF} {color_map_value}"

    ## SUBPROCESS GROUND TRUTH
    # Run the subprocess for ground truth compare and capture its output
    print("Running ground truth compare")

    run_subprocess_gt = subprocess.Popen(run_gt_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)

    # Read and print the output while the subprocess is running
    while run_subprocess_gt.poll() is None:
        output_gt = run_subprocess_gt.stdout.readline()
        print(output_gt, end='')

    # Once the subprocess is done, print any remaining output
    remaining_output_gt = run_subprocess_gt.communicate()[0]
    print(remaining_output_gt)
    print("Running ground truth compare done\n")

    # Check the return code of the subprocess 
    return_code_gt = run_subprocess_gt.returncode

    if return_code_gt == 0:
        print("Subprocess for ground truth exited normally\n")
    else:
        print(f"Subprocess for ground truth exited with return code {return_code_gt}. An error occurred.\n")
        sys.exit(1)

    # Waiting to finish the subprocess for ground truth
    run_subprocess_gt.wait()
    
    ## SUBPROCESS COLMAP
    # Run the subprocess for colmap compare and capture its output
    print("Running colmap compare")

    run_subprocess_colmap = subprocess.Popen(run_colmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)

    # Read and print the output while the subprocess is running
    while run_subprocess_colmap.poll() is None:
        output_colmap = run_subprocess_colmap.stdout.readline()
        print(output_colmap, end='')

    # Once the subprocess is done, print any remaining output
    remaining_output_colmap = run_subprocess_colmap.communicate()[0]
    print(remaining_output_colmap)
    print("Running colmap compare done")

    # Check the return code of the subprocess 
    return_code_colmap = run_subprocess_colmap.returncode

    if return_code_colmap == 0:
        print("Subprocess for colmap exited normally")
    else:
        print(f"Subprocess for colmap exited with return code {return_code_colmap}. An error occurred.")
        sys.exit(1)

    # Waiting to finish the subprocess for colmap
    run_subprocess_colmap.wait()

print("Successfully compared all cropped objects.")
#===================================================================================
#===================================================================================
#===================================================================================







