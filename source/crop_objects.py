#
# The following script performs the following tasks
# 1. Read object names (under criteria) used for the creation of the scene -> selected_objects (in model_def_list.txt) 
# 2. Read poses of selected_objects (in model_poses_list.txt)
# 3. Read the ground point cloud
# 4. Reads all .ply from vrg_crop_gen/resources/model (or other specified directory) and stores for each selected
#    object their corresponding file path for the raw .ply and the _bounding_box.ply
# 5. Combines and visualizes aabbs(both pcd and mesh) of selected_objects with ground truth point cloud <br>


# Section: 0
# Importing modules
import sys
import os
import open3d as o3d
import numpy as np

# Section: 1
# This section reads object names used for the creation of the scene from
# model_def_list.txt AND with an added criteria e.g. only apple and cherry
#===================================================================================
#===================================================================================
#===================================================================================

# Check if a command-line argument is provided
if len(sys.argv) != 3:
    print("Error: Usage python crop_objects.py <file_path_to_project> <file_path_to_model_dir>")
    print("file_path_to_project: provide the path to the project that contains output_dataset_txt and ground_truth_point_cloud.xyz")
    print("file_path_to_parent_of_model_dir: provide the path to the parent directory that in resources/model has the models e.g. check vrg_crop_gen")
    print(len(sys.argv))
    sys.exit(1)

# Get the file path from the first command-line argument
file_path_to_project = sys.argv[1]
print(f"\nProvided file_path_to_project: {file_path_to_project}\n")

# Construct the full file path using os.path.join
def_list_file_path = os.path.join(file_path_to_project, "output_dataset_txt", "model_def_list.txt")

# Initialize an empty list to store the lines that match the criteria
selected_objects = []

# Open the file and read it line by line
with open(def_list_file_path, "r") as file:
    for line in file:
        # Check if the line starts with "Apple" or "Cherry"
        if line.startswith("Apple") or line.startswith("Cherry"):
            # Split the line at the semicolon and take the first part
            line_parts = line.split(";")
            selected_objects.append(line_parts[0])

# Print the selected objects
print("==============================================================================================")
print("==============================================================================================")
print("Section: 1")
print("Object names(under criteria) used for the creation of the scene")
print("Found at model_def_list.txt")
for obj in selected_objects:
    print(obj)

#===================================================================================
#===================================================================================
#===================================================================================

# Section: 2
# This section reads the poses of selected_objects from model_poses_list.txt
#===================================================================================
#===================================================================================
#===================================================================================

class object_pose:
    def __init__(self, object_name, x_coords, y_coords, z_coords, yaw):
        self.object_name = object_name
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.z_coords = z_coords
        self.yaw = yaw
        self.path_to_ply = ""
        self.path_to_aabb_ply = ""

    def __str__(self):
        return f"object_name: {self.object_name}\nx_coords: {self.x_coords}\ny_coords: {self.y_coords}\nz_coords: {self.z_coords}\nyaw: {self.yaw}\npath_to_ply: {self.path_to_ply}\n"

# Example usage:
#obj1 = object_pose("Object1", 1.0, 2.0, 3.0, 45.0)
#print(obj1)

# Initialize an empty list to store object poses
object_poses = []

# Specify the file path for the new text file
pose_file_path = os.path.join(file_path_to_project, "output_dataset_txt", "model_poses_list.txt")

# Open the pose file and read it line by line
with open(pose_file_path, "r") as pose_file:
    for line in pose_file:
        # Split the line by semicolon to extract object name and pose data
        parts = line.strip().split(";")
        if len(parts) == 3:
            object_name, pose_data, _ = parts
            if object_name in selected_objects:
                pose_data = pose_data.split(" ")
                if len(pose_data) == 4:
                    x_coords, y_coords, z_coords, yaw = map(float, pose_data)
                    pose = object_pose(object_name, x_coords, y_coords, z_coords, yaw)
                    object_poses.append(pose)
                else:
                    print(f"Invalid format for pose data: {line}")
                    exit(1)
        else:
            print(f"Invalid line format: {line}")
            exit(1)

print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 2")
print("Poses of selected_objects")
print("Found at from model_poses_list.txt\n")

# Print the object poses
for pose in object_poses:
    print(pose)

#===================================================================================
#===================================================================================
#===================================================================================
   
# Section: 3
# Read the ground truth point cloud
#===================================================================================
#===================================================================================
#===================================================================================

print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 3")
print("Reading and visualizing ground truth\n")

# Construct ground truth file path
ground_truth_file_path = os.path.join(file_path_to_project, "ground_truth_point_cloud.xyz")
# Read ground truth point cloud
print("Reading ground truth point cloud...")
pcd_ground_truth = o3d.io.read_point_cloud(ground_truth_file_path)
# Visualize ground truth point cloud
print("Visualizing ground truth point cloud...")
o3d.visualization.draw_geometries([pcd_ground_truth])

#===================================================================================
#===================================================================================
#===================================================================================

# Section: 4
# Reads all .ply from vrg_crop_gen/model (or other specified directory) and stores for each selected
# object their corresponding file path for the raw .ply and the _bounding_box.ply
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 4")
print("Reads all .ply from vrg_crop_gen/model (or other specified directory) and stores for each selected\
 object their corresponding file path for the raw .ply and the _bounding_box.ply")

