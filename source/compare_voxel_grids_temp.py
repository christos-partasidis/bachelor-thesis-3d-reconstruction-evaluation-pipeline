#
# The following script performs the following
# 1. Read voxel grids of ground truth and colmap
# 2. Extract from the voxels the coordinates and the values

#########################   MATCHING WITH INDEX   #########################
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)
## GROUND TRUTH
# 3. Find voxels in ground truth that exist in estimate (based on index)
# 4. Convert matched voxel coords to point cloud and voxel grid
# 5. Color found voxels with original (blue) and not found with red
# 6. Print comparison metrics for matching (based on index)

## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)
## COLMAP
# 7. Find voxels in estimate that exist in ground truth (based on index)
# 8. Convert matched voxel coords to point cloud and voxel grid
# 9. Color found voxels with original (green) and not found with red
# 10. Print comparison metrics for matching (based on index)

#########################   DISTANCE WITHOUT BOUNDARIES   #########################
## TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (wo boundaries)
## GROUND TRUTH
# 11. Find nearest voxel at estimated voxel grid for all ground truth voxels (wo boundaries)
# 12. Print comparison metrics for distances (wo boundaries)

## TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH (wo boundaries)
## COLMAP
# 13. Find nearest voxel at ground truth voxel grid for all colmap voxels (wo boundaries)
# 14. Print comparison metrics for distances (wo boundaries)

#########################   MATCHING WITH CENTERS AND BOUNDARIES   #########################
## TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# 15. Find voxels in ground truth that exist in estimate (based on center w boundaries)
# 16. Convert matched voxel coords to point cloud and voxel grid
# 17. Color found voxels with original (blue) and not found with red
# 18. Print comparison metrics for matching (based on center w boundaries)

## TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# 19. Find voxels in estimate that exist in ground truth (based on center w boundaries)
# 20. Convert matched voxel coords to point cloud and voxel grid
# 21. Color found voxels with original (green) and not found with red
# 22. Print comparison metrics for matching (based on center w boundaries)

#########################   DISTANCE WITH BOUNDARIES   #########################
## TEST_7 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)
## GROUND TRUTH
# 23. Find nearest voxel at estimated voxel grid for all ground truth voxels (with boundaries)
# 24. Print comparison metrics for distances (with boundaries)

## TEST_8 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)
## COLMAP
# 25. Find nearest voxel at ground truth voxel grid for all estimated voxels (with boundaries)
# 26. Print comparison metrics for distances (with boundaries)

## Configuration:

# argument 0: Path to ground truth voxel grid
# argument 1: Path to colmap voxel grid

# voxel_size: Is used when converting centers to point cloud and creating the
# corresponding voxel grid
voxel_size = 0.3

# Set the bound
bound = 0.3
    
# random_colors_TF color: 
# True the final voxel grid will have random colors,
# False the final voxel grid will have its original colors
random_colors_TF = False

# color_map_value:
# viridis: Blue - Low, Yellow - High
# RdYlGn_r: Green - Low, Red - High
color_map_value = "viridis"

# Debug Mode: True to run in debug mode, False to run in normal mode
debug = True # For visualizations
debug2 = False # For terminal prints

# Section: 0
# Importing modules
#===================================================================================
#===================================================================================
#===================================================================================
import open3d as o3d
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import os
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 1
# Read voxel grids of ground truth and colmap
# arg0: groundtruth, arg1: estimated(colmap)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 1 | compare_voxel_grids.py")
print("Read voxel grids of ground truth and colmap\n")
print("arg0: groundtruth, arg1: colmap")
# Read voxel grid of ground truth
voxel_grid_gt = o3d.io.read_voxel_grid("/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443/gt_cropped_objects/1_gt_Apple_Trunk1_light_voxelized.ply")
# Read voxel grid of colmap
voxel_grid_colmap = o3d.io.read_voxel_grid("/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443/colmap_a_cropped_objects/1_colmap_Apple_Trunk1_light_voxelized.ply")

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

