import glob
import os
import math
import sys
import time

# Check if arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3.10 create_ground_truth_point_cloud.py <model_poses_txt_file_path> <crop_gen_model_dir_path>")
    sys.exit(1)

# Get the argument passed (the model_poses_txt_file_path)
model_poses_txt_file_path = sys.argv[1]

# Get the argument passed (the crop_gen_model_dir_path)
crop_gen_model_dir_path = sys.argv[2]

# Check if the file "model_poses_list.txt" exists
if not os.path.isfile(model_poses_txt_file_path):
    print(f"Error: File '{model_poses_txt_file_path}' does not exist. Exiting.")
    sys.exit(1)

# Initialize empty lists for each element
object_names = []
x_coords = []
y_coords = []
z_coords = []
yaws = []
object_ids = []

# Open and read the file line by line
with open(model_poses_txt_file_path, "r") as file:
    for line in file:
        # Split each line into its components using ";"
        parts = line.strip().split(";")
        
        # Check if there are exactly 3 elements in the line
        if len(parts) != 3:
            print(f"Error reading '{model_poses_txt_file_path}': Line does not have 3 elements: {line}.")
            exit(1)
            
        object_name, coordinates, object_id = parts

        # Split the coordinates into its sub-components using space
        coord_parts = coordinates.split(" ")
        
        # Check if there are exactly 4 elements in the coordinates
        if len(coord_parts) != 4:
            print(f"Error reading '{model_poses_txt_file_path}': Incorrect number of elements in coordinates: {coordinates}")
            exit(1)
        
        try:
            x_coord = float(coord_parts[0])
            y_coord = float(coord_parts[1])
            z_coord = float(coord_parts[2])
            yaw = float(coord_parts[3])
        except ValueError:
            print(f"Error reading '{model_poses_txt_file_path}': Failed to convert coordinates to float: {coordinates}")
            exit(1)

        # Append each element to its corresponding list
        object_names.append(object_name)
        x_coords.append(x_coord)
        y_coords.append(y_coord)
        z_coords.append(z_coord)
        yaws.append(yaw)
        object_ids.append(object_id)

# Function to recursively search for .obj files in a directory
def find_obj_files(directory):
    obj_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".obj"):
                #xyz_files.append(os.path.join(root, file))
                obj_path = os.path.join(root, file)
                obj_files.append(obj_path)

    return obj_files

# Get a list of .obj files in the specified directory and its subdirectories
obj_files_in_dir = find_obj_files(crop_gen_model_dir_path)

# Initialize a list to store the paths of found .xyz files
object_paths = []

# Check if the .obj files specified in object_names exist
for object_name in object_names:
    object_filename = f"{object_name}.obj"
    if object_filename in [os.path.basename(x) for x in obj_files_in_dir]:
        object_paths.append([x for x in obj_files_in_dir if os.path.basename(x) == object_filename][0])
    else:
        print(f"{object_filename} does not exist in {crop_gen_model_dir_path} or its subdirectories. Exiting(1.0.0.3.5).")
        sys.exit(1)

print("All object files included in model_poses_list.txt have been found.")
print("Continuing with the process to transform all object files to xyz files")

# Create the 'xyz_format' directory if it doesn't exist
output_directory = 'xyz_format'
os.makedirs(output_directory, exist_ok=True)

# Iterate through the list of .obj files
for obj_file in object_paths:
    # Define the output .xyz file path
    base_name = os.path.splitext(os.path.basename(obj_file))[0]
    output_xyz_file = os.path.join(output_directory, f"{base_name}.xyz")

    # Read the .obj file and extract vertex positions
    vertices = []
    with open(obj_file, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):
                parts = line.split()
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                vertices.append([x, y, z])

    # Write the extracted vertex positions to the .xyz file
    with open(output_xyz_file, 'w') as xyz_file:
        for vertex in vertices:
            xyz_file.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")

    print(f"{obj_file} converted to {output_xyz_file}")

# Initialize a list to store the paths of created .xyz files
object_paths = []

xyz_files_in_dir = "xyz_format"

# Check if the .xyz files specified in object_names exist
for object_name in object_names:
    xyz_filename = f"{object_name}.xyz"
    found = False # Flag to check if the .xyz file was found
    
    # Iterate through items in xyz_files_in_dir
    for root, _, files in os.walk(xyz_files_in_dir):
        for file in files:
            # Check if the file is an .xyz file and its name matches the target .xyz file
            if file.endswith('.xyz') and file == xyz_filename:
                # Construct the full path to the found .xyz file
                xyz_filepath = os.path.join(root, file)
                object_paths.append(xyz_filepath)
                found = True
                break  # Exit the loop once a matching .xyz file is found

        # Check if the item is a file and its base name matches the target .xyz file
        #if os.path.isfile(item) and os.path.basename(item) == xyz_filename:
            #object_paths.append(item)
            #found = True
            #4break  # Exit the loop once a matching .xyz file is found
    
    if not found:
        print(f"{xyz_filename} does not exist in {xyz_files_in_dir} or its subdirectories. Exiting(1.0.1.1).")
        for x in xyz_files_in_dir:
            print(os.path.basename(x))
        sys.exit(1)

print("All .xyz files included in model_poses_list.txt have been found.")
print("Continuing with the process to combine the .xyz files.")

# Toggle variable for rotation (True/False)
rotate_coordinates = True  # Set this to True to enable rotation

# Open and write to the "combined.xyz" file
with open("ground_truth_point_cloud.xyz", "w") as combined_file:
    for i in range(len(object_paths)):
        object_path = object_paths[i]
        x_coord = x_coords[i]
        y_coord = y_coords[i]
        z_coord = z_coords[i]
        yaw = yaws[i]

        # Read the corresponding .xyz file
        xyz_filename = f"{object_path}"
        with open(xyz_filename, "r") as xyz_file:
            for line in xyz_file:
                # Split the line into x, y, z coordinates
                x, y, z, *rest = line.strip().split()

                # Convert coordinates to float
                x, y, z = float(x), float(y), float(z)

                # Apply rotation if enabled
                if rotate_coordinates:
                    # Convert yaw to radians and rotate the coordinates
                    yaw_rad = math.radians(yaw)
                    new_x = x * math.cos(yaw_rad) - y * math.sin(yaw_rad) #confirmed
                    new_y = x * math.sin(yaw_rad) + y * math.cos(yaw_rad) #confirmed
                    x, y = new_x, new_y
                    
                # Apply modifications based on x_coords, y_coords, and z_coords
                x += x_coord
                y += y_coord
                z += z_coord

                # Write the modified line to "combined.xyz"
                combined_file.write(f"{x} {y} {z} {' '.join(rest)}\n")

print("Combined and modified .xyz files into 'combined.xyz'.")
























































