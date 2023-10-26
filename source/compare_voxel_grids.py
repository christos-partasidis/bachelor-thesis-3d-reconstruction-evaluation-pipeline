#
# The following script performs the following
# 1. Read voxel grids of ground truth and colmap
# 2. Extract from the voxels the coordinates and the values
## TEST_1: VOXEL MATCHING
# 3. Find voxels in ground truth that exist in estimate
# 4. Convert matched voxel coords to point cloud and voxel grid
# 5. Print comparison metrics for matching
## TEST_2: VOXEL DISTANCE
## 6. Calculate nearest voxel of all ground truth voxels

# Configuration:

# argument 0: Path to ground truth voxel grid
# argument 1: Path to colmap voxel grid

# voxel_size: Is used when converting centers to point cloud and creating the
# corresponding voxel grid
voxel_size = 0.3

# random_colors_TF color: True the final voxel grid will have random colors,
# False the final voxel grid will have its original colors
random_colors_TF = False

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
    o3d.visualization.draw_geometries([voxel_grid_gt])
    o3d.visualization.draw_geometries([voxel_grid_colmap])
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

# Section: 3
# Find voxels in ground truth that exist in estimate
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 3 | compare_voxel_grids.py")
print("Find voxels in ground truth that exist in estimate\n")

# Intialize empty list to store T/F for all ground truth voxels
# T: Found in estimated, F: Not found in estimated
found_voxels_TF = []

# Iterate through the coords of the ground truth
for coord_gt in coords_gt:
    # Initialize a flag to check if the voxel exists
    exists_in_estimated = False

    # Iterate through each voxel in the estimate
    for coord_colmap in coords_colmap:
        # Check if coordinates of the ground truth match the coordinates of the stimate
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

# Get values of coords that were found in the stimate
values_gt_found = values_gt[found_voxels_TF]
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 4
# Convert matched voxel coords to point cloud and voxel grid
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 4 | compare_voxel_grids.py")
print("Convert matched voxel coords to point cloud and voxel grid\n")
## Get centers
# Initialize center array to store centers for each voxel
centers = []

print("Getting centers...")

# Get centers
for i, coord in enumerate(coords_gt_found):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers.append(vox_center)

print("Number of centers: ", len(centers))
print("\nvoxel_size: ", voxel_size)

if debug2:
    print("coords_gt_found[0]: ", coords_gt_found[0])
    print("centers[0]: ", centers[0])

# Convert list to numpy array
centers_np = np.asarray(centers)

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
centers_np_8 = []
for center in centers_np:
    for i in range(8):
        centers_np_8.append(center)
if debug2:
    print("Length of centers_np_8: ", len(centers_np_8))

# Convert list to np array
centers_np_8 = np.asarray(centers_np_8)

# Replicate corner offsets len(coords_gt_found) times
corner_offsets_8 = []

for i in range(len((coords_gt_found))):
    for point_offset in corner_offsets:
        corner_offsets_8.append(point_offset)

if debug2:
    print("len(coords_gt_found): ", len(coords_gt_found))        
    print("len(corner_offsets_8): ", len(corner_offsets_8))

# Transform list to np array    
corner_offsets_8 = np.asarray(corner_offsets_8)

# Calculate the corner points
corner_points = centers_np_8 + corner_offsets_8

if debug2:
    print("len(corner_points): ", len(corner_points))

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

unique_points, num_duplicates, unique_indices = remove_duplicate_points_and_count(corner_points)

if debug2:
    print("Number of duplicates: ", num_duplicates)

# Initialize a point cloud
point_cloud = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud.points = o3d.utility.Vector3dVector(unique_points)

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

    # Iterate through each value(color) found
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
    mask[unique_indices] = True
    
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

# Section: 5
# Print comparison metrics
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 5 | compare_voxel_grids.py")
print("Print comparison metrics\n")

print("#Voxels at ground truth: ", len(coords_gt))
print("#Voxels at estimate: ", len(voxels_colmap))
print("#Voxels matched: ", len(coords_gt_found))
print("%Voxels matched: {:.2f}%".format((len(coords_gt_found)/len(coords_gt))*100))

#===================================================================================
#===================================================================================
#===================================================================================

