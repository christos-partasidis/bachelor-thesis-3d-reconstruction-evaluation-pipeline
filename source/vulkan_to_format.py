# This is a python script to convert images_poses.txt
# created from vulkan to the compatible format

import sys
import os

# Check if at least one argument (excluding the script name) is provided
if len(sys.argv) < 2:
    print("Usage: python colmapt_to_format.py <latest_data>")
    sys.exit(1)

# The first command-line argument (sys.argv[1]) is the <latest_data> passed from the Bash script
latest_data = sys.argv[1]


# Define the input and output file paths
input_file_path = '../projects/' + latest_data + '/output_dataset_txt/image_poses.txt'
output_file_path = '../projects/' + latest_data + '/evaluation/ground_truth.txt'

# Check if the output file already exists
if os.path.exists(output_file_path):
    print(f"The output file '{output_file_path}' already exists. Exiting to avoid overwriting.")
    sys.exit(1)
try:
    # Read the input file and filter lines
    filtered_lines = []

    with open(input_file_path, 'r') as input_file:
        for index, line in enumerate(input_file):

            # Skip lines that start with '#'
            if index==0:
                filtered_lines.append("# time x y z qx qy qz qw\n")
                continue

            parts = line.strip().split(',')

            if len(parts) >= 2:  # Make sure there are at least two elements in the line
                filename = parts[0].split('_')[1].split('.')[0]
                new_line = filename + ' ' + ' '.join(parts[1:])
                new_number = int(filename) + 1
                new_line = str(new_number) + ' ' + ' '.join(parts[1:])

            filtered_lines.append(new_line + '\n')        

    # Write the filtered lines to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(filtered_lines)
    
    print("Conversion complete for vulkan.")

except FileNotFoundError:
    print(f"File '{input_file_path}' not found.")
except Exception as e:
    print("An error occurred:", str(e))   


