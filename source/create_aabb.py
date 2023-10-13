import os
import open3d as o3d
import sys

# Function to create and save bounding box for a .ply file
def create_and_save_bounding_box(ply_file_path):
    # Read the .ply file
    point_cloud = o3d.io.read_point_cloud(ply_file_path)
    aabb = point_cloud.get_axis_aligned_bounding_box()
    max_bound = aabb.get_max_bound()
    min_bound = aabb.get_min_bound()
    
    # Create a mesh representing the bounding box
    bounding_box = o3d.geometry.TriangleMesh.create_box(
        width=max_bound[0] - min_bound[0],
        height=max_bound[1] - min_bound[1],
        depth=max_bound[2] - min_bound[2]
    )
    
    # Save the bounding box in PLY format
    output_path = os.path.splitext(ply_file_path)[0] + '_bounding_box.ply'
    o3d.io.write_triangle_mesh(output_path, bounding_box)
    print(f"Bounding box saved to {output_path}")


# Check if a directory argument is provided when executing the script
if len(sys.argv) != 2:
    print("Usage: python create_aabb.py <base_directory>")
    sys.exit(1)
    
# Directory to search for .ply files
# Get the base directory from the command-line argument
base_directory = sys.argv[1]

# Recursive function to search for .ply files and create bounding boxes
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.ply'):
                ply_file_path = os.path.join(root, file)
                create_and_save_bounding_box(ply_file_path)

# Start the processing from the base directory
process_directory(base_directory)