# Section: 2
# Extract from the voxels the coordinates and the values
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 2 | compare_voxel_grids.py")
print("Extract from the voxels the coordinates and the values\n")

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

# Initialize lists to store coords and colors of the of the colmap voxels
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

## Section: 3
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)
## GROUND TRUTH
# Find voxels in ground truth that exist in estimate (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 3 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)")
print("GROUND TRUTH")
print("Find voxels in ground truth that exist in estimate (based on index)\n")

# Intialize empty list to store T/F for all ground truth voxels
# T: Found in estimated, F: Not found in estimated
found_voxels_TF = []

# Iterate through the coords of the ground truth
for coord_gt in coords_gt:
    # Initialize a flag to check if the voxel exists
    exists_in_estimated = False

    # Iterate through each voxel in the estimate
    for coord_colmap in coords_colmap:
        # Check if coordinates of the ground truth match the coordinates of the estimate
        if np.all(coord_gt == coord_colmap):
            exists_in_estimated = True
            break  # No need to check the rest of the estimated voxels once found

    # Append the result to the found_voxels_TF array
    found_voxels_TF.append(exists_in_estimated)

# Convert the list to a NumPy array for easier manipulation
found_voxels_TF = np.array(found_voxels_TF)

# Get number of found voxels
true_count = np.sum(found_voxels_TF)

# Print number of voxels found
print("Number of voxels found in ground truth:", true_count)

# Get coords that were found in the estimate
coords_gt_found = coords_gt[found_voxels_TF]

# Get values of coords that were found in the estimate
values_gt_found = values_gt[found_voxels_TF]
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 4
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)
## GROUND TRUTH
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 4 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)")
print("GROUND TRUTH")
print("Convert matched voxel coords to point cloud and voxel grid\n")

## Get centers of found voxels in estimate
# Initialize center array to store centers for each voxel
centers_found_gt = []

print("Getting centers of found voxels...")

# Get centers
for i, coord in enumerate(coords_gt_found):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_found_gt.append(vox_center)

print("Number of found centers in ground truth: ", len(centers_found_gt))

if debug2:
    print("coords_gt_found[0]: ", coords_gt_found[0])
    print("centers_found_gt[0]: ", centers_found_gt[0])

# Convert list to numpy array
centers_found_gt_np = np.asarray(centers_found_gt)

## Convert centers to point cloud

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

# Replicate centers 8 times
centers_found_gt_np_8 = []
for center in centers_found_gt_np:
    for i in range(8):
        centers_found_gt_np_8.append(center)

if debug2:
    print("Length of centers_np_8: ", len(centers_found_gt_np_8))

# Convert list to np array
centers_found_gt_np_8 = np.asarray(centers_found_gt_np_8)

# Replicate corner offsets len(coords_gt_found) times
corner_offsets_found_gt_8 = []

for i in range(len((coords_gt_found))):
    for point_offset in corner_offsets:
        corner_offsets_found_gt_8.append(point_offset)

if debug2:
    print("len(coords_gt_found): ", len(coords_gt_found))        
    print("len(corner_offsets_found_gt_8): ", len(corner_offsets_found_gt_8))

# Transform list to np array    
corner_offsets_found_gt_8 = np.asarray(corner_offsets_found_gt_8)

# Calculate the corner points
corner_points_found_gt = centers_found_gt_np_8 + corner_offsets_found_gt_8

if debug2:
    print("len(corner_points_found_gt): ", len(corner_points_found_gt))

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

unique_points_found_gt, num_duplicates, unique_indices_found_gt = remove_duplicate_points_and_count(corner_points_found_gt)

if debug2:
    print("Number of duplicates found at gt: ", num_duplicates)

# Initialize a point cloud
point_cloud = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud.points = o3d.utility.Vector3dVector(unique_points_found_gt)

# Sets random colors at the point cloud and voxel grid
if random_colors_TF:
    # Generate random colors for each point in the point cloud 
    # Get number of points
    num_points = len(point_cloud.points)
    # Generate random color for each point
    colors = np.random.randint(0, 255, size=(num_points, 3), dtype=np.uint8)
    # Set the colors to the point cloud
    point_cloud.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize the colors to the range [0, 1]
