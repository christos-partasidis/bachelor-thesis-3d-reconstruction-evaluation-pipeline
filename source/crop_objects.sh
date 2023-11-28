#!/bin/bash

# The following section is used to read the latest.txt
#==================================================================
#==================================================================
#==================================================================

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
else
    echo "File $latest_file not found."
    exit 1
fi

#==================================================================
#==================================================================
#==================================================================


# The following section is used to read the configurations_flags.txt
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
#$var_values[2]
#==================================================================
#==================================================================
#==================================================================

# THE FOLLOWING SECTION RUNS THE PYTHON SCRIPT
#==================================================================
#==================================================================
#==================================================================

latest_data="../projects/$latest_data"
echo "latest_data: $latest_data"

file_path_to_model_dir="${var_values[0]}/resources/model"
echo "file_path_to_model_dir: $file_path_to_model_dir"

python3.10 crop_objects.py $latest_data $file_path_to_model_dir

#==================================================================
#==================================================================
#==================================================================