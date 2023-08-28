#!/bin/bash


# THE FOLLOWING SECTION IS USED TO READ THE CONFIGURATION_FLAGS.TXT
#==================================================================
#==================================================================
#==================================================================

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define the path to the text file
CONF_TXT_FILE="$SCRIPT_DIR/../configuration_flags.txt"

# Declare indexed arrays to store variable names and values
declare -a var_names=()
declare -a var_values=()

# Check if the text file exists
if [ -f "$CONF_TXT_FILE" ]; then
    # Read the text file line by line
    while IFS= read -r line; do
        # Remove leading and trailing whitespaces from the line
        trimmed_line=$(echo "$line" | tr -d '[:space:]')
        
        # Extract variable name and value
        if [[ $trimmed_line == --*=* ]]; then
            
            var_name="${trimmed_line/=*/}"
            var_value="${trimmed_line/*=/}"
            
            # Print variable name and value
            echo "Variable: $var_name"
            echo "Value: $var_value"
            
	    # Store the variable names and values in indexed arrays
            var_names+=("$var_name")
            var_values+=("$var_value")
        
        else
            echo " "
        fi
    done < "$CONF_TXT_FILE"
    # Print the first variable and value from indexed arrays
    if [ ${#var_names[@]} -gt 0 ]; then
        echo "First Variable: ${var_names[0]}"
        echo "First Value: ${var_values[0]}"
    else
        echo "No variables found in the text file."
    fi
else
    echo "Text file not found: $CONF_TXT_FILE"
fi
# COMMENTS
# 0 -> crop_gen_path, 1 -> colmap_path, 2 -> slam_evaluation_path
# 4 -> evaluation_path
#==================================================================
#==================================================================
#==================================================================
#$var_values[2]

# Get the parent directory of the current directory
parent_dir=$(dirname "$(pwd)")

# Path to the "latest.txt" file in the "projects" directory
latest_file="$parent_dir/projects/latest.txt"

# Check if the file exists
if [ -f "$latest_file" ]; then
    # Read the first line of the file, remove white spaces, and store it in a variable
    latest_data=$(head -n 1 "$latest_file" | tr -d '[:space:]')
    
    # Print the data for verification
    echo "Data from latest.txt: $latest_data"

    # Check if a directory with the name in latest_data exists in the projects directory
    project_dir="$parent_dir/projects/$latest_data"
    if [ -d "$project_dir" ]; then
        echo "Directory $project_dir exists."

        # Move files to the specified directory
        target_dir="${var_values[2]}"
        if [ ! -d "$target_dir" ]; then
            echo "Target directory $target_dir does not exist. Exiting..."
            exit 1
        fi

        python3.10 rgb_counter_for_format.py "$project_dir/evaluation/ground_truth.txt"
        cd ..
        cd source

        # Check if files exist before moving

        if [ ! -f "$project_dir/evaluation/ground_truth.txt" ]; then
            missing_files+=("ground_truth.txt")
        fi

        if [ ! -f "$project_dir/evaluation/estimated_trajectory.txt" ]; then
            missing_files+=("estimated_trajectory.txt")
        fi

        if [ ! -f "$project_dir/evaluation/rgb.txt" ]; then
            missing_files+=("rgb.txt")
        fi

        if [ ${#missing_files[@]} -eq 0 ]; then
            
            # Move files
            mv "$project_dir/evaluation/ground_truth.txt" "$target_dir"
            mv "$project_dir/evaluation/estimated_trajectory.txt" "$target_dir"
            mv "$project_dir/evaluation/rgb.txt" "$target_dir"
            echo "Files moved (ground_truth.txt, estimated_trajectory.txt, rgb.txt) to $target_dir"

            # Change to slam_evaluation/src directory and execute the command to evaluate
            cd "$target_dir/src"
            
            while [ ! -f "../ground_truth.txt" ] || [ ! -f "../estimated_trajectory.txt" ] || [ ! -f "../rgb.txt" ]; do
                sleep 1  # Wait for a second before checking again
                
                missing_files=()

                if [ ! -f "../ground_truth.txt" ]; then
                    missing_files+=("ground_truth.txt")
                fi

                if [ ! -f "../estimated_trajectory.txt" ]; then
                    missing_files+=("estimated_trajectory.txt")
                fi

                if [ ! -f "../rgb.txt" ]; then
                    missing_files+=("rgb.txt")
                fi

                if [ ${#missing_files[@]} -eq 1 ]; then
                    echo "Waiting for ${missing_files[0]} to be moved..."
                elif [ ${#missing_files[@]} -eq 2 ]; then
                    echo "Waiting for ${missing_files[0]} and ${missing_files[1]} to be moved..."
                elif [ ${#missing_files[@]} -eq 3 ]; then
                    echo "Waiting for ${missing_files[0]}, ${missing_files[1]}, and ${missing_files[2]} to be moved..."
                fi
            done
            # echo "INSIDE TARGET_DIR/SRC"

            # for item in ../*; do
            #     echo "$item"
            # done

            # exit 1

            ./main_executable ../ground_truth.txt ../estimated_trajectory.txt ../rgb.txt --max_interpolation_timespan 2 --all_visualizations --write_estimated_trajectory_ply
            
            echo "Finished evaluation."

            # Sleep for 2 seconds
            sleep 2

            # Move files from evaluation back to the evaluation directory
            mv *.ply *.svg "$project_dir/evaluation/"
            echo "Moved .ply .svg evaluation files back to project"

            # Move to slam-evaluation directory
            cd ..
            
            # Move specific files to the evaluation directory
            mv "ground_truth.txt" "estimated_trajectory.txt" "rgb.txt" "$project_dir/evaluation/"
            echo "Moved ground_truth, estimated_trajectory, rgb back to project"

            
            
        else
            echo "The following required files are missing: ${missing_files[@]}. Exiting..."
            exit 1
        fi

    else
        echo "Directory $project_dir does not exist."
        exit 1
    fi

else
    echo "File $latest_file not found."
    exit 1
fi