# Sets colors at the point cloud and voxel grid from the ground truth
else:
    # Initialize list to store replicated values 
    values_gt_found_8 = []

    # Iterate through each value (color) found
    for index, value in enumerate(values_gt_found):
        # Repeat 8 times
        for i in range(8):
            values_gt_found_8.append(value)

    if debug2:    
        print("len(values_gt_found_8: ", len(values_gt_found_8))

    # Convert list to numpy array
    values_gt_found_8 = np.asarray(values_gt_found_8)
    
    # Create a mask to select only the first occurrence of each unique point
    mask = np.full(len(values_gt_found_8), False)
    mask[unique_indices_found_gt] = True
    
    # Remove duplicates and get the count of duplicates
    values_gt_found_8 = values_gt_found_8[mask]
    
    point_cloud.colors = o3d.utility.Vector3dVector(values_gt_found_8) 
    
if debug:
    o3d.visualization.draw_geometries([point_cloud])

# Create a VoxelGrid from the PointCloud
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid])

#===================================================================================
#===================================================================================
#===================================================================================

## Section: 5
## TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)
## GROUND TRUTH
# Color found voxels with original (blue) and not found with red
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 5| compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)")
print("GROUND TRUTH")
print("Color found voxels with original (blue) and not found with red\n")

## Get centers gt
# Initialize centers array to store centers for each voxel of the ground truth
print("Getting ground truth centers....")

centers_gt = []

# Get centers of ground truth
for i, coord in enumerate(coords_gt):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_gt.append(vox_center)

# Convert list to numpy array
centers_gt = np.asarray(centers_gt)
    
# Initialize color list for storing color values of found and not found ground truth voxels
colors_test1_5 = []

# Iterate through all voxels of ground truth T/F
for index, is_true in enumerate(found_voxels_TF):
    if is_true:
        # Append original color (blue)
        colors_test1_5.append(values_gt[index])
    else:
        # Append modified color (red)
        #colors_test1_5.append(np.array([1.0, 0.0, 0.0]))
        # Append a random variation of red
        red_component = np.random.uniform(0.0, 1.0)   # Full red
        colors_test1_5.append(np.array([red_component, 0.0, 0.0]))

    
# Convert list to numpy array
colors_test1_5 = np.asarray(colors_test1_5)

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

if debug2:
    print("Number of duplicates_gt: ", num_duplicates_gt)

# Initialize a point cloud
point_cloud_gt = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_gt.points = o3d.utility.Vector3dVector(unique_points_gt)

# Initialize list to store replicated values 
values_gt_8 = []

# Iterate through each value(color) found
for index, value in enumerate(colors_test1_5):
    # Repeat 8 times
    for i in range(8):
        values_gt_8.append(value)

if debug2:    
    print("len(values_gt_8): ", len(values_gt_8))

# Convert list to numpy array
values_gt_8 = np.asarray(values_gt_8)

# Create a mask to select only the first occurrence of each unique point
mask = np.full(len(values_gt_8), False)
mask[unique_indices_gt] = True

# Remove duplicates and get the count of duplicates
values_gt_8 = values_gt_8[mask]

point_cloud_gt.colors = o3d.utility.Vector3dVector(values_gt_8) 

if debug:
    o3d.visualization.draw_geometries([point_cloud_gt])

# Create a VoxelGrid from the PointCloud
voxel_grid_gt = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_gt, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_gt])
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 6
# TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)
# GROUND TRUTH
# Print comparison metrics for matching (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 6 | compare_voxel_grids.py")
print("TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on index)")
print("GROUND TRUTH")
print("Print comparison metrics for matching (based on index)")

print("#Voxels at ground truth: ", len(coords_gt))
print("#Voxels at estimate: ", len(voxels_colmap))
print("#Voxels matched: ", len(coords_gt_found))
print("%Voxels matched: {:.2f}%".format((len(coords_gt_found)/len(coords_gt))*100))
print("")
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 7
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)
## COLMAP
# Find voxels in estimate that exist in ground truth (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 7 | compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)")
print("COLMAP")
print("Find voxels in estimate that exist in ground truth (based on index)\n")

