#=======================================================================================================
#=======================================================================================================
#=======================================================================================================
#=======================================================================================================
#================= MUST MODIFY TO BE CONFIGURABLE AND CORRECT THE PATHS=================================
#=======================================================================================================
#=======================================================================================================
#=======================================================================================================
#=======================================================================================================
import glob
import os
import math
import sys

# Check if an argument is provided
if len(sys.argv) != 3:
    print("Usage: python3.10 create_ground_truth_point_cloud.py <model_poses_txt_file_path> <crop_gen_model_dir>")
    sys.exit(1)

# Get the argument passed (the model_poses_txt_file)
model_poses_txt_file = sys.argv[1]

# Get the argument passed (the crop_gen_model_dir)
crop_gen_model_dir = sys.argv[2]

# Get a list of all ".xyz" files in the current directory
#xyz_files = glob.glob("*.xyz")

#print(xyz_files)

# Check if the file "model_poses_list.txt" exists
if not os.path.isfile(model_poses_txt_file):
    print(f"Error: File '{model_poses_txt_file}' does not exist. Exiting.")
    sys.exit(1)

# Initialize empty lists for each element
object_names = []
x_coords = []
y_coords = []
z_coords = []
yaws = []
object_ids = []


# Open and read the file line by line
with open(model_poses_txt_file, "r") as file:
    for line in file:
        # Split each line into its components using ";"
        parts = line.strip().split(";")
        
        # Check if there are exactly 3 elements in the line
        if len(parts) != 3:
            print(f"Error reading '{model_poses_txt_file}': Line does not have 3 elements: {line}.")
            exit(1)
            
        object_name, coordinates, object_id = parts

        # Split the coordinates into its sub-components using space
        coord_parts = coordinates.split(" ")
        
        # Check if there are exactly 4 elements in the coordinates
        if len(coord_parts) != 4:
            print(f"Error reading '{model_poses_txt_file}': Incorrect number of elements in coordinates: {coordinates}")
            exit(1)
        
        try:
            x_coord = float(coord_parts[0])
            y_coord = float(coord_parts[1])
            z_coord = float(coord_parts[2])
            yaw = float(coord_parts[3])
        except ValueError:
            print(f"Error reading '{model_poses_txt_file}': Failed to convert coordinates to float: {coordinates}")
            exit(1)

        # Append each element to its corresponding list
        object_names.append(object_name)
        x_coords.append(x_coord)
        y_coords.append(y_coord)
        z_coords.append(z_coord)
        yaws.append(yaw)
        object_ids.append(object_id)


# Function to recursively search for .xyz files in a directory
def find_xyz_files(directory):
    xyz_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xyz"):
                #xyz_files.append(os.path.join(root, file))
                xyz_path = os.path.join(root, file)
                xyz_files.append(xyz_path)

    return xyz_files

# Get a list of .xyz files in the specified directory and its subdirectories
xyz_files_in_dir = find_xyz_files(crop_gen_model_dir)
print("THE XYZ FILES IN DIR")
print(xyz_files_in_dir)

# Initialize a list to store the paths of found .xyz files
object_paths = []

# Check if the .xyz files specified in object_names exist
for object_name in object_names:
    xyz_filename = f"{object_name}.xyz"
    if xyz_filename in [os.path.basename(x) for x in xyz_files_in_dir]:
        #object_paths.append(os.path.join(crop_gen_model_dir, xyz_filename))
        object_paths.append([x for x in xyz_files_in_dir if os.path.basename(x) == xyz_filename][0])
    else:
        #print(f"{xyz_filename} does not exist in {crop_gen_model_dir} or its subdirectories. Exiting(1.0.0).")
        print(f"{xyz_filename} does not exist in {crop_gen_model_dir} or its subdirectories. Exiting(1.0.0).")
        sys.exit(1)

print("All .xyz files included in model_poses_list.txt have been found.")
print("Continuing with the process to combine the .xyz files.")

# Toggle variable for rotation (True/False)
rotate_coordinates = True  # Set this to True to enable rotation

# Open and write to the "combined.xyz" file
with open("combined712345679.xyz", "w") as combined_file:
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
























































