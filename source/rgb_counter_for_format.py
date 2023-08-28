# rgb_counter_for_format.py

import sys
import os

def count_lines(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)

def create_rgb_file(filename, line_count):
    directory = os.path.dirname(filename)
    rgb_filename = f"{directory}/rgb.txt"
    
    with open(rgb_filename, 'w') as rgb_file:
        for i in range(1, line_count):
            rgb_file.write(f"{i}\n")
        rgb_file.write(f"{line_count}\n")  # Write the last line without newline


if len(sys.argv) != 2:
    print("Usage: python rgb_counter_for_format.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
line_count = count_lines(filename)
print(f"Number of lines in '{filename}': {line_count}")


create_rgb_file(filename, line_count - 1)
print(f"rgb.txt created with {line_count} lines.")