# Intialize empty list to store T/F for all estimate voxels
# T: Found in ground truth, F: Not found in ground truth
found_voxels_TF_colmap = []

# Iterate through the coords of the estimate
for coord_colmap in coords_colmap:
    # Initialize a flag to check if the voxel exists
    exists_in_ground_truth = False

    # Iterate through each voxel in the ground truth
    for coord_gt in coords_gt:
        # Check if coordinates of the ground truth match the coordinates of the estimate
        if np.all(coord_colmap == coord_gt):
            exists_in_ground_truth = True
            break  # No need to check the rest of the ground truth voxels once found

    # Append the result to the found_voxels_TF array
    found_voxels_TF_colmap.append(exists_in_ground_truth)
    
# Convert the list to a NumPy array for easier manipulation
found_voxels_TF_colmap = np.array(found_voxels_TF_colmap)

# Get number of found voxels
true_count_colmap = np.sum(found_voxels_TF_colmap)

# Print number of voxels found in ground truth
print("Number of voxels found in ground truth:", true_count_colmap)

# Get coords that were found in the ground truth
coords_colmap_found = coords_colmap[found_voxels_TF_colmap]

# Get values of coords that were found in the ground truth
values_colmap_found = values_colmap[found_voxels_TF_colmap]
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 8
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)
## COLMAP
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 8 | compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)")
print("COLMAP")
print("Convert matched voxel coords to point cloud and voxel grid\n")

## Get centers of found colmap
# Initialize center array to store centers for each voxel
centers_found_colmap = []

print("Getting centers of found voxels in estimate...")

# Get centers
for i, coord in enumerate(coords_colmap_found):
    # Get voxel center
    vox_center = voxel_grid_colmap.get_voxel_center_coordinate(coord)
    # Append center
    centers_found_colmap.append(vox_center)

print("Number of found centers in colmap: ", len(centers_found_colmap))

# Convert list to numpy array
centers_found_colmap_np = np.asarray(centers_found_colmap)

## Convert centers to point cloud 

# Replicate centers 8 times
centers_found_colmap_np_8 = []
for center in centers_found_colmap_np:
    for i in range(8):
        centers_found_colmap_np_8.append(center)

if debug2:
    print("Length of centers_found_colmap_np_8: ", len(centers_found_colmap_np_8))

# Convert list to np array
centers_found_colmap_np_8 = np.asarray(centers_found_colmap_np_8)

# Replicate corner offsets len(coords_colmap_found) times
corner_offsets_found_colmap_8 = []

for i in range(len((coords_colmap_found))):
    for point_offset in corner_offsets:
        corner_offsets_found_colmap_8.append(point_offset)

if debug2:
    print("len(coords_colmap_found): ", len(coords_colmap_found))        
    print("len(corner_offsets_found_colmap_8): ", len(corner_offsets_found_colmap_8))

# Transform list to np array    
corner_offsets_found_colmap_8 = np.asarray(corner_offsets_found_colmap_8)

# Calculate the corner points
corner_points_found_colmap = centers_found_colmap_np_8 + corner_offsets_found_colmap_8

if debug2:
    print("len(corner_points_found_colmap): ", len(corner_points_found_colmap))

unique_points_found_colmap, num_duplicates, unique_indices_found_colmap = remove_duplicate_points_and_count(corner_points_found_colmap)

if debug2:
    print("Number of duplicates found at colmap: ", num_duplicates)

# Initialize a point cloud
point_cloud_found_colmap = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_found_colmap.points = o3d.utility.Vector3dVector(unique_points_found_colmap)

# Sets random colors at the point cloud and voxel grid
if random_colors_TF:
    # Generate random colors for each point in the point cloud 
    # Get number of points
    num_points = len(point_cloud_found_colmap.points)
    # Generate random color for each point
    colors = np.random.randint(0, 255, size=(num_points, 3), dtype=np.uint8)
    # Set the colors to the point cloud
    point_cloud_found_colmap.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize the colors to the range [0, 1]
