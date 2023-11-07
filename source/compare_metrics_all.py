#
# The following script performs the following
# 0. Importing modules and reading arguments
# 1. Read metrics for different bound sizes
# 2. Create plots for metrics of different bound sizes

# Section: 0
## Importing modules and reading arguments
#===================================================================================
#===================================================================================
#===================================================================================
import subprocess
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import rc

# Enable LaTeX rendering for text formatting
rc('text', usetex=True)

# Get the path to the current script
script_path = sys.argv[0]
# Get the name
script_name = os.path.basename(script_path)

print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 0 | " + script_name)
print("Importing modules and reading arguments\n")

print("Reading arguments")

if len(sys.argv) != 2:
    print("Length of arguments: ", len(sys.argv))
    print("Usage: python compare_metrics_all.py 1<path_to_project>")
    print("path_to_project: provide the path to the project (that contains colmap_a_cropped_objects and gt_cropped_objects)")
    sys.exit(1)

# 1. Read path to project
path_to_project = sys.argv[1]

# Check if project directory exists
if not os.path.exists(path_to_project):
    print(f"The project directory '{path_to_project}' does not exist. Please provide a valid path.")
    sys.exit(1)

# Print read arguments
print("==============================================================================================")
print("Read arguments")
print("1. path_to_project: ", path_to_project)
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 1
## Read metrics for different bound sizes
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 1 | " + script_name)
print("Read metrics for different bound sizes\n")

# Initialize a dictionary to store the metrics and their corresponding values
metrics_dict = {
    "name_of_test": [],
    "avg_gt_voxels_matched": [],
    "min_gt_distance": [],
    "max_gt_distance": [],
    "avg_gt_mae": [],
    "avg_gt_rmse": [],
    "avg_gt_mse": [],
    "avg_colmap_voxels_matched": [],
    "avg_colmap_recall": [],
    "min_colmap_distance": [],
    "max_colmap_distance": [],
    "avg_colmap_mae": [],
    "avg_colmap_rmse": [],
    "avg_colmap_mse": [],
}

# List all directories in the specified path that start with "metrics" but are not "metrics_general"
subdirectories = [d for d in os.listdir(path_to_project) if os.path.isdir(os.path.join(path_to_project, d)) and d.startswith("metrics") and d != "metrics_general"]

# Iterate through the subdirectories and read the "avg_metrics.txt" file
for directory in subdirectories:
    avg_metrics_file = os.path.join(path_to_project, directory, "avg_metrics.txt")
    try:
        with open(avg_metrics_file, "r") as file:
            metrics_dict["name_of_test"].append(directory)
            lines = file.readlines()
            for line in lines:
                # Split the line into TITLE and VALUE using the ":" as the separator
                parts = line.strip().split(":")
                if len(parts) == 2:
                    title, value = parts[0].strip(), parts[1].strip()
                    # Check if the TITLE is in the metrics_dict
                    if title in metrics_dict:
                        # Append the value to the corresponding attribute in the dictionary
                        metrics_dict[title].append(value)

    except FileNotFoundError:
        print(f"File not found: {avg_metrics_file}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while processing {avg_metrics_file}: {str(e)}")
        sys.exit(1)

print("\nMetrics dictionary before sort\n")
# Now, metrics_dict contains the attributes and their corresponding values
# You can access the values for each attribute as lists in metrics_dict
for title, values in metrics_dict.items():
    print(f"{title}: {values}")

# Initialize list to store suffixes of bound to use for sort
suffix_values = []

# Sort dictionary by bounding: small -> high
# Extract the last two integers, add a ".", convert to float, and add to the list
for name in metrics_dict["name_of_test"]:
    last_two_integers = name.split('_')[-2:]
    float_value = float(f"{last_two_integers[0]}.{last_two_integers[1]}")
    suffix_values.append(float_value)

# Sort the list of suffix_values with corresponding indices
sorted_suffix_values = []
sorted_indices = []

for i, value in enumerate(suffix_values):
    index = len(sorted_suffix_values)
    for j, sorted_value in enumerate(sorted_suffix_values):
        if value < sorted_value:
            index = j
            break
    sorted_suffix_values.insert(index, value)
    sorted_indices.insert(index, i)

# Permute the data dictionary based on the sorted indices
for key, values in metrics_dict.items():
    metrics_dict[key] = [values[i] for i in sorted_indices]
    
print("\nMetrics dictionary after sort\n")
for title, values in metrics_dict.items():
    print(f"{title}: {values}")
#===================================================================================
#===================================================================================
#===================================================================================

# Section: 2
## Create plots for metrics of different bound sizes
#===================================================================================
#===================================================================================
#===================================================================================
print("\n")
print("==============================================================================================")
print("==============================================================================================")
print("Section: 2 | " + script_name)
print("Create plots for metrics of different bound sizes\n")

# Define the path to metrics_general directory
metrics_general_dir = os.path.join(path_to_project, "metrics_general")

# Create the "metrics_general" directory if it doesn't exist
if not os.path.exists(metrics_general_dir):
    os.makedirs(metrics_general_dir)

# Plot and save graphs for each attribute
for attribute, values in metrics_dict.items():
    if attribute != "name_of_test":
        plt.figure(figsize=(8, 6))
        
        # Set the background color to light blue for the entire figure
        fig = plt.gcf()
        fig.patch.set_facecolor('lightblue')
    
        # Plot the data on top of the background
        plt.plot(sorted_suffix_values, [float(value) for value in values], marker='o')
        plt.xlabel(r'\textbf{Bound sizes}', fontsize=22)
        plt.ylabel(r'\textbf{' + attribute + r'}', fontsize=22)
        plt.title(r'\textbf{' + attribute + r' vs. Bound sizes}', fontsize=24)


        # Adjust the margins for labels
        plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.grid(True)

        # Save the plot in the "metrics_general" directory
        plot_filename = os.path.join(metrics_general_dir, f"{attribute}_plot.png")
        plt.savefig(plot_filename)
        plt.close()


print("Plots saved in the 'metrics_general' directory.")
#===================================================================================
#===================================================================================
#===================================================================================