# Section: 6
# Calculate nearest voxel and create a color map of all ground truth voxels
#===================================================================================
#===================================================================================
#===================================================================================
if debug2:
    print(len(coords_gt))
    print(coords_gt)
    print(type(coords_gt))
    print(type(coords_gt[0]))

## Get centers gt
# Initialize centers array to store centers for each voxel of the ground truth
centers_gt = []

# Get centers
for i, coord in enumerate(coords_gt):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_gt.append(vox_center)

if debug2:
    print("Length of centers_gt: ", len(centers_gt))
    print("voxel_size: ", voxel_size)
    print("centers_gt[0]: ", centers_gt[0])
    print("type(centers_gt): ", type(centers_gt))
    print("type(centers_gt[0]): ", type(centers_gt[0]))

# Convert list to numpy array
centers_gt = np.asarray(centers_gt)
print("type(centers_gt): ", type(centers_gt))

## Get centers colmap
if debug2:
    print(len(voxels_colmap))
    print(len(coords_colmap))
    print(coords_colmap)
    print(type(coords_colmap))
    print(type(coords_colmap[0]))

# Initialize center array to store centers for each voxel of the ground truth
centers_colmap = []
# Get centers
for i, coord in enumerate(coords_colmap):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_colmap.append(vox_center)

if debug2:
    print("Length of centers gt: ", len(centers_colmap))
    print("voxel_size: ", voxel_size)
    print("centers_colmap[0]: ", centers_colmap[0])
    print("type(centers_colmap): ", type(centers_colmap))
    print("type(centers_colmap[0]): ", type(centers_colmap[0]))

# Convert list to numpy array
centers_colmap = np.asarray(centers_colmap)
print("type(centers_colmap): ", type(centers_colmap))

## For each center in the ground truth find the closest (distance,index) in colmap
# distance module needed
# Initialize empty arrays to store distances and indices
num_gt_centers = len(centers_gt)
num_colmap_centers = len(centers_colmap)
distances = np.empty(num_gt_centers)
distance_index = np.empty(num_gt_centers, dtype=int)

# Loop through each center in centers_gt
for i in range(num_gt_centers):
    gt_center = centers_gt[i]
    
    # Compute distances between gt_center and all centers in centers_colmap
    dist_to_colmap = np.array([distance.euclidean(gt_center, colmap_center) for colmap_center in centers_colmap])
    
    # Find the index of the closest center in centers_colmap
    min_distance_index = np.argmin(dist_to_colmap)
    
    # Store the closest distance and index
    distances[i] = dist_to_colmap[min_distance_index]
    distance_index[i] = min_distance_index

# Find minimum distance
minimum_distance = np.min(distances)

# Find maxmimum distance
maximum_distance = np.max(distances)

# Print minimum and maximum distance
print("Minimum Distance: {:.2f}".format(minimum_distance))
print("Maximum Distance: {:.2f}".format(maximum_distance))

# Calculate Mean Absolute Error (MAE)
mae = np.mean(np.abs(distances))
print("Distances Mean Absolute Error (MAE): {:.2f}".format(mae))

# Calculate Root Mean Square Error (RMSE)
rmse = np.sqrt(np.mean(distances**2))
print("Distances Root Mean Square Error (RMSE): {:.2f}".format(rmse))

# Calculate Mean Squared Error (MSE)
mse = np.mean(distances**2)
print("Distances Mean Squared Error (MSE): {:.2f}".format(mse))

## Convert distances into colors
# matplotlib modules needed

# # Method 1 (commented out)
# # Define the colormap and normalization range
# cmap = plt.get_cmap('viridis')  # You can choose other colormaps as well
# norm = Normalize(vmin=min(distances), vmax=max(distances))

# # Create a ScalarMappable to map distances to colors
# sm = ScalarMappable(cmap=cmap, norm=norm)

# # Create an empty array to store the RGB colors
# colors = np.zeros((len(distances), 3))

# # Map distances to colors
# for i, distance in enumerate(distances):
#     rgba_color = sm.to_rgba(distance)  # Get RGBA color
#     colors[i] = rgba_color[:3]  # Extract RGB part

# Method 2
# Define the colormap (Reversed: Red-Yellow-Green)
cmap = plt.get_cmap("RdYlGn_r")  # Reversed Red-Yellow-Green colormap

# Normalize distances to [0, 1] to map them to the colormap
norm = plt.Normalize(distances.min(), distances.max())

