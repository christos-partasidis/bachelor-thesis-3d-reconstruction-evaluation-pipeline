### The script performs the following:

#########################  GENERAL  #########################
# 0. Importing modules and reading arguments
# 1. Defining functions
# 2. Configuration
# 3. Read voxel grids of ground truth and estimated (colmap)
# 4. Extract from the voxels the coordinates and the values from both ground truth and colmap
# 5. Extract from the coordinates the ground truth and colmap centers
#    and create the respective point clouds and create the respective point clouds
 
#########################  VOXEL MATCHING WITH BOUNDARIES   #########################
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# 6. Find voxels in ground truth that exist in estimate (based on center w boundaries)
# 7. Convert matched voxel coords to point cloud and voxel grid
# 8. Color found voxels with original (blue) and not found with red
# 9. Print comparison metrics for matching (based on center w boundaries)

## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# 10. Find voxels in estimate that exist in ground truth (based on center w boundaries)
# 11. Convert matched voxel coords to point cloud and voxel grid
# 12. Color found voxels with original (green) and not found with red
# 13. Print comparison metrics for matching (based on center w boundaries)

#########################   DISTANCE CALCULATION WITH BOUNDARIES   #########################
## TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)
## GROUND TRUTH
# 14. Find nearest voxel at estimated voxel grid for all ground truth voxels (with boundaries)
# 15. Print comparison metrics for distances (with boundaries)

## TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)
## COLMAP
# 16. Find nearest voxel at ground truth voxel grid for all estimated voxels (with boundaries)
# 17. Print comparison metrics for distances (with boundaries)

## Section: 0
## Importing modules and reading arguments
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 0 | compare_voxel_grids.py")
print("Importing modules and reading arguments\n")

import open3d as o3d
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import os
import sys

print("Reading arguments")

if len(sys.argv) < 5 or len(sys.argv) > 7:
    print("Length of arguments: ", len(sys.argv))
    print("Usage: python compare_voxel_grids.py 1<path_to_gt_voxel_grid> 2<path_to_colmap_voxel_grid>  3<voxel_size> 4<bound> 5<random_colors_TF>(true or false) 6<color_map_value>")
    sys.exit(1)

# Read voxel grid of ground truth 
path_to_gt_voxel_grid = sys.argv[1]

if not os.path.exists(path_to_gt_voxel_grid):
    raise FileNotFoundError(f"The ground truth file '{path_to_gt_voxel_grid}' does not exist. Please provide a valid path.")

voxel_grid_gt = o3d.io.read_voxel_grid(path_to_gt_voxel_grid)

# Read voxel grid of colmap 
path_to_colmap_voxel_grid = sys.argv[2]

if not os.path.exists(path_to_colmap_voxel_grid):
    raise FileNotFoundError(f"The colmap file '{path_to_colmap_voxel_grid}' does not exist. Please provide a valid path.")

voxel_grid_colmap = o3d.io.read_voxel_grid(path_to_colmap_voxel_grid)

# voxel_size: It is used when converting centers to point cloud and creating the
# corresponding voxel grid
# Attempt to convert voxel_size (third argument) to a float
try:
    voxel_size = float(sys.argv[3])
except ValueError:
    print("Error: voxel_size (third argument) must be a valid float.")
    sys.exit(1)

# bound: It us used for searching the area around a center both for matching and distance
# Attempt to convert bound (forth argument) to a float
try:
    bound = float(sys.argv[4])
except ValueError:
    print("Error: bound (forth argument) must be a valid float.")
    sys.exit(1)

# random_colors_TF color: 
# True: the final voxel grids will have random colors,
# False: the final voxel grids will have original colors
random_colors_TF = False  # Default value for random_colors_TF

# Check if optional arguments are provided
if len(sys.argv) >= 6:
    random_colors_str = sys.argv[5]
    if random_colors_str.lower() == "true":
        random_colors_TF = True

    # Check if the string is "False" and assign the boolean value
    elif random_colors_str.lower() == "false":
        random_colors_TF = False

    else:
        # Handle the case where the input is neither "True" nor "False"
        raise ValueError("Error: random_colors_TF (fifth argument) must be either true or false.")
    
# color_map_value:
# viridis:  Low:Blue, High: Yellow
# RdYlGn_r: Low:Green, Red - High
# check matplotlib doc for other
color_map_value = "viridis" # Default value for color_map_value

if len(sys.argv) == 7:
    color_map_value = sys.argv[6]
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
print("Section: 1 | compare_voxel_grids.py")
print("Defining functions\n")
# In: An numpy array that contains numpy arrays that each represent a point
# Out: Removes all dublicates and returns the array, the amount of the dublicates, the corresponding indices of the uniques
def remove_duplicate_points_and_count(arr):
    unique_values, unique_indices = np.unique(arr, axis=0, return_index=True)
    
    # Create a mask to select only the first occurrence of each unique point
    mask = np.full(len(arr), False)
    mask[unique_indices] = True
    
    # Remove duplicates and get the count of duplicates
    unique_points = arr[mask]
    num_duplicates = len(arr) - len(unique_points)
    
    return unique_points, num_duplicates, unique_indices