# Sets colors at the point cloud and voxel grid from the ground truth
else:
    # Initialize list to store replicated values 
    values_colmap_found_8 = []

    # Iterate through each value (color) found
    for index, value in enumerate(values_colmap_found):
        # Repeat 8 times
        for i in range(8):
            values_colmap_found_8.append(value)

    if debug2:    
        print("len(values_colmap_found_8): ", len(values_colmap_found_8))

    # Convert list to numpy array
    values_colmap_found_8 = np.asarray(values_colmap_found_8)
    
    # Create a mask to select only the first occurrence of each unique point
    mask = np.full(len(values_colmap_found_8), False)
    mask[unique_indices_found_colmap] = True
    
    # Remove duplicates and get the count of duplicates
    values_colmap_found_8 = values_colmap_found_8[mask]
    
    point_cloud_found_colmap.colors = o3d.utility.Vector3dVector(values_colmap_found_8) 
    
if debug:
    o3d.visualization.draw_geometries([point_cloud_found_colmap])

# Create a VoxelGrid from the PointCloud
voxel_grid_found_colmap = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_found_colmap, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_found_colmap])

#===================================================================================
#===================================================================================
#===================================================================================

## Section: 9
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)
## COLMAP
# Color found voxels with original (green) and not found with red
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 9| compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)")
print("COLMAP")
print("Color found voxels with original (green) and not found with red\n")

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
    
# Initialize color list for storing color values of found and not found ground truth voxels
colors_test2_9 = []

# Iterate through all voxels of ground truth T/F
for index, is_true in enumerate(found_voxels_TF_colmap):
    if is_true:
        # Append original color (green)
        colors_test2_9.append(values_colmap[index])
    else:
        # Append modified color (red)
        colors_test2_9.append(np.array([1.0, 0.0, 0.0]))
    
# Convert list to numpy array
colors_test2_9 = np.asarray(colors_test2_9)

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

if debug2:
    print("Number of duplicates: ", num_duplicates)

# Initialize a point cloud
point_cloud_colmap = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_colmap.points = o3d.utility.Vector3dVector(unique_points_colmap)

# Initialize list to store replicated values 
values_colmap_8 = []

# Iterate through each value(color) found
for index, value in enumerate(colors_test2_9):
    # Repeat 8 times
    for i in range(8):
        values_colmap_8.append(value)

if debug2:    
    print("len(values_colmap_8): ", len(values_colmap_8))

# Convert list to numpy array
values_colmap_8 = np.asarray(values_colmap_8)

# Create a mask to select only the first occurrence of each unique point
mask = np.full(len(values_colmap_8), False)
mask[unique_indices_colmap] = True

# Remove duplicates 
values_colmap_8 = values_colmap_8[mask]

point_cloud_colmap.colors = o3d.utility.Vector3dVector(values_colmap_8) 

if debug:
    o3d.visualization.draw_geometries([point_cloud_colmap])

# Create a VoxelGrid from the PointCloud
voxel_grid_colmap = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_colmap, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_colmap])
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 10
## TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH
## COLMAP
# Print comparison metrics for matching
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 10 | compare_voxel_grids.py")
print("TEST_2: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on index)")
print("COLMAP")
print("Print comparison metrics for matching")

print("#Voxels at ground truth: ", len(coords_gt))
print("#Voxels at estimate: ", len(voxels_colmap))
print("#Voxels matched at colmap: ", len(coords_colmap_found))
print("%Voxels matched at colmap (%Precision = TP / (TP + FP) * 100): {:.2f}%".format((len(coords_colmap_found)/len(voxels_colmap))*100))
print("Recall = TP/(TP+FN): {:.2f}".format(len(coords_colmap_found)/(len(coords_colmap_found) + (len(coords_gt) - len(coords_colmap_found)))))
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 11
## TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (wo boundaries)
## GROUND TRUTH
# Find nearest voxel at estimated voxel grid for all ground truth voxels (wo boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 11 | compare_voxel_grids.py")
print("TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (wo boundaries)")
print("GROUND TRUTH")
print("Find nearest voxel at estimated voxel grid for all ground truth voxels (wo boundaries)\n")

