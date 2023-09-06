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

# Get a list of all ".xyz" files in the current directory
xyz_files = glob.glob("*.xyz")

print(xyz_files)

# Check if the file "model_poses_list.txt" exists
if not os.path.isfile("model_poses_list.txt"):
    print("Error: The file 'model_poses_list.txt' does not exist.")
    exit(1)

# Initialize empty lists for each element
object_names = []
x_coords = []
y_coords = []
z_coords = []
yaws = []
object_ids = []


# Open and read the file line by line
with open("model_poses_list.txt", "r") as file:
    for line in file:
        # Split each line into its components using ";"
        parts = line.strip().split(";")
        
        # Check if there are exactly 3 elements in the line
        if len(parts) != 3:
            print(f"Error (reading 'model_poses_list.txt'): Line does not have 3 elements: {line}.")
            exit(1)
            
        object_name, coordinates, object_id = parts

        # Split the coordinates into its sub-components using space
        coord_parts = coordinates.split(" ")
        
        # Check if there are exactly 4 elements in the coordinates
        if len(coord_parts) != 4:
            print(f"Error (reading 'model_poses_list.txt'): Incorrect number of elements in coordinates: {coordinates}")
            exit(1)
        
        try:
            x_coord = float(coord_parts[0])
            y_coord = float(coord_parts[1])
            z_coord = float(coord_parts[2])
            yaw = float(coord_parts[3])
        except ValueError:
            print(f"Error (reading 'model_poses_list.txt'): Failed to convert coordinates to float: {coordinates}")
            exit(1)

        # Append each element to its corresponding list
        object_names.append(object_name)
        x_coords.append(x_coord)
        y_coords.append(y_coord)
        z_coords.append(z_coord)
        yaws.append(yaw)
        object_ids.append(object_id)


# Check if the corresponding .xyz file exists for each object
for object_name in object_names:
    xyz_filename = f"{object_name}.xyz"
    if not os.path.isfile(xyz_filename):
        print(f"Error: .xyz file not found for object '{object_name}' ({xyz_filename}).")
        exit(1)

# Toggle variable for rotation (True/False)
rotate_coordinates = True  # Set this to True to enable rotation

# Open and write to the "combined.xyz" file
with open("combined71234567_LEFT.xyz", "w") as combined_file:
    for i in range(len(object_names)):
        object_name = object_names[i]
        x_coord = x_coords[i]
        y_coord = y_coords[i]
        z_coord = z_coords[i]
        yaw = yaws[i]

        # Read the corresponding .xyz file
        xyz_filename = f"{object_name}.xyz"
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
























