# Function to extract parent folder and filename
def extract_folder_and_filename(path):
    folder = os.path.dirname(path)
    filename = os.path.basename(path)
    filename = filename.split(".")[0]  # Remove everything after the first dot
    return folder, filename

# Function to create absolute file path with ".png" extension
def create_png_path(folder, filename):
    return os.path.join(folder, filename + "_scatterplot.png")

# Function to create absolute file path with ".png" extension
def create_png_path_2(folder, filename):
    return os.path.join(folder, filename + "_color_points.png")
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
print("Section: 2 | compare_voxel_grids.py")
print("Configuration\n")

# Debug Mode: True to run in debug mode, False to run in normal mode
debug = True # For visualizations
debug2 = False # For terminal prints

# Get half voxel
voxel_half = voxel_size / 2

# Set corner offsets
corner_offsets = np.array([
    [-voxel_half, -voxel_half, -voxel_half],
    [voxel_half, -voxel_half, -voxel_half],
    [-voxel_half, voxel_half, -voxel_half],
    [voxel_half, voxel_half, -voxel_half],
    [-voxel_half, -voxel_half, voxel_half],
    [voxel_half, -voxel_half, voxel_half],
    [-voxel_half, voxel_half, voxel_half],
    [voxel_half, voxel_half, voxel_half]
])

# Extract parent folder and name of ground truth voxel_grid
parent_folder_gt, filename_gt = extract_folder_and_filename(path_to_gt_voxel_grid)
if debug:
    print("Extracting gt voxel grid path:")
    print("Parent folder gt:", parent_folder_gt)
    print("Filename gt:", filename_gt)

# Used to save the scatterplot
path_gt_scatterplot =  create_png_path(parent_folder_gt, filename_gt)

# Used to save the color points
path_gt_color_points =  create_png_path_2(parent_folder_gt, filename_gt)
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 3
## Read voxel grids of ground truth and estimated (colmap)
## arg0: groundtruth, arg1: estimated (colmap)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 3 | compare_voxel_grids.py")
print("Read voxel grids of ground truth and estimated (colmap)\n")
print("arg0: groundtruth, arg1: colmap")

# Visualize voxel grids
if debug:
    print("Visualizing ground truth voxel grid...")
    o3d.visualization.draw_geometries([voxel_grid_gt])
    print("Visualizing colmap voxel grid...")
    o3d.visualization.draw_geometries([voxel_grid_colmap])
    print("Visualizing combined ground truth (blue) and colmap (green) voxel grids...")
    o3d.visualization.draw_geometries([voxel_grid_gt, voxel_grid_colmap])

print("Ground truth voxel grid: ", voxel_grid_gt)
print("Colmap voxel grid: ", voxel_grid_colmap)
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 4
# Extract from the voxels the coordinates and the values from both ground truth and colmap
# and estimated
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 4 | compare_voxel_grids.py")
print("Extract from the voxels the coordinates and the values from both ground truth and colmap\n")
print("and estimated")

# Get ground truth voxels
voxels_gt = voxel_grid_gt.get_voxels()

# Initialize lists to store coords and colors of the ground truth voxels
coords_gt_list = []
values_gt_list = []

# Get coords and colors
for voxel in voxels_gt:
    coords_gt_list.append(voxel.grid_index)
    values_gt_list.append(voxel.color)
    
# Transform lists to np arrays    
coords_gt = np.asarray(coords_gt_list)
values_gt = np.asarray(values_gt_list)

# Get colmap voxels
voxels_colmap = voxel_grid_colmap.get_voxels()

# Initialize lists to store coords and colors of the colmap voxels
coords_colmap_list = []
values_colmap_list = []

# Get coords and colors
for voxel in voxels_colmap:
    coords_colmap_list.append(voxel.grid_index)
    values_colmap_list.append(voxel.color)
    
# Transform lists to np arrays   
coords_colmap = np.asarray(coords_colmap_list)
values_colmap = np.asarray(values_colmap_list)   

print("Number of ground truth coordinates: ", len(coords_gt_list))
print("Number of colmap coordinates: ", len(coords_colmap_list))

#===================================================================================
#===================================================================================
#===================================================================================

# Section: 5
# Extract from the coordinates the ground truth and colmap centers
# and create the respective point clouds
# Build voxel grids
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 5 | compare_voxel_grids.py")
print("Extract from the coordinates the ground truth and colmap centers")
print("and create the respective point clouds")
print("Build voxel grids")

## Get centers gt
# Initialize centers array to store centers for each voxel of the ground truth
centers_gt = []

print("Getting ground truth centers....")

# Get centers of ground truth
for i, coord in enumerate(coords_gt):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_gt.append(vox_center)

# Convert list to numpy array
centers_gt = np.asarray(centers_gt)

# Replicate centers 8 times
centers_gt_8 = []
for center in centers_gt:
    for i in range(8):
        centers_gt_8.append(center)
        
# Convert list to np array
centers_gt_8 = np.asarray(centers_gt_8)

# Replicate corner offsets len(centers_gt) times
corner_offsets_gt_8 = []