# Have centers_gt and centers_colmap

## For each center in the ground truth find the center with the closest distance in colmap
print("Finding the closest distance for ground truth voxels...")

# Get number of centers in ground truth
num_gt_centers = len(centers_gt)

# Get number of centers in colmap
num_colmap_centers = len(centers_colmap)

# Initialize distances array to store minimum distance for each voxel in ground truth
distances_gt = np.empty(num_gt_centers)

# Initialize distance_index array to store for each voxel in ground truth
# the index of the voxel in colmap that corresponds to the minimum distance  
distance_index_gt = np.empty(num_gt_centers, dtype=int)

# Loop through each center in centers_gt
for i in range(num_gt_centers):
    gt_center = centers_gt[i]
    
    # Compute distances between gt_center and all centers in centers_colmap
    dist_to_colmap = np.array([distance.euclidean(gt_center, colmap_center) for colmap_center in centers_colmap])
    
    # Find the index of the closest center from centers_colmap
    min_distance_index = np.argmin(dist_to_colmap)
    
    # Store the closest distance and index
    distances_gt[i] = dist_to_colmap[min_distance_index]
    distance_index_gt[i] = min_distance_index

# Find minimum distance
minimum_distance_gt = np.min(distances_gt)

# Find maximimum distance
maximum_distance_gt = np.max(distances_gt)

## Convert distances into colors
print("Converting distances into colors...")
# matplotlib modules needed

# Define the colormap 
cmap = plt.get_cmap(color_map_value)  

# Normalize distances to [0, 1] to map them to the colormap
norm = plt.Normalize(minimum_distance_gt, maximum_distance_gt)

# Create a list of RGB values for each distance
colors = [cmap(norm(distance)) for distance in distances_gt]

# Convert the list of RGB values to a numpy array
color_array_gt = np.array(colors)

# Print the color array
if debug2:
    print(color_array_gt)

print("Displaying scatterplot color points")
# Scatterplot
plt.scatter(distances_gt, np.arange(len(distances_gt)), c=color_array_gt)
plt.xlabel("Ground truth | Distances ")
plt.ylabel("Index")
plt.show()

print("Displaying color points")
# Plot the colors for visualization
fig, ax = plt.subplots(figsize=(8, 2))
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Ground truth | Distance Color Map")
plt.show()

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

## Section: 12
## TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (wo boundaries)
## GROUND TRUTH
# Print comparison metrics for distances (wo boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 12 | compare_voxel_grids.py")
print("TEST_3 VOXEL DISTANCE GROUND TRUTH -> COLMAP (wo boundaries)")
print("GROUND TRUTH")
print("Print comparison metrics for distances (wo boundaries)\n")

# Print minimum and maximum distance
print("Minimum Distance: {:.2f}".format(minimum_distance_gt))
print("Maximum Distance: {:.2f}".format(maximum_distance_gt))

# Calculate Mean Absolute Error (MAE)
mae = np.mean(np.abs(distances_gt))
print("Distances Mean Absolute Error (MAE): {:.2f}".format(mae))

# Calculate Root Mean Square Error (RMSE)
rmse = np.sqrt(np.mean(distances_gt**2))
print("Distances Root Mean Square Error (RMSE): {:.2f}".format(rmse))

# Calculate Mean Squared Error (MSE)
mse = np.mean(distances_gt**2)
print("Distances Mean Squared Error (MSE): {:.2f}".format(mse))

#===================================================================================
#===================================================================================
#===================================================================================

## Section: 13
## TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH (wo boundaries)
## COLMAP
# Find nearest voxel at ground truth voxel grid for all colmap voxels (wo boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 13 | compare_voxel_grids.py")
print("TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH (wo boundaries)")
print("COLMAP")
print("Find nearest voxel at ground truth voxel grid for all colmap voxels (wo boundaries)\n")