# Create a list of RGB values for each distance
colors = [cmap(norm(distance)) for distance in distances]

# Convert the list of RGB values to a numpy array
color_array = np.array(colors)

# Print the color array
print(color_array)

# Example: Visualize the colors
plt.scatter(distances, np.arange(len(distances)), c=color_array)
plt.xlabel("Distances")
plt.ylabel("Index")
plt.show()

# Plot the colors for visualization
fig, ax = plt.subplots(figsize=(8, 2))
ax.imshow([colors], aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Distance Color Map")
plt.show()

## *** MUST CHECK METHOD 1 TO VERIFY VALIDITY OF METHOD 2

### Convert voxel grid gt -> to points -> add color -> convert back to voxel grid
## Get centers gt
# Initialize center array to store centers for each voxel
centers_gt = []

print("Getting centers of ground truth...", end='')

# Get centers
for i, coord in enumerate(coords_gt):
    # Get voxel center
    vox_center = voxel_grid_gt.get_voxel_center_coordinate(coord)
    # Append center
    centers_gt.append(vox_center)
    
print("Success!")

print("Number of ground truth centers: ", len(centers_gt))
print("\nvoxel_size: ", voxel_size)

# Convert list to numpy array
centers_gt = np.asarray(centers_gt)

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
centers_np_gt_8 = []
for center in centers_gt:
    for i in range(8):
        centers_np_gt_8.append(center)
print("Length of centers_np_gt_8: ", len(centers_np_gt_8))

# Convert list to np array
centers_np_8 = np.asarray(centers_np_8)

# Replicate corner offsets len(centers_gt) times
corner_offsets_gt_8 = []

for i in range(len((centers_gt))):
    for point_offset in corner_offsets:
        corner_offsets_gt_8.append(point_offset)
print("len(centers_gt): ", len(centers_gt))        
print("len(corner_offsets_gt_8): ", len(corner_offsets_gt_8))

# Transform list to np array    
corner_offsets_gt_8 = np.asarray(corner_offsets_gt_8)

# Calculate the corner points
corner_points_gt = centers_np_gt_8 + corner_offsets_gt_8

print("len(corner_points_gt): ", len(corner_points_gt))

unique_points_gt, num_duplicates, unique_indices_gt = remove_duplicate_points_and_count(corner_points_gt)

print("Number of duplicates: ", num_duplicates)

# Initialize a point cloud
point_cloud_gt = o3d.geometry.PointCloud()

# Set the points to the unique points
point_cloud_gt.points = o3d.utility.Vector3dVector(unique_points_gt)

print(len(unique_points_gt))

# Sets random colors at the point cloud and voxel grid
if random_colors_TF:
    # Generate random colors for each point in the point cloud 
    # Get number of points
    num_points = len(point_cloud_gt.points)
    # Generate random color for each point
    colors = np.random.randint(0, 255, size=(num_points, 3), dtype=np.uint8)
    # Set the colors to the point cloud
    point_cloud_gt.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize the colors to the range [0, 1]
# Sets colors at the point cloud and voxel grid from the ground truth
else:
    # Initialize list to store replicated values 
    color_array_8 = []

    # Iterate through each value(color)
    for index, value in enumerate(color_array):
        # Repeat 8 times
        for i in range(8):
            color_array_8.append(value)
        
    print("len(color_array_8: ", len(color_array_8))

    # Convert list to numpy array
    color_array_8 = np.asarray(color_array_8)
    
    # Create a mask to select only the first occurrence of each unique point
    mask = np.full(len(color_array_8), False)
    mask[unique_indices_gt] = True
    
    # Remove duplicates
    color_array_8 = color_array_8[mask]
    
    # Extract RGB from RGBA
    color_array_8 = color_array_8[:, :3]
    
    point_cloud_gt.colors = o3d.utility.Vector3dVector(color_array_8) 

print(len(color_array_8))
print(type(color_array_8))
print(type(color_array_8[0]))
print(color_array_8[0])

if debug:
    o3d.visualization.draw_geometries([point_cloud_gt])

# Create a VoxelGrid from the PointCloud
voxel_grid_gt = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud_gt, voxel_size)

if debug:
    o3d.visualization.draw_geometries([voxel_grid_gt])