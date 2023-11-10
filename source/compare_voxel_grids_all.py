#
# The following script performs the following
# 0. Import modules and read arguments
# 1. Defining classes and functions
# 2. Configuration
# 3. Read gt and colmap voxelized .ply files
# 4. Runs compare_voxel_grid_gt.py and compare_voxel_grid_colmap.py
#    for voxelized cropped objects found in the project
# 5. Calculates and saves the total average metrics

## Section: 0
## Import modules and read arguments
#===================================================================================
#===================================================================================
#===================================================================================
import os
import sys
import subprocess
import glob

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
## Defining classes and functions
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 1 | " + script_name)
print("Defining classes and functions\n")

class DataObject:
    def __init__(self):
        self.title = ""
        self.value = ""

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
                    
def extract_specific_lines(root_dir):
    titles_to_extract = [
        "GT %Voxels matched",
        "GT Minimum Distance",
        "GT Maximum Distance",
        "GT Distances Mean Absolute Error (MAE)",
        "GT Distances Root Mean Square Error (RMSE)",
        "GT Distances Mean Squared Error (MSE)",
        "COLMAP %Voxels matched at colmap",
        "COLMAP Recall = TP/(TP+FN)",
        "COLMAP Minimum Distance",
        "COLMAP Maximum Distance",
        "COLMAP Distances Mean Absolute Error (MAE)",
        "COLMAP Distances Root Mean Square Error (RMSE)",
        "COLMAP Distances Mean Squared Error (MSE)"
    ]

    data_lists = {title: [] for title in titles_to_extract}
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            base_name, file_extension = os.path.splitext(filename)
            if base_name.endswith("_data") and base_name[:-5].isdigit() and file_extension == ".txt":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        for line in file:
                            line = line.strip()
                            if line.startswith("#"):
                                for title in titles_to_extract:
                                    if title in line:
                                        value = line.split(":")[1].strip()
                                        data_lists[title].append(value)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return data_lists    
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

# Construct path to metrics directory
path_to_metrics = os.path.join(path_to_project, "metrics_vox_" + str(voxel_size).replace(".", "_") + "_bound_" + str(bound).replace(".", "_"))
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

## Section: 5
## Calculates and saves the total average metrics
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 5 | " + script_name)
print("Calculates and saves the total average metrics")

# Check if metrics directory exists
if not os.path.exists(path_to_metrics):
    print(f"The metrics directory '{path_to_metrics}' does not exist.")
    sys.exit(1)


data_lists = extract_specific_lines(path_to_metrics)

if debug2:
    for title, values in data_lists.items():
        print(f"Title: {title}")
        print(f"Values: {values}")

#==============================================================================================
### GT metrics
#==============================================================================================
## Calculating average of GT %Voxels matched
avg_gt_voxels_matched = 0.0
sum_gt_voxels_matched = 0.0

# Summing GT %Voxels matched
for gt_perc_vox_match in data_lists["GT %Voxels matched"]:
    
    # Remove the '%' character and convert the remaining string to a float
    gt_perc_vox_match = float(gt_perc_vox_match.rstrip('%'))
    # Sum
    sum_gt_voxels_matched += gt_perc_vox_match

# Calculate average
avg_gt_voxels_matched = sum_gt_voxels_matched / len(data_lists["GT %Voxels matched"])
#==============================================================================================
## Find minimum of all GT Minimum Distances
# Convert the strings to floats and find the minimum float value
min_gt_distance = min(float(x) for x in data_lists["GT Minimum Distance"])

## Find maximum of all GT Minimum Distance
# Convert the strings to floats and find the maximum float value
max_gt_distance = max(float(x) for x in data_lists["GT Maximum Distance"])
#==============================================================================================
## Calculating average of GT Distances Mean Absolute Error (MAE)

avg_gt_mae = 0.0
sum_gt_mae = 0.0

# Summing GT Distances Mean Absolute Error (MAE)
for gt_mae in data_lists["GT Distances Mean Absolute Error (MAE)"]:
    
    # Convert the string to a float
    gt_mae = float(gt_mae)
    # Sum
    sum_gt_mae += gt_mae

# Calculate average
avg_gt_mae = sum_gt_mae / len(data_lists["GT Distances Mean Absolute Error (MAE)"])
#==============================================================================================
## Calculating average of GT Distances Root Mean Square Error (RMSE)
avg_gt_rmse = 0.0
sum_gt_rmse = 0.0

# Summing GT Distances Root Mean Square Error (RMSE)
for gt_rmse in data_lists["GT Distances Root Mean Square Error (RMSE)"]:
    
    # Convert the string to a float
    gt_rmse = float(gt_rmse)
    # Sum
    sum_gt_rmse += gt_rmse

# Calculate average
avg_gt_rmse = sum_gt_rmse / len(data_lists["GT Distances Root Mean Square Error (RMSE)"])
#==============================================================================================
## Calculating average of GT Distances Mean Squared Error (MSE)

avg_gt_mse = 0.0
sum_gt_mse = 0.0

# Summing GT Distances Mean Squared Error (MSE)
for gt_mse in data_lists["GT Distances Mean Squared Error (MSE)"]:
    
    # Convert the string to a float
    gt_mse = float(gt_mse)
    # Sum
    sum_gt_mse += gt_mse