# Have centers_gt and centers_colmap

## For each center in the colmap find the center with the closest distance in ground truth
print("Finding the closest distance for colmap voxels...")

# Get number of centers in ground truth
num_gt_centers = len(centers_gt)

# Get number of centers in colmap
num_colmap_centers = len(centers_colmap)

# Initialize distances array to store minimum distance for each voxel in colmap
distances_colmap = np.empty(num_colmap_centers)

# Initialize distance_index array to store for each voxel in colmap
# the index of the voxel in colmap that corresponds to the minimum distance  
distance_index_colmap = np.empty(num_colmap_centers, dtype=int)

# Loop through each center in centers_colmap
for i in range(num_colmap_centers):
    colmap_center = centers_colmap[i]
    
    # Compute distances between colmap_center and all centers in centers_gt
    dist_to_ground_truth = np.array([distance.euclidean(colmap_center, gt_center) for gt_center in centers_gt])
    
    # Find the index of the closest center from centers_gt
    min_distance_index = np.argmin(dist_to_ground_truth)
    
    # Store the closest distance and index
    distances_colmap[i] = dist_to_ground_truth[min_distance_index]
    distance_index_colmap[i] = min_distance_index

# Find minimum distance
minimum_distance_colmap = np.min(distances_colmap)

# Find maximimum distance
maximum_distance_colmap = np.max(distances_colmap)

## Convert distances into colors
print("Converting distances into colors...")
# matplotlib modules needed

# Define the colormap 
cmap = plt.get_cmap(color_map_value)  

# Normalize distances to [0, 1] to map them to the colormap
norm = plt.Normalize(minimum_distance_colmap, maximum_distance_colmap)

# Create a list of RGB values for each distance
colors = [cmap(norm(distance)) for distance in distances_colmap]

# Convert the list of RGB values to a numpy array
color_array_colmap = np.array(colors)

print("Displaying scatterplot color points")
# Scatterplot
plt.scatter(distances_colmap, np.arange(len(distances_colmap)), c=color_array_colmap)
plt.xlabel("Colmap | Distances ")
plt.ylabel("Index")
plt.show()

print("Displaying color points")
# Plot the colors for visualization
fig, ax = plt.subplots(figsize=(8, 2))
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Colmap | Distance Color Map")
plt.show()

## Convert voxel grid colmap -> to points -> add color -> convert back to voxel grid
## Convert centers to point cloud
# #9

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

## Section: 14
## TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH (wo boundaries)
## COLMAP
# Print comparison metrics for distances (wo boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 14 | compare_voxel_grids.py")
print("TEST_4 VOXEL DISTANCE COLMAP -> GROUND TRUTH (wo boundaries)")
print("COLMAP")
print("Print comparison metrics for distances (wo boundaries)\n")

# Print minimum and maximum distance
print("Minimum Distance: {:.2f}".format(minimum_distance_colmap))
print("Maximum Distance: {:.2f}".format(maximum_distance_colmap))

# Calculate Mean Absolute Error (MAE)
mae_colmap = np.mean(np.abs(distances_colmap))
print("Distances Mean Absolute Error (MAE): {:.2f}".format(mae_colmap))

# Calculate Root Mean Square Error (RMSE)
rmse_colmap = np.sqrt(np.mean(distances_colmap**2))
print("Distances Root Mean Square Error (RMSE): {:.2f}".format(rmse_colmap))

