# This is a python script to convert images.txt
# created from colmap to the compatible format

import sys
import os

# Check if at least one argument (excluding the script name) is provided
if len(sys.argv) < 2:
    print("Usage: python colmapt_to_format.py <latest_data>")
    sys.exit(1)

# The first command-line argument (sys.argv[1]) is the <latest_data> passed from the Bash script
latest_data = sys.argv[1]

# Define the input and output file paths
input_file_path = '../projects/' + latest_data + '/0/images.txt'
output_file_path = '../projects/' + latest_data + '/evaluation/estimated_trajectory.txt'

# Check if the "evaluation" directory already exists
evaluation_dir = os.path.dirname(output_file_path)
if os.path.exists(evaluation_dir):
    print("The 'evaluation' directory already exists. Exiting to avoid overwriting.")
    sys.exit(1)

try:
    # Read the input file and filter lines
    filtered_lines = []
    with open(input_file_path, 'r') as input_file:
        for index, line in enumerate(input_file):

            # Skip lines that start with '#'
            if line.startswith('#'):
                continue

            if line.strip().endswith('.png'):
                elements = line.strip().split()
                if len(elements) >= 6:
                    elements[1], elements[-1] = elements[-1], elements[1] 
                    del elements[1]
                    # Exchange positions of the second, third, and fourth elements with the fifth, sixth, and seventh elements
                    elements[1], elements[2], elements[3], elements[4], elements[5], elements[6] = \
                        elements[4], elements[5], elements[6], elements[1], elements[2], elements[3]
                    del elements[-2]

                filtered_lines.append(" ".join(elements) + '\n')

    # Add header line at the beginning of the output file
    header_line = "# time x y z qx qy qz qw\n"
    filtered_lines.insert(0, header_line)

    # Create the "evaluation" directory if it doesn't exist
    os.makedirs(evaluation_dir)

    # Write the filtered lines to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(filtered_lines)

    print("Conversion complete for colmap.")

except FileNotFoundError:
    print(f"File '{input_file_path}' not found.")
except Exception as e:
    print("An error occurred:", str(e))















