# Calculate average
avg_gt_mse = sum_gt_mse / len(data_lists["GT Distances Mean Squared Error (MSE)"])
#==============================================================================================
### COLMAP metrics
#==============================================================================================
## Calculating average of COLMAP %Voxels matched at colmap

avg_colmap_voxels_matched = 0.0
sum_colmap_voxels_matched = 0.0

# Summing COLMAP %Voxels matched at colmap
for colmap_perc_vox_match in data_lists["COLMAP %Voxels matched at colmap"]:
    
    # Remove the '%' character and convert the remaining string to a float
    colmap_perc_vox_match = float(colmap_perc_vox_match.rstrip('%'))
    # Sum
    sum_colmap_voxels_matched += colmap_perc_vox_match

# Calculate average
avg_colmap_voxels_matched = sum_colmap_voxels_matched / len(data_lists["COLMAP %Voxels matched at colmap"])
#==============================================================================================
## Calculating average of COLMAP Recall = TP/(TP+FN)

avg_colmap_recall = 0.0
sum_colmap_recall = 0.0

# Summing COLMAP Recall = TP/(TP+FN)
for colmap_recall in data_lists["COLMAP Recall = TP/(TP+FN)"]:
    
    # Convert the string to a float
    colmap_recall = float(colmap_recall)
    # Sum
    sum_colmap_recall += colmap_recall

# Calculate average
avg_colmap_recall = sum_colmap_recall / len(data_lists["COLMAP Recall = TP/(TP+FN)"])
#==============================================================================================
## Find minimum of all COLMAP Minimum Distance
# Convert the strings to floats and find the minimum float value
min_colmap_distance = min(float(x) for x in data_lists["COLMAP Minimum Distance"])
#==============================================================================================
## Find maximum of all COLMAP Minimum Distance
# Convert the strings to floats and find the maximum float value
max_colmap_distance = max(float(x) for x in data_lists["COLMAP Maximum Distance"])
#==============================================================================================
## Calculating average of COLMAP Distances Mean Absolute Error (MAE)

avg_colmap_mae = 0.0
sum_colmap_mae = 0.0

# Summing COLMAP Distances Mean Absolute Error (MAE)
for colmap_mae in data_lists["COLMAP Distances Mean Absolute Error (MAE)"]:
    
    # Convert the string to a float
    colmap_mae = float(colmap_mae)
    # Sum
    sum_colmap_mae += colmap_mae

# Calculate average
avg_colmap_mae = sum_colmap_mae / len(data_lists["COLMAP Distances Mean Absolute Error (MAE)"])
#==============================================================================================
## Calculating average of COLMAP Distances Root Mean Square Error (RMSE)

avg_colmap_rmse = 0.0
sum_colmap_rmse = 0.0

# Summing COLMAP Distances Root Mean Square Error (RMSE)
for colmap_rmse in data_lists["COLMAP Distances Root Mean Square Error (RMSE)"]:
    
    # Convert the string to a float
    colmap_rmse = float(colmap_rmse)
    # Sum
    sum_colmap_rmse += colmap_rmse

# Calculate average
avg_colmap_rmse = sum_colmap_rmse / len(data_lists["COLMAP Distances Root Mean Square Error (RMSE)"])
#==============================================================================================
## Calculating average of COLMAP Distances Mean Squared Error (MSE)

avg_colmap_mse = 0.0
sum_colmap_mse = 0.0

# Summing COLMAP Distances Mean Squared Error (MSE)
for colmap_mse in data_lists["COLMAP Distances Mean Squared Error (MSE)"]:
    
    # Convert the string to a float
    colmap_mse = float(colmap_mse)
    # Sum
    sum_colmap_mse += colmap_mse

# Calculate average
avg_colmap_mse = sum_colmap_mse / len(data_lists["COLMAP Distances Mean Squared Error (MSE)"])
#==============================================================================================
# Define the content for "avg_metrics.txt"
content_avg_metrics = f"""
## GT
avg_gt_voxels_matched: {avg_gt_voxels_matched/100.0:.2f}
min_gt_distance: {min_gt_distance:.2f}
max_gt_distance: {max_gt_distance:.2f}
avg_gt_mae: {avg_gt_mae:.2f}
avg_gt_rmse: {avg_gt_rmse:.2f}
avg_gt_mse: {avg_gt_mse:.2f}

## COLMAP 
avg_colmap_voxels_matched: {avg_colmap_voxels_matched/100.0:.2f}
avg_colmap_recall: {avg_colmap_recall:.2f}
min_colmap_distance: {min_colmap_distance:.2f}
max_colmap_distance: {max_colmap_distance:.2f}
avg_colmap_mae: {avg_colmap_mae:.2f}
avg_colmap_rmse: {avg_colmap_rmse:.2f}
avg_colmap_mse: {avg_colmap_mse:.2f}
"""
#==============================================================================================
# Define the file path for "avg_metrics.txt" within the directory
path_to_avg_metrics = os.path.join(path_to_metrics, "avg_metrics.txt")

# Write the content to the file
with open(path_to_avg_metrics, "w") as file:
    file.write(content_avg_metrics)

# Print a confirmation message
print(f"avg_metrics.txt has been created in {path_to_avg_metrics}")
#===================================================================================
#===================================================================================
#===================================================================================