# Calculate Mean Squared Error (MSE)
mse_colmap = np.mean(distances_colmap**2)
print("Distances Mean Squared Error (MSE): {:.2f}".format(mse_colmap))
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 15
## TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Find voxels in ground truth that exist in estimate (based on center w boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 15 | compare_voxel_grids.py")
print("TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
print("GROUND TRUTH")
print("Find voxels in ground truth that exist in estimate (based on center w boundaries)\n")

# Intialize empty list to store T/F for all ground truth voxels
# T: Found in estimated, F: Not found in estimated
found_voxels_TF_gt_15 = []

# # Get number of centers in ground truth
# num_gt_centers = len(centers_gt)

# # Get number of centers in colmap
# num_colmap_centers = len(centers_colmap)

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
            dist_to_colmap_w_bound.append(maximum_distance_gt)
            
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

## Section: 16
## TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 16 | compare_voxel_grids.py")
print("TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
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

## Section: 17
## TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Color found voxels with original (blue) and not found with red
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 17| compare_voxel_grids.py")
print("TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
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
#===================================================================================

# Section: 18
## TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)
## GROUND TRUTH
# Print comparison metrics for matching (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 18 | compare_voxel_grids.py")
print("TEST_5: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)")
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

## Section: 19
## TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Find voxels in estimate that exist in ground truth (based on center w boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 19 | compare_voxel_grids.py")
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
            dist_to_ground_truth_w_bound.append(maximum_distance_colmap)
            
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

## Section: 20
## TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 20 | compare_voxel_grids.py")
print("TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
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

## Section: 21
## TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Color found voxels with original (blue) and not found with red
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 21| compare_voxel_grids.py")
print("TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
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
# Section: 22
## TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)
## COLMAP
# Print comparison metrics for matching (based on index)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 22 | compare_voxel_grids.py")
print("TEST_6: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)")
print("COLMAP")
print("Print comparison metrics for matching (based on center w boundaries)")

print("#Voxels at ground truth: ", len(coords_gt))
print("#Voxels at estimate: ", len(voxels_colmap))
print("#Voxels matched at colmap: ", len(coords_colmap_found_w_bound))

print("%Voxels matched at colmap : {:.2f}%".format((len(coords_colmap_found_w_bound)/len(coords_colmap))*100))
print("%Voxels matched at colmap (%Precision = TP / (TP + FP) * 100): {:.2f}%".format((len(coords_colmap_found_w_bound)/len(voxels_colmap))*100))
print("Recall = TP/(TP+FN): {:.2f}".format(len(coords_colmap_found_w_bound)/(len(coords_colmap_found_w_bound) + (len(coords_gt) - len(coords_colmap_found)))))
#===================================================================================
#===================================================================================
#===================================================================================

## Section: 23
## TEST_7 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)
## GROUND TRUTH
# Find nearest voxel at estimated voxel grid for all ground truth voxels (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 23 | compare_voxel_grids.py")
print("TEST_7 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)")
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

print("Displaying scatterplot color points")
# Scatterplot
plt.scatter(distances_gt_w_bound, np.arange(len(distances_gt_w_bound)), c=color_array_gt)
plt.xlabel("Ground truth | Distances with boundaries")
plt.ylabel("Index")
plt.show()

print("Displaying color points")
# Plot the colors for visualization
fig, ax = plt.subplots(figsize=(8, 2))
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Ground truth | Distance Color Map with boundaries")
plt.show()

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

## Section: 24
## TEST_7 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)
## GROUND TRUTH
# Print comparison metrics for distances (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 24 | compare_voxel_grids.py")
print("TEST_7 VOXEL DISTANCE GROUND TRUTH -> COLMAP (with boundaries)")
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

## Section: 25
## TEST_8 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)
## COLMAP
# Find nearest voxel at ground truth voxel grid for all estimated voxels (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 25 | compare_voxel_grids.py")
print("TEST_8 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)")
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

print("Displaying scatterplot color points")
# Scatterplot
plt.scatter(distances_colmap_w_bound, np.arange(len(distances_colmap_w_bound)), c=color_array_colmap)
plt.xlabel("Colmap | Distances with boundaries")
plt.ylabel("Index")
plt.show()

print("Displaying color points")
# Plot the colors for visualization
fig, ax = plt.subplots(figsize=(8, 2))
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Colmap | Distance Color Map with boundaries")
plt.show()

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

## Section: 26
## TEST_8 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)
## COLMAP
# Print comparison metrics for distances (with boundaries)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 26 | compare_voxel_grids.py")
print("TEST_8 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (with boundaries)")
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