# Get the file path to model dir from the second command-line argument
file_path_to_model_dir = sys.argv[2]
print(f"\nProvided file_path_to_model_dir: {file_path_to_model_dir}\n")

# Function to search for .ply files and store their name and path
def find_ply_files(directory):
    ply_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".ply"):
                file_path = os.path.join(root, file)
                ply_files.append((file, file_path))
    return ply_files

# Search for .ply files in the file_path_to_model_dir directory and its subdirectories
ply_files = find_ply_files(file_path_to_model_dir)

# Iterate through the object_poses list and update the path_to_ply and path_to_aabb_ply attributes
for obj in object_poses:
    object_name = obj.object_name + "_bounding_box.ply"
    #print(object_name)
    for ply_name, ply_path in ply_files:
        if object_name == ply_name:
            obj.path_to_ply = ply_path.replace("_bounding_box", "")
            obj.path_to_aabb_ply = ply_path

print("\nPrinting object_poses")

# Print the updated object_poses list
for obj in object_poses:
    print("Object Name:", obj.object_name)

    # Check if path_to_ply is empty
    if not obj.path_to_ply:
        print("Path to .ply is empty!")
        print("Exiting the program due to missing file paths.")
        sys.exit(1)

    # Check if path_to_aabb_ply is empty
    if not obj.path_to_aabb_ply:
        print("Path to aabb .ply is empty!")
        print("Exiting the program due to missing file paths.")
        sys.exit(1)

    print("Path to .ply:", obj.path_to_ply)
    print("Path to aabb .ply:", obj.path_to_aabb_ply)
    print("\n")

#===================================================================================
#===================================================================================
#===================================================================================

# Section: 5
# This section reads the axis aligned bounding box(aabb) for each selected_object, transforms it, and rotates it
# based on the ground truth pose
# Then combines all aabbs for the selected_objects with the ground truth point_cloud
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 5")
print("This section reads the axis aligned bounding box(aabb) for each selected_object, transforms it, and rotates it\
     based on the ground truth pose.\
     Then combines all aabbs for the selected_objects with the ground truth point_cloud\
    ")
#===================================================================================
#===================================================================================
#===================================================================================
# This function is used to perform the left-handed rotation of the mesh
# angle_degrees must be in radiance
def rotate_mesh_left_handed(mesh, angle_degrees, axis='z'):
    rotation_matrix = {
        'x': np.array([
            [1, 0, 0],
            [0, np.cos(-angle_degrees), -np.sin(-angle_degrees)],
            [0, np.sin(-angle_degrees), np.cos(-angle_degrees)]
        ]),
        'y': np.array([
            [np.cos(-angle_degrees), 0, np.sin(-angle_degrees)],
            [0, 1, 0],
            [-np.sin(-angle_degrees), 0, np.cos(-angle_degrees)]
        ]),
        'z': np.array([
            [np.cos(-angle_degrees), -np.sin(-angle_degrees), 0],
            [np.sin(-angle_degrees), np.cos(-angle_degrees), 0],
            [0, 0, 1]
        ])
    }

    rotation_matrix = rotation_matrix[axis]
    mesh.rotate(rotation_matrix)

# This function receives the list of object_poses
# and finds all the aabb for each object
# transforms, and rotates each one
# Then combines them into a single list 
def combine_all_aabb(object_poses, all_aabb):
    for obj in object_poses:
        # Load the PLY file
        pcd_obj = o3d.io.read_point_cloud(obj.path_to_ply)
        mesh_aabb = o3d.io.read_triangle_mesh(obj.path_to_aabb_ply)
        
        # Visualization for debugging purposes
        o3d.visualization.draw_geometries([pcd_obj])
        o3d.visualization.draw_geometries([mesh_aabb])
    
        # Define translation and rotation parameters
        new_position = [obj.x_coords, obj.y_coords, obj.z_coords]
        yaw_angle_degrees = obj.yaw
    
        # Translate the mesh to the new position (absolute)
        center = mesh_aabb.get_center()
        center[2] = 0
        mesh_aabb.translate(new_position - center)
    
        # Rotate the mesh
        rotate_mesh_left_handed(mesh_aabb, np.radians(yaw_angle_degrees), axis='z')
    
        # Store the mesh in the list
        all_aabb.append(mesh_aabb)
    
    return all_aabb

# Initialize the list that will contain all the aabb
all_aabb = []

# Call combine_all_aabb
print("Getting all aabb...")
all_aabb = combine_all_aabb(object_poses, all_aabb)

# Number of points for each aabb
number_of_points = 25000
print(f"Number of points per aabb: {number_of_points}")

# Create a point cloud containing all the aabb(pcd)
print("Creating pcd of combined aabb ...")
all_aabb_pcd = o3d.geometry.PointCloud()
for mesh in all_aabb:
    all_aabb_pcd += mesh.sample_points_uniformly(number_of_points) 

# Visualize the ground truth point cloud and all the aabb(pcd)
print("Visualizing combined pcd of ground truth and aabb")
all_geometries = [pcd_ground_truth] + [all_aabb_pcd]
o3d.visualization.draw_geometries(all_geometries)    

# Visualize the ground truth point cloud and all the aabb(mesh)
print("Visualizing combined pcd of ground truth and meshes of aabb")
o3d.visualization.draw_geometries([all_aabb[0], all_aabb[1], all_aabb[2], all_aabb[3], pcd_ground_truth])

#===================================================================================
#===================================================================================
#===================================================================================




