for i in range(len((centers_gt))):
    for point_offset in corner_offsets:
        corner_offsets_gt_8.append(point_offset)
        
# Transform list to np array    
corner_offsets_gt_8 = np.asarray(corner_offsets_gt_8)

# Calculate the corner points
corner_points_gt = centers_gt_8 + corner_offsets_gt_8

unique_points_gt, num_duplicates_gt, unique_indices_gt = remove_duplicate_points_and_count(corner_points_gt)

## Create ground truth point cloud
# Initialize a point cloud
point_cloud_gt = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_gt.points = o3d.utility.Vector3dVector(unique_points_gt)

## Get centers colmap
# Initialize centers array to store centers for each voxel of the ground truth
centers_colmap = []

print("Getting colmap centers....")

# Get centers of colmap
for i, coord in enumerate(coords_colmap):
    # Get voxel center
    vox_center = voxel_grid_colmap.get_voxel_center_coordinate(coord)
    # Append center
    centers_colmap.append(vox_center)

# Convert list to numpy array
centers_colmap = np.asarray(centers_colmap)

# Replicate centers 8 times
centers_colmap_8 = []
for center in centers_colmap:
    for i in range(8):
        centers_colmap_8.append(center)
        
# Convert list to np array
centers_colmap_8 = np.asarray(centers_colmap_8)

# Replicate corner offsets len(centers_colmap) times
corner_offsets_8 = []

for i in range(len((centers_colmap))):
    for point_offset in corner_offsets:
        corner_offsets_8.append(point_offset)
        
# Transform list to np array    
corner_offsets_8 = np.asarray(corner_offsets_8)

# Calculate the corner points
corner_points_colmap = centers_colmap_8 + corner_offsets_8

unique_points_colmap, num_duplicates, unique_indices_colmap = remove_duplicate_points_and_count(corner_points_colmap)

