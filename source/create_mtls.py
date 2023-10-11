import os

# Directory where your .obj files are located
base_directory = './model'

# List subdirectories at the same level as "Apple_Autumn"
subdirectories = [name for name in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, name))]

# Loop through the subdirectories
for subdirectory in subdirectories:
    obj_directory = os.path.join(base_directory, subdirectory)
    
    # Check if the directory name is "Fence"
    if subdirectory == "Fence":
        # If it's "Fence," update obj_directory to look in "Fence/Fence2"
        obj_directory = os.path.join(obj_directory, "Fence2")
        
    # Create .mtl files for each .obj file in the directory
    for obj_file in os.listdir(obj_directory):
        if obj_file.endswith('.obj'):
            # Generate the object name from the .obj file name (without the extension)
            object_name = os.path.splitext(obj_file)[0]
            
            # Check if the directory is "Fence" and modify object_name
            if subdirectory == "Fence":
                object_name2 = object_name.split('_')[0]
                # Define the .mtl file content with the dynamic texture reference and additional material properties
                mtl_content = f"""\
newmtl {object_name}  # Use object name as material name
Ka 1.000000 1.000000 1.000000
Kd 0.800000 0.800000 0.800000
Ks 0.500000 0.500000 0.500000
Ni 1.450000
d 1.000000           
illum 2
map_Kd ../../../textures/{subdirectory}/{object_name2}.jpg
map_d ../../../textures/{subdirectory}/{object_name2}.jpg
"""
            else:
                object_name2 = object_name
                # Define the .mtl file content with the dynamic texture reference and additional material properties
                mtl_content = f"""\
newmtl {object_name}  # Use object name as material name
Ka 1.000000 1.000000 1.000000
Kd 0.800000 0.800000 0.800000
Ks 0.500000 0.500000 0.500000
Ni 1.450000
d 1.000000           
illum 2
map_Kd ../../textures/{subdirectory}/{object_name2}.jpg
map_d ../../textures/{subdirectory}/{object_name2}.jpg
"""

            # Save the .mtl file in the same directory as the .obj file
            mtl_file_name = f'{object_name}.mtl'
            mtl_file_path = os.path.join(obj_directory, mtl_file_name)

            with open(mtl_file_path, 'w') as mtl_file:
                mtl_file.write(mtl_content)

            print(f"Created .mtl file for {obj_file}: {mtl_file_name} in directory {subdirectory}")