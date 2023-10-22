#
# The following script performs the following tasks
# 1. Read object names (under criteria) used for the creation of the scene -> selected_objects (in model_def_list.txt) 
# 2. Read poses of selected_objects (in model_poses_list.txt)
# 3. Read and visualize the ground point cloud
# 4. Read and visualize the colmap (aligned) point cloud
# 5. Reads all .ply from vrg_crop_gen/resources/model (or other specified directory) and stores for each selected
#    object their corresponding file path for the raw .ply
# 6. Combines and visualizes aabbs(both pcd and mesh) of selected_objects with ground truth and colmap (aligned) point clouds <br>
# 7. Combines and visualizes pcd of ground truth and colmap (aligned)
# 8. Crop objects from ground truth pcd and store them
# 9. Crop objects from colmap (aligned) pcd and store them
# 10. Visualize and store combined ground truth and colmap (aligned) cropped objects

# Configuration:
# Debug Mode: True to run in debug mode, False to run in normal mode
debug = True
debug2 = True
debug3 = True
debug4 = True
debug5 = True

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

# Get the file_path_to_project from the first command-line argument
file_path_to_project = sys.argv[1]
print(f"\nProvided file_path_to_project: {file_path_to_project}\n")

# Get the file_path_to_model_dir from the second command-line argument
file_path_to_model_dir = sys.argv[2]
print(f"\nProvided file_path_to_model_dir: {file_path_to_model_dir}\n")

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
    def __init__(self, object_name, x_coords, y_coords, z_coords, yaw, ID_counter):
        self.object_name = object_name
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.z_coords = z_coords
        self.yaw = yaw
        self.ID_counter = ID_counter
        self.path_to_ply = ""
        

    def __str__(self):
        return f"object_name: {self.object_name}\nx_coords: {self.x_coords}\ny_coords: {self.y_coords}\nz_coords: {self.z_coords}\nyaw: {self.yaw}\nID_counter: {self.ID_counter}\npath_to_ply: {self.path_to_ply}\n"

# Example usage:
#obj1 = object_pose("Object1", 1.0, 2.0, 3.0, 45.0)
#print(obj1)

# Initialize an empty list to store object poses
object_poses = []

# ID counter for each object
ID_counter = 0

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
                    pose = object_pose(object_name, x_coords, y_coords, z_coords, yaw, ID_counter)
                    object_poses.append(pose)
                    ID_counter = ID_counter + 1
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
if debug:
    # Visualize ground truth point cloud
    print("Visualizing ground truth point cloud...")
    o3d.visualization.draw_geometries([pcd_ground_truth])
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 4
# Read the colmap (aligned) point cloud
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 4")
print("Reading and visualizing colmap (aligned) point cloud\n")

# Construct colmap file path
colmap_aligned_file_path = os.path.join(file_path_to_project, "align", "fused.ply")
# Read colmap (aligned) point cloud
print("Reading colmap (aligned) point cloud...")
pcd_colmap_aligned = o3d.io.read_point_cloud(colmap_aligned_file_path)

if debug:
    # Visualize colmap (aligned) point cloud
    print("Visualizing colmap (aligned) point cloud...")
    o3d.visualization.draw_geometries([pcd_colmap_aligned])
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 5
# Reads all .ply from vrg_crop_gen/model (or other specified directory) and stores for each selected
# object their corresponding file path for the raw .ply 
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 5")
print("Reads all .ply from vrg_crop_gen/model (or other specified directory) and stores for each selected\
 object their corresponding file path for the raw .ply")

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

# Section: 6
# This section creates the axis aligned bounding box(aabb) for each selected_object, transforms it, and rotates it
# based on the ground truth pose
# Then combines all aabbs for the selected_objects with the ground truth and colmap (aligned) point clouds
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 6")
print("This section reads the axis aligned bounding box(aabb) for each selected_object, transforms it, and rotates it\
     based on the ground truth pose.\
     Then combines and visualizes all aabbs (both pcd and mesh) for the selected_objects with the ground truth and colmap (aligned) point_clouds\
    ")