## Create colmap point cloud
# Initialize a point cloud
point_cloud_colmap = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_colmap.points = o3d.utility.Vector3dVector(unique_points_colmap)
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 6
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Find voxels in ground truth that exist in estimate (based on center w boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 6 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
print("GROUND TRUTH")
print("Find voxels in ground truth that exist in estimate (based on center w boundaries)\n")

# Initialize empty list to store T/F for all ground truth voxels
# T: Found in estimated, F: Not found in estimated
found_voxels_TF_gt_15 = []

# Get number of centers in ground truth
num_gt_centers = len(centers_gt)

# Get number of centers in colmap
num_colmap_centers = len(centers_colmap)

# Initialize distances array to store minimum distance for each voxel in ground truth
distances_gt_w_bound = np.empty(num_gt_centers)

# Initialize distance_index array to store for each voxel in ground truth
# the index of the voxel in colmap that corresponds to the minimum distance  
distance_index_gt_w_bound = np.empty(num_gt_centers, dtype=int)

# Bound is set
    
# Loop through each center in centers_gt
for i in range(num_gt_centers):
    gt_center = centers_gt[i]
    
    # Variable to check if found voxel within bounds
    found_within_bounds = False
    
    # Initialize list to store the distances with boundaries
    dist_to_colmap_w_bound = []
    
    # Compute distances between gt_center and all centers in centers_colmap
    for colmap_center in centers_colmap:
        
        if (gt_center[0] - bound <= colmap_center[0] <= gt_center[0] + bound and gt_center[1] - bound <= colmap_center[1] <= gt_center[1] + bound and gt_center[2] - bound <= colmap_center[2] <= gt_center[2] + bound):
            dist_to_colmap_w_bound.append(distance.euclidean(gt_center, colmap_center))
            found_within_bounds = True
        else:
            dist_to_colmap_w_bound.append(bound * 3)
            
    dist_to_colmap_w_bound = np.array(dist_to_colmap_w_bound)
    
    # # Compute distances between gt_center and all centers in centers_colmap
    # dist_to_colmap_w_bound = np.array([distance.euclidean(gt_center, colmap_center) for colmap_center in centers_colmap])
    
    # Find the index of the closest center from centers_colmap
    min_distance_index = np.argmin(dist_to_colmap_w_bound)
    
    # Store the closest distance and index
    distances_gt_w_bound[i] = dist_to_colmap_w_bound[min_distance_index]
    distance_index_gt_w_bound[i] = min_distance_index
    
    # Check if all voxels in estimated are out of the bounds
    if found_within_bounds:
        found_voxels_TF_gt_15.append(True)
    else:
        found_voxels_TF_gt_15.append(False)
    
# Convert the list to a NumPy array for easier manipulation
found_voxels_TF_gt_15 = np.array(found_voxels_TF_gt_15)

# Get number of found voxels
true_count_gt_15 = np.sum(found_voxels_TF_gt_15)

# Print number of voxels found
print("# of voxels in ground truth: ", len(coords_gt))
print("Number of voxels found in ground truth (based on center w boundaries): ", true_count_gt_15)

# Get coords that were found in the estimate
coords_gt_found_15 = coords_gt[found_voxels_TF_gt_15]

# Get values of coords that were found in the estimate
values_gt_found_15 = values_gt[found_voxels_TF_gt_15]
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 7
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 7 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
print("GROUND TRUTH")
print("Convert matched voxel coords to point cloud and voxel grid\n")

## Get centers of found voxels in estimate
# Initialize center array to store centers for each voxel
centers_found_gt_15 = []

print("Getting centers of found voxels (based on center w boundaries)...")

# Get centers
for i, coord in enumerate(coords_gt_found_15):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_found_gt_15.append(vox_center)

print("Number of found centers in ground truth: ", len(centers_found_gt_15))

# Convert list to numpy array
centers_found_gt_15 = np.asarray(centers_found_gt_15)

# Replicate centers 8 times
centers_found_gt_15_8 = []

for center in centers_found_gt_15:
    for i in range(8):
        centers_found_gt_15_8.append(center)

if debug2:
    print("Length of centers_found_gt_15_8: ", len(centers_found_gt_15_8))

# Convert list to np array
centers_found_gt_15_8 = np.asarray(centers_found_gt_15_8)

# Replicate corner offsets len(coords_gt_found) times
corner_offsets_found_gt_15_8 = []

for i in range(len((coords_gt_found_15))):
    for point_offset in corner_offsets:
        corner_offsets_found_gt_15_8.append(point_offset)

if debug2:
    print("len(coords_gt_found_15): ", len(coords_gt_found_15))        
    print("len(corner_offsets_found_gt_15_8): ", len(corner_offsets_found_gt_15_8))

# Transform list to np array    
corner_offsets_found_gt_15_8 = np.asarray(corner_offsets_found_gt_15_8)

# Calculate the corner points
corner_points_found_gt_15 = centers_found_gt_15_8 + corner_offsets_found_gt_15_8

if debug2:
    print("len(corner_points_found_gt_15): ", len(corner_points_found_gt_15))


unique_points_found_gt_15, num_duplicates_15, unique_indices_found_gt_15 = remove_duplicate_points_and_count(corner_points_found_gt_15)

if debug2:
    print("Number of duplicates found at gt 15: ", num_duplicates_15)

# Initialize a point cloud
point_cloud_gt_15 = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_gt_15.points = o3d.utility.Vector3dVector(unique_points_found_gt_15)

# Sets random colors at the point cloud and voxel grid
if random_colors_TF:
    # Generate random colors for each point in the point cloud 
    # Get number of points
    num_points = len(point_cloud_gt_15.points)
    # Generate random color for each point
    colors = np.random.randint(0, 255, size=(num_points, 3), dtype=np.uint8)
    # Set the colors to the point cloud
    point_cloud_gt_15.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize the colors to the range [0, 1]
# Sets colors at the point cloud and voxel grid from the ground truth
else:
    # Initialize list to store replicated values 
    values_gt_found_15_8 = []

    # Iterate through each value (color) found
    for index, value in enumerate(values_gt_found_15):
        # Repeat 8 times
        for i in range(8):
            values_gt_found_15_8.append(value)

    if debug2:    
        print("len(values_gt_found_15_8: ", len(values_gt_found_15_8))

    # Convert list to numpy array
    values_gt_found_15_8 = np.asarray(values_gt_found_15_8)
    
    # Create a mask to select only the first occurrence of each unique point
    mask = np.full(len(values_gt_found_15_8), False)
    mask[unique_indices_found_gt_15] = True
    
    # Remove duplicates and get the count of duplicates
    values_gt_found_15_8 = values_gt_found_15_8[mask]
    
    point_cloud_gt_15.colors = o3d.utility.Vector3dVector(values_gt_found_15_8) 
    
if debug:
    o3d.visualization.draw_geometries([point_cloud_gt_15])

# Create a VoxelGrid from the PointCloud
voxel_grid_gt_15 = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_gt_15, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_gt_15])
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 8
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Color found voxels with original (blue) and not found with red
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 8 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
print("GROUND TRUTH")
print("Color found voxels with original (blue) and not found with red\n")

## Get centers gt
# #5
    
# Initialize color list for storing color values of found and not found ground truth voxels
colors_test5_17 = []

# Iterate through all voxels of ground truth T/F
for index, is_true in enumerate(found_voxels_TF_gt_15):
    if is_true:
        # Append original color (blue)
        colors_test5_17.append(values_gt[index])
    else:
        # Append modified color (red)
        # colors_test5_17.append(np.array([1.0, 0.0, 0.0]))
        # Append a random variation of red
        red_component = np.random.uniform(0.0, 1.0)   # Full red
        colors_test5_17.append(np.array([red_component, 0.0, 0.0]))
    
# Convert list to numpy array
colors_test5_17 = np.asarray(colors_test5_17)

# Initialize a point cloud
point_cloud_gt_17 = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_gt_17.points = o3d.utility.Vector3dVector(unique_points_gt)

# Initialize list to store replicated values 
values_gt_17_8 = []

# Iterate through each value(color) found
for index, value in enumerate(colors_test5_17):
    # Repeat 8 times
    for i in range(8):
        values_gt_17_8.append(value)

