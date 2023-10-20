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
#===================================================================================
#===================================================================================
#===================================================================================
import sys
import os
import open3d as o3d
import numpy as np
#===================================================================================
#===================================================================================
#===================================================================================

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

# Iterate through the object_poses list and update the path_to_ply attribute
for obj in object_poses:
    object_name = obj.object_name + ".ply"
    #print(object_name)
    for ply_name, ply_path in ply_files:
        if object_name == ply_name:
            obj.path_to_ply = ply_path
            
print("\nPrinting object_poses")

# Print the updated object_poses list
for obj in object_poses:
    print("Object Name:", obj.object_name)

    # Check if path_to_ply is empty
    if not obj.path_to_ply:
        print("Path to .ply is empty!")
        print("Exiting the program due to missing file paths.")
        sys.exit(1)

    print("Path to .ply:", obj.path_to_ply)
    print("\n")

#===================================================================================
#===================================================================================
#===================================================================================

# Section: 5
# This section creates the axis aligned bounding box(aabb) for each selected_object, transforms it, and rotates it
# based on the ground truth pose
# Then combines all aabbs for the selected_objects with the ground truth point_cloud
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 5")
print("This section reads the axis aligned bounding box(aabb) for each selected_object, transforms it, and rotates it\
     based on the ground truth pose.\
     Then combines all aabbs for the selected_objects with the ground truth point_cloud\
    ")

# This function receives the list of object_poses
# and finds all the aabb for each object
# transforms, and rotates each one
# Then combines them into a single list 
def combine_all_aabb(object_poses, all_aabb):
    for obj in object_poses:
        # Load the PLY file
        pcd_obj = o3d.io.read_point_cloud(obj.path_to_ply)
        
        # Visualization for debugging purposes
        #o3d.visualization.draw_geometries([pcd_obj])
        aabb = pcd_obj.get_axis_aligned_bounding_box()
        o3d.visualization.draw_geometries([pcd_obj, aabb])

        points_of_aabb = aabb.get_box_points()
        translation = np.array([obj.x_coords, obj.y_coords, obj.z_coords])

        # Create transformation matrices
        translation_matrix = np.identity(4)
        translation_matrix[:3, 3] = translation
        # Rotation in degrees around the Z-axis
        rotation_radians = np.radians(obj.yaw)
        rotation_matrix = np.array([
            [np.cos(rotation_radians), -np.sin(rotation_radians), 0, 0],
            [np.sin(rotation_radians), np.cos(rotation_radians), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Combine translation and rotation into a single transformation matrix
        transformation_matrix = np.dot(translation_matrix, rotation_matrix)
        
        points_of_aabb_open3d_obj = o3d.geometry.PointCloud()
        points_of_aabb_open3d_obj.points = o3d.utility.Vector3dVector(points_of_aabb)

        # Apply the transformation to the point cloud
        points_of_aabb_open3d_obj.transform(transformation_matrix)
        
        o3d.visualization.draw_geometries([points_of_aabb_open3d_obj])

        triangles = np.array([
        [3, 6, 5],
        [4, 5, 6],
        [2, 1, 0],
        [1, 2, 7],
        [0, 3, 2],
        [3, 5, 2],
        [7, 4, 1],
        [1, 4, 6],
        [6, 3, 0],
        [0, 1, 6],
        [2, 5, 4],
        [2, 4, 7]
        ])

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = points_of_aabb_open3d_obj.points
        mesh.triangles = o3d.utility.Vector3iVector(triangles)

        o3d.visualization.draw_geometries([mesh])

        all_aabb.append(mesh)

        # Store the mesh in the list
        #all_aabb.append(mesh_aabb)

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
geometries = all_aabb + [pcd_ground_truth]  
o3d.visualization.draw_geometries(geometries)

#===================================================================================
#===================================================================================
#===================================================================================



