# This function receives the list of object_poses
# and finds all the aabb for each object
# transforms, and rotates each one
# Then combines them into a single list 
def combine_all_aabb(object_poses, all_aabb):
    for obj in object_poses:
        # Load the PLY file
        print("Reading pcd of object")
        pcd_obj = o3d.io.read_point_cloud(obj.path_to_ply)
        
        # Visualization for debugging purposes
        #o3d.visualization.draw_geometries([pcd_obj])
        aabb = pcd_obj.get_axis_aligned_bounding_box()
        aabb.color = (1, 0, 0)
        if debug:
            print("Visualizing pcd of object with aabb")
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

        if debug:
            print("Visualizing pcd of aabb (after transform)")
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
        if debug:
            print("Visualizing mesh of aabb (after transform)")
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

if debug:
    # Visualize the ground truth point cloud and all the aabb(pcd)
    print("Visualizing combined pcd of ground truth and aabb")
    all_geometries = [pcd_ground_truth] + [all_aabb_pcd]
    o3d.visualization.draw_geometries(all_geometries)    

    # Visualize the ground truth point cloud and all the aabb(mesh)
    print("Visualizing combined pcd of ground truth and meshes of aabb")
    geometries = all_aabb + [pcd_ground_truth]  
    o3d.visualization.draw_geometries(geometries)

    # Visualize the colmap (aligned) point cloud and all the aabb(pcd)
    print("Visualizing combined pcd of colmap (aligned) and aabb")
    all_geometries = [pcd_colmap_aligned] + [all_aabb_pcd]
    o3d.visualization.draw_geometries(all_geometries)

    # Visualize the colmap (aligned) point cloud and all the aabb(mesh)
    print("Visualizing combined pcd of colmap (aligned) and meshes of aabb")
    geometries = all_aabb + [pcd_colmap_aligned]
    o3d.visualization.draw_geometries(geometries)
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 7
# Combines and visualizes pcd of ground truth and colmap (aligned)
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 7")
print("Combines and visualizes pcd of ground truth and colmap (aligned)\n")
# Visualize ground truth and colmap (aligned) point clouds
print("Visualizing combined pcd of ground truth and colmap (aligned)")
all_geometries = [pcd_ground_truth] + [pcd_colmap_aligned]
o3d.visualization.draw_geometries(all_geometries)
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 8
# Crop objects from ground truth pcd and store them
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 8")
print("Crop objects from ground truth pcd and store them\n")

# Initialize list that will contain the cropped objects
pcd_ground_truth_cropped_objects = []

for mesh in all_aabb:
    # Get vertices of mesh
    vertices = mesh.vertices
    # Transform to o3d vector
    o3d_vertices = o3d.utility.Vector3dVector(vertices)
    # Create oriented bounding box from mesh vertices
    bounding_box = o3d.geometry.OrientedBoundingBox.create_from_points(o3d_vertices) 

    if debug2:
        print("Visualizing bounding box...")
        # Visualize bounding box
        bounding_box.color = (1, 0, 0)
        print(bounding_box)
        o3d.visualization.draw_geometries([bounding_box])

    # Crop the point cloud using the bounding box
    pcd_ground_truth_cropped = pcd_ground_truth.crop(bounding_box)

    # Append cropped object
    pcd_ground_truth_cropped_objects.append(pcd_ground_truth_cropped)

    if debug2:
        print("Visualizing cropped point cloud...")
        # Display the cropped point cloud:
        o3d.visualization.draw_geometries([pcd_ground_truth_cropped])
        print("Visualizing cropped point cloud. and aabb..")
        # Display the cropped point cloud and aabb
        geometries = [mesh] + [pcd_ground_truth_cropped]  
        o3d.visualization.draw_geometries(geometries)