if debug2:    
    print("len(values_gt_17_8): ", len(values_gt_17_8))

# Convert list to numpy array
values_gt_17_8 = np.asarray(values_gt_17_8)

# Create a mask to select only the first occurrence of each unique point
mask = np.full(len(values_gt_17_8), False)
mask[unique_indices_gt] = True

# Remove duplicates and get the count of duplicates
values_gt_17_8 = values_gt_17_8[mask]

point_cloud_gt_17.colors = o3d.utility.Vector3dVector(values_gt_17_8) 

if debug:
    o3d.visualization.draw_geometries([point_cloud_gt_17])

# Create a VoxelGrid from the PointCloud
voxel_grid_gt_17 = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_gt_17, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_gt_17])
#===================================================================================
#===================================================================================
#==================================================================================


# Section: 9
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Print comparison metrics for matching (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 9 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
print("GROUND TRUTH")
print("Print comparison metrics for matching (based on center w boundaries)")

print("#Voxels at ground truth: ", len(coords_gt))
print("#Voxels at estimate: ", len(voxels_colmap))
print("#Voxels matched: ", len(coords_gt_found_15))
print("%Voxels matched: {:.2f}%".format((len(coords_gt_found_15)/len(coords_gt))*100))
print("")
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 10
## TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Find voxels in estimate that exist in ground truth (based on center w boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 10 | compare_voxel_grids.py")
print("TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
print("COLMAP")
print("Find voxels in estimate that exist in ground truth (based on center w boundaries)\n")

# Intialize empty list to store T/F for all estimate voxels
# T: Found in ground truth, F: Not found in groudn truth
found_voxels_TF_colmap_w_bound = []

# Initialize distances array to store minimum distance for each voxel in estimate
distances_colmap_w_bound = np.empty(num_colmap_centers)

# Initialize distance_index array to store for each voxel in estimate
# the index of the voxel in ground truth that corresponds to the minimum distance  
distance_index_colmap_w_bound = np.empty(num_colmap_centers, dtype=int)

# Bound is set
    
# Loop through each center in centers_colmap
for i in range(num_colmap_centers):
    colmap_center = centers_colmap[i]
    
    # Variable to check if found voxel within bounds
    found_within_bounds = False
    
    # Initialize list to store the distances with boundaries
    dist_to_ground_truth_w_bound = []
    
    # Compute distances between colmap_center and all centers in centers_gt
    # with boundary
    for gt_center in centers_gt:
        
        if (colmap_center[0] - bound <= gt_center[0] <= colmap_center[0] + bound and colmap_center[1] - bound <= gt_center[1] <= colmap_center[1] + bound and colmap_center[2] - bound <= gt_center[2] <= colmap_center[2] + bound):
            dist_to_ground_truth_w_bound.append(distance.euclidean(colmap_center, gt_center))
            found_within_bounds = True
        else:
            dist_to_ground_truth_w_bound.append(bound * 3)
            
    dist_to_ground_truth_w_bound = np.array(dist_to_ground_truth_w_bound)
    
    # Find the index of the closest center from centers_gt
    min_distance_index = np.argmin(dist_to_ground_truth_w_bound)
    
    # Store the closest distance and index
    distances_colmap_w_bound[i] = dist_to_ground_truth_w_bound[min_distance_index]
    distance_index_colmap_w_bound[i] = min_distance_index
    
    # Check if all voxels in estimated are out of the bounds
    if found_within_bounds:
        found_voxels_TF_colmap_w_bound.append(True)
    else:
        found_voxels_TF_colmap_w_bound.append(False)
    
# Convert the list to a NumPy array for easier manipulation
found_voxels_TF_colmap_w_bound = np.array(found_voxels_TF_colmap_w_bound)

# Get number of found voxels
true_count_colmap_w_bound = np.sum(found_voxels_TF_colmap_w_bound)

# Print number of voxels found
print("# of voxels in estimate: ", len(coords_colmap))
print("Number of voxels found in estimate (based on center w boundaries): ", true_count_colmap_w_bound)

# Get coords that were found in the ground truth
coords_colmap_found_w_bound = coords_colmap[found_voxels_TF_colmap_w_bound]

# Get values of coords that were found in the ground truth
values_colmap_found_w_bound = values_colmap[found_voxels_TF_colmap_w_bound]
#===================================================================================
#===================================================================================
#===================================================================================


## Section: 11
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 11 | compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
print("COLMAP")
print("Convert matched voxel coords to point cloud and voxel grid\n")

## Get centers of found voxels in ground truth
# Initialize center array to store centers for each voxel
centers_found_colmap_w_bound = []

print("Getting centers of found voxels (based on center w boundaries)...")

# Get centers
for i, coord in enumerate(coords_colmap_found_w_bound):
    # Get voxel center
    vox_center = voxel_grid_colmap.get_voxel_center_coordinate(coord)
    # Append center
    centers_found_colmap_w_bound.append(vox_center)

print("Number of found centers in estimate: ", len(centers_found_colmap_w_bound))

# Convert list to numpy array
centers_found_colmap_w_bound = np.asarray(centers_found_colmap_w_bound)

# Replicate centers 8 times
centers_found_colmap_w_bound_8 = []

for center in centers_found_colmap_w_bound:
    for i in range(8):
        centers_found_colmap_w_bound_8.append(center)

if debug2:
    print("Length of centers_found_colmap_w_bound_8: ", len(centers_found_colmap_w_bound_8))

# Convert list to np array
centers_found_colmap_w_bound_8 = np.asarray(centers_found_colmap_w_bound_8)

# Replicate corner offsets len(coords_gt_found) times
corner_offsets_found_colmap_w_bound_8 = []

for i in range(len((coords_colmap_found_w_bound))):
    for point_offset in corner_offsets:
        corner_offsets_found_colmap_w_bound_8.append(point_offset)

# Transform list to np array    
corner_offsets_found_colmap_w_bound_8 = np.asarray(corner_offsets_found_colmap_w_bound_8)

# Calculate the corner points
corner_points_found_colmap_w_bound = centers_found_colmap_w_bound_8 + corner_offsets_found_colmap_w_bound_8

if debug2:
    print("len(corner_points_found_colmap_w_bound): ", len(corner_points_found_colmap_w_bound))


unique_points_found_colmap_w_bound, num_duplicates_colmap_w_bound, unique_indices_found_colmap_w_bound = remove_duplicate_points_and_count(corner_points_found_colmap_w_bound)

if debug2:
    print("Number of duplicates found at colmap w bound: ", num_duplicates_colmap_w_bound)

# Initialize a point cloud
point_cloud_colmap_w_bound = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_colmap_w_bound.points = o3d.utility.Vector3dVector(unique_points_found_colmap_w_bound)

# Sets random colors at the point cloud and voxel grid
if random_colors_TF:
    # Generate random colors for each point in the point cloud 
    # Get number of points
    num_points = len(point_cloud_colmap_w_bound.points)
    # Generate random color for each point
    colors = np.random.randint(0, 255, size=(num_points, 3), dtype=np.uint8)
    # Set the colors to the point cloud
    point_cloud_colmap_w_bound.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize the colors to the range [0, 1]
# Sets colors at the point cloud and voxel grid from the ground truth
else:
    # Initialize list to store replicated values 
    values_colmap_found_w_bound_8 = []

    # Iterate through each value (color) found
    for index, value in enumerate(values_colmap_found_w_bound):
        # Repeat 8 times
        for i in range(8):
            values_colmap_found_w_bound_8.append(value)

    if debug2:    
        print("len(values_colmap_found_w_bound_8: ", len(values_colmap_found_w_bound_8))

    # Convert list to numpy array
    values_colmap_found_w_bound_8 = np.asarray(values_colmap_found_w_bound_8)
    
    # Create a mask to select only the first occurrence of each unique point
    mask = np.full(len(values_colmap_found_w_bound_8), False)
    mask[unique_indices_found_colmap_w_bound] = True
    
    # Remove duplicates and get the count of duplicates
    values_colmap_found_w_bound_8 = values_colmap_found_w_bound_8[mask]
    
    point_cloud_colmap_w_bound.colors = o3d.utility.Vector3dVector(values_colmap_found_w_bound_8) 
    
if debug:
    o3d.visualization.draw_geometries([point_cloud_colmap_w_bound])

# Create a VoxelGrid from the PointCloud
voxel_grid_colmap_w_bound = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_colmap_w_bound, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_colmap_w_bound])
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 12
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Color found voxels with original (blue) and not found with red
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 12 | compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
print("COLMAP")
print("Color found voxels with original (green) and not found with red\n")

## Get centers gt
# #5
    
# Initialize color list for storing color values of found and not found ground truth voxels
colors_test6_21 = []

# Iterate through all voxels of ground truth T/F
for index, is_true in enumerate(found_voxels_TF_colmap_w_bound):
    if is_true:
        # Append original color (green)
        colors_test6_21.append(values_colmap[index])
    else:
        # Append modified color (red)
        colors_test6_21.append(np.array([1.0, 0.0, 0.0]))
    
# Convert list to numpy array
colors_test6_21 = np.asarray(colors_test6_21)

# Initialize a point cloud
point_cloud_colmap_w_bound_color = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_colmap_w_bound_color.points = o3d.utility.Vector3dVector(unique_points_found_colmap_w_bound)

# Initialize list to store replicated values 
values_colmap_w_bound_8 = []

# Iterate through each value(color) found
for index, value in enumerate(colors_test6_21):
    # Repeat 8 times
    for i in range(8):
        values_colmap_w_bound_8.append(value)

if debug2:    
    print("len(values_colmap_w_bound_8): ", len(values_colmap_w_bound_8))

# Convert list to numpy array
values_colmap_w_bound_8 = np.asarray(values_colmap_w_bound_8)

# Create a mask to select only the first occurrence of each unique point
mask = np.full(len(values_colmap_w_bound_8), False)
mask[unique_indices_found_colmap_w_bound] = True

# Remove duplicates and get the count of duplicates
values_colmap_w_bound_8 = values_colmap_w_bound_8[mask]