# Visualize combined ground truth cropped objects
if debug3:
    # Initialize an empty point cloud to store the combined ground truth cropped objects
    pcd_ground_truth_cropped_objects_combined = o3d.geometry.PointCloud()
    
    # Construct point cloud with all ground truth cropped objects
    print("Constructing point cloud with all ground truth cropped objects...")
    for pcd in pcd_ground_truth_cropped_objects:    
        pcd_ground_truth_cropped_objects_combined += pcd
        
    # Visualize point cloud with all ground truth cropped objects
    print("Visualizing point cloud with all ground truth cropped objects...")
    o3d.visualization.draw_geometries([pcd_ground_truth_cropped_objects_combined])
       
# Visualizes combined ground truth cropped objects and all the aabb(mesh)     
if debug3:
    # Visualizes combined ground truth cropped objects and all the aabb(mesh)    
    print("Visualizing combined pcd of ground truth and meshes of aabb")
    geometries = all_aabb + [pcd_ground_truth_cropped_objects_combined]  
    o3d.visualization.draw_geometries(geometries)

# Constructing ground truth cropped objects file path
file_name_gt_cropped_objects = "gt_cropped_objects"
file_path_gt_cropped_objects = os.path.join(file_path_to_project, file_name_gt_cropped_objects)
print("file_path_gt_cropped_objects: ", file_path_gt_cropped_objects)

# Creating ground truth cropped objects directory
os.makedirs(file_path_gt_cropped_objects, exist_ok=True)

# Saving the ground truth cropped objects
for i, pcd in enumerate(pcd_ground_truth_cropped_objects):
    
    # Define the output file path
    output_file = os.path.join(file_path_gt_cropped_objects, f"{object_poses[i].ID_counter}_gt_{object_poses[i].object_name}.ply")  
        
    # Save the point cloud to the specified file
    o3d.io.write_point_cloud(output_file, pcd)

    print(f"Saved {output_file}")
    

print("Ground truth cropped objects saved successfully")
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 9
# Crop objects from colmap (aligned) pcd and store them
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 9")
print("Crop objects from colmap (aligned) pcd and store them\n")

# Initialize list that will contain the cropped objects
pcd_colmap_a_cropped_objects = []

for mesh in all_aabb:
    # Get vertices of mesh
    vertices = mesh.vertices
    # Transform to o3d vector
    o3d_vertices = o3d.utility.Vector3dVector(vertices)
    # Create oriented bounding box from mesh vertices
    bounding_box = o3d.geometry.OrientedBoundingBox.create_from_points(o3d_vertices) 

    if debug4:
        print("Visualizing bounding box...")
        # Visualize bounding box
        bounding_box.color = (1, 0, 0)
        print(bounding_box)
        o3d.visualization.draw_geometries([bounding_box])

    # Crop the colmap (aligned) using the bounding box
    pcd_colmap_a_cropped = pcd_colmap_aligned.crop(bounding_box)

    # Append cropped object
    pcd_colmap_a_cropped_objects.append(pcd_colmap_a_cropped)

    if debug4:
        print("Visualizing cropped point cloud...")
        # Display the cropped point cloud:
        o3d.visualization.draw_geometries([pcd_colmap_a_cropped])
        print("Visualizing cropped point cloud. and aabb..")
        # Display the cropped point cloud and aabb
        geometries = [mesh] + [pcd_colmap_a_cropped]  
        o3d.visualization.draw_geometries(geometries)

# Visualize combined colmap (aligned) cropped objects
if debug4:
    # Initialize an empty point cloud to store the combined colmap (aligned) cropped objects
    pcd_colmap_a_cropped_objects_combined = o3d.geometry.PointCloud()
    
    # Construct point cloud with all colmap (aligned) cropped objects
    print("Constructing point cloud with all colmap (aligned) cropped objects...")
    for pcd in pcd_colmap_a_cropped_objects:    
        pcd_colmap_a_cropped_objects_combined += pcd
        
    # Visualize point cloud with all colmap (aligned) cropped objects
    print("Visualizing point cloud with all colmap (aligned) cropped objects...")
    o3d.visualization.draw_geometries([pcd_colmap_a_cropped_objects_combined])
       
# Visualizes combined colmap (aligned) cropped objects and all the aabb(mesh)     
if debug4:
    # Visualizes combined colmap (aligned) cropped objects and all the aabb(mesh)    
    print("Visualizing combined pcd of colmap (aligned) and meshes of aabb")
    geometries = all_aabb + [pcd_colmap_a_cropped_objects_combined]  
    o3d.visualization.draw_geometries(geometries)

# Constructing colmap (aligned) cropped objects file path
file_name_colmap_a_cropped_objects = "colmap_a_cropped_objects"
file_path_colmap_a_cropped_objects = os.path.join(file_path_to_project, file_name_colmap_a_cropped_objects)
print("file_path_colmap_a_cropped_objects: ", file_path_colmap_a_cropped_objects)

# Creating colmap (aligned) cropped objects directory
os.makedirs(file_path_colmap_a_cropped_objects, exist_ok=True)

# Saving the ground truth cropped objects
for i, pcd in enumerate(pcd_colmap_a_cropped_objects):
    
    # Define the output file path
    output_file = os.path.join(file_path_colmap_a_cropped_objects, f"{object_poses[i].ID_counter}_colmap_{object_poses[i].object_name}.ply")  
        
    # Save the point cloud to the specified file
    o3d.io.write_point_cloud(output_file, pcd)

    print(f"Saved {output_file}")
    
print("Colmap (aligned) cropped objects saved successfully")
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 10 
# Visualize combined ground truth and colmap (aligned) cropped objects
#===================================================================================
#===================================================================================
#===================================================================================
print("\n==============================================================================================")
print("==============================================================================================")
print("Section: 10")
print("Visualize combined ground truth and colmap (aligned) cropped objects\n")
# Constructing combined cropped objects file path
file_name_combined_cropped_objects = "combined_cropped_objects"
file_path_combined_cropped_objects = os.path.join(file_path_to_project, file_name_combined_cropped_objects)
print("file_path_combined_cropped_objects: ", file_path_combined_cropped_objects)

# Creating combined cropped objects directory
os.makedirs(file_path_combined_cropped_objects, exist_ok=True)

# Visualize and store combined cropped objects
for i, gt_pcd in enumerate(pcd_ground_truth_cropped_objects):
    
    # Initialize object to store copy of object ground truth pcd
    copy_gt_pcd = o3d.geometry.PointCloud()
    # Transfer points
    copy_gt_pcd.points = gt_pcd.points
    # Set color to blue
    blue_color = [0.0, 0.0, 1.0]
    num_points = len(copy_gt_pcd.points)
    copy_gt_pcd.colors = o3d.utility.Vector3dVector(np.tile(blue_color, (num_points, 1)))
    
    # Initialize object to store copy of object colmap (aligned) pcd
    copy_colmap_pcd = o3d.geometry.PointCloud()
    # Transfer points
    copy_colmap_pcd.points = pcd_colmap_a_cropped_objects[i].points
    # Set color to green
    green_color = [0.0, 1.0, 0.0]
    num_points = len(copy_colmap_pcd.points)
    copy_colmap_pcd.colors = o3d.utility.Vector3dVector(np.tile(green_color, (num_points, 1)))
    
    # Construct combined pcd
    print("Constructing combined pcd...")
    combined_pcd = copy_gt_pcd + copy_colmap_pcd
    
    if debug5:
        # Visualize combined pcd
        print("Visualizing combined pcd...")
        o3d.visualization.draw_geometries([combined_pcd])
    
    # Define the output file path
    output_file = os.path.join(file_path_combined_cropped_objects, f"{object_poses[i].ID_counter}_combined_{object_poses[i].object_name}.ply")    
    
    # Save the point cloud to the specified file
    o3d.io.write_point_cloud(output_file, combined_pcd) 
    
    print(f"Saved {output_file}")
    
print("Combined cropped objects saved successfully")
#===================================================================================
#===================================================================================
#===================================================================================