point_cloud_colmap_w_bound_color.colors = o3d.utility.Vector3dVector(values_colmap_w_bound_8) 

if debug:
    o3d.visualization.draw_geometries([point_cloud_colmap_w_bound_color])

# Create a VoxelGrid from the PointCloud
voxel_grid_colmap_w_bound_color = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_colmap_w_bound_color, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_colmap_w_bound_color])
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 13
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Print comparison metrics for matching (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 13 | compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
print("COLMAP")
print("Print comparison metrics for matching (based on center w boundaries)")

print("#Voxels at ground truth: ", len(coords_gt))
print("#Voxels at estimate: ", len(voxels_colmap))
print("#Voxels matched at colmap: ", len(coords_colmap_found_w_bound))

print("%Voxels matched at colmap : {:.2f}%".format((len(coords_colmap_found_w_bound)/len(coords_colmap))*100))
print("%Voxels matched at colmap (%Precision = TP / (TP + FP) * 100): {:.2f}%".format((len(coords_colmap_found_w_bound)/len(voxels_colmap))*100))
print("Recall = TP/(TP+FN): {:.2f}".format(len(coords_colmap_found_w_bound)/(len(coords_colmap_found_w_bound) + (len(coords_gt) - len(coords_colmap_found_w_bound)))))
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 14
## TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)
## GROUND TRUTH
# Find nearest voxel at estimated voxel grid for all ground truth voxels (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 14 | compare_voxel_grids.py")
print("TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)")
print("GROUND TRUTH")
print("Find nearest voxel at estimated voxel grid for all ground truth voxels (with boundaries)\n")

# Find minimum distance with boundaries
minimum_distance_gt_w_bound = np.min(distances_gt_w_bound)

# Find maximimum distance with boundaries
maximum_distance_gt_w_bound = np.max(distances_gt_w_bound)

## Convert distances into colors
print("Converting distances into colors...")

# Define the colormap 
cmap = plt.get_cmap(color_map_value)  

# Normalize distances to [0, 1] to map them to the colormap
norm = plt.Normalize(minimum_distance_gt_w_bound, maximum_distance_gt_w_bound)

# Create a list of RGB values for each distance
colors = [cmap(norm(distance)) for distance in distances_gt_w_bound]

# Convert the list of RGB values to a numpy array
color_array_gt = np.array(colors)

# Print the color array
if debug2:
    print(color_array_gt)

# Saving scatterplot
print("Saving scatterplot")
plt.scatter(distances_gt_w_bound, np.arange(len(distances_gt_w_bound)), c=color_array_gt)
plt.xlabel("Ground truth | Distances with boundaries")
plt.ylabel("Index")
#plt.show()
plt.savefig(path_gt_scatterplot)  
plt.close()  

# Save the colors for visualization
print("Saving color points")
fig, ax = plt.subplots(figsize=(8, 2))
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Ground truth | Distance Color Map with boundaries")
#plt.show()
#plt.savefig("ground_truth_color_points.png")  
plt.savefig(path_gt_color_points)
plt.close()  

## Convert voxel grid gt -> to points -> add color -> convert back to voxel grid
## Convert centers to point cloud
# #5

## Add color
# Initialize list to store replicated values 
color_array_gt_8 = []

# Iterate through each value(color)
for index, value in enumerate(color_array_gt):
    # Repeat 8 times
    for i in range(8):
        color_array_gt_8.append(value)

if debug2:
    print("len(color_array_gt_8): ", len(color_array_gt_8))

# Convert list to numpy array
color_array_gt_8 = np.asarray(color_array_gt_8)

# Create a mask to select only the first occurrence of each unique point
mask = np.full(len(color_array_gt_8), False)
mask[unique_indices_gt] = True

# Remove duplicates
color_array_gt_8 = color_array_gt_8[mask]

# Extract RGB from RGBA
color_array_gt_8 = color_array_gt_8[:, :3]

# Set colors to point cloud
point_cloud_gt.colors = o3d.utility.Vector3dVector(color_array_gt_8) 

if debug2:
    print(len(color_array_gt_8))
    print(type(color_array_gt_8))
    print(type(color_array_gt_8[0]))
    print(color_array_gt_8[0])

if debug:
    o3d.visualization.draw_geometries([point_cloud_gt])

print("Creating ground truth voxel grid from points...")
# Create a VoxelGrid from the PointCloud
voxel_grid_gt = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_gt, voxel_size)

o3d.visualization.draw_geometries([voxel_grid_gt])
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 15
## TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)
## GROUND TRUTH
# Print comparison metrics for distances (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 15 | compare_voxel_grids.py")
print("TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)")
print("GROUND TRUTH")
print("Print comparison metrics for distances (with boundaries)\n")

# Print minimum and maximum distance
print("Minimum Distance: {:.2f}".format(minimum_distance_gt_w_bound))
print("Maximum Distance: {:.2f}".format(maximum_distance_gt_w_bound))

# Calculate Mean Absolute Error (MAE) with bound
mae_gt_w_bound = np.mean(np.abs(distances_gt_w_bound))
print("Distances Mean Absolute Error (MAE): {:.2f}".format(mae_gt_w_bound))

# Calculate Root Mean Square Error (RMSE) with bound
rmse_gt_w_bound = np.sqrt(np.mean(distances_gt_w_bound**2))
print("Distances Root Mean Square Error (RMSE): {:.2f}".format(rmse_gt_w_bound))

# Calculate Mean Squared Error (MSE) with bound
mse_gt_w_bound = np.mean(distances_gt_w_bound**2)
print("Distances Mean Squared Error (MSE): {:.2f}".format(mse_gt_w_bound))

#===================================================================================
#===================================================================================
#===================================================================================

## Section: 16
## TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)
## COLMAP
# Find nearest voxel at ground truth voxel grid for all estimated voxels (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 16 | compare_voxel_grids.py")
print("TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)")
print("COLMAP")
print("Find nearest voxel at ground truth voxel grid for all estimated voxels (with boundaries)\n")

# Find minimum distance with boundaries
minimum_distance_colmap_w_bound = np.min(distances_colmap_w_bound)

# Find maximimum distance with boundaries
maximum_distance_colmap_w_bound = np.max(distances_colmap_w_bound)

## Convert distances into colors
print("Converting distances into colors...")

# Define the colormap 
cmap = plt.get_cmap(color_map_value)  

# Normalize distances to [0, 1] to map them to the colormap
norm = plt.Normalize(minimum_distance_colmap_w_bound, maximum_distance_colmap_w_bound)

# Create a list of RGB values for each distance
colors = [cmap(norm(distance)) for distance in distances_colmap_w_bound]

# Convert the list of RGB values to a numpy array
color_array_colmap = np.array(colors)

# Print the color array
if debug2:
    print(color_array_colmap)

print("here2")
# Saving scatter plot
# Scatterplot
plt.scatter(distances_colmap_w_bound, np.arange(len(distances_colmap_w_bound)), c=color_array_colmap)
plt.xlabel("Colmap | Distances with boundaries")
plt.ylabel("Index")
# plt.show()
plt.savefig("colmap_scatterplot.png")  
plt.close()  
print("her32")

print("Displaying color points")

# Save the colors for visualization
fig, ax = plt.subplots()
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Colmap | Distance Color Map with boundaries")
#plt.show()
plt.savefig("colmap_color_points.png")
plt.close()

## Convert voxel grid gt -> to points -> add color -> convert back to voxel grid
## Convert centers to point cloud
# #5

## Add color
# Initialize list to store replicated values 
color_array_colmap_8 = []

# Iterate through each value(color)
for index, value in enumerate(color_array_colmap):
    # Repeat 8 times
    for i in range(8):
        color_array_colmap_8.append(value)

if debug2:
    print("len(color_array_colmap_8): ", len(color_array_colmap_8))

# Convert list to numpy array
color_array_colmap_8 = np.asarray(color_array_colmap_8)

# Create a mask to select only the first occurrence of each unique point
mask = np.full(len(color_array_colmap_8), False)
mask[unique_indices_colmap] = True

# Remove duplicates
color_array_colmap_8 = color_array_colmap_8[mask]

# Extract RGB from RGBA
color_array_colmap_8 = color_array_colmap_8[:, :3]

# Set colors to point cloud
point_cloud_colmap.colors = o3d.utility.Vector3dVector(color_array_colmap_8) 

if debug2:
    print(len(color_array_colmap_8))
    print(type(color_array_colmap_8))
    print(type(color_array_colmap_8[0]))
    print(color_array_colmap_8[0])

if debug:
    o3d.visualization.draw_geometries([point_cloud_colmap])

print("Creating ground truth voxel grid from points...")
# Create a VoxelGrid from the PointCloud
voxel_grid_colmap = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_colmap, voxel_size)

o3d.visualization.draw_geometries([voxel_grid_colmap])
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 17
## TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)
## COLMAP
# Print comparison metrics for distances (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 17 | compare_voxel_grids.py")
print("TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)")
print("COLMAP")
print("Print comparison metrics for distances (with boundaries)\n")

# Print minimum and maximum distance
print("Minimum Distance: {:.2f}".format(minimum_distance_colmap_w_bound))
print("Maximum Distance: {:.2f}".format(maximum_distance_colmap_w_bound))

# Calculate Mean Absolute Error (MAE) with bound
mae_colmap_w_bound = np.mean(np.abs(distances_colmap_w_bound))
print("Distances Mean Absolute Error (MAE): {:.2f}".format(mae_colmap_w_bound))

# Calculate Root Mean Square Error (RMSE) with bound
rmse_colmap_w_bound = np.sqrt(np.mean(distances_colmap_w_bound**2))
print("Distances Root Mean Square Error (RMSE): {:.2f}".format(rmse_colmap_w_bound))

# Calculate Mean Squared Error (MSE) with bound
mse_colmap_w_bound = np.mean(distances_colmap_w_bound**2)
print("Distances Mean Squared Error (MSE): {:.2f}".format(mse_colmap_w_bound))

#===================================================================================
#===================================================================================
#===================================================================================