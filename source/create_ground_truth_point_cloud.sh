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
echo "${var_values[0]}"

# THE FOLLOWING SECTION IS USED TO READ THE LATEST.TXT
#==================================================================
#==================================================================
#==================================================================
LATEST_TXT_FILE="$SCRIPT_DIR/../projects/latest.txt"
# Check if the file exists
if [ -f "$LATEST_TXT_FILE" ]; then
    # Read the first line from the file
    first_line=$(head -n 1 "$LATEST_TXT_FILE")
    echo "latest.txt: $first_line"
else
    echo "$LATEST_TXT_FILE does not exist. Exiting."
    exit 1
fi
# THE FOLLOWING SECTION IS USED TO READ THE MODEL_POSES_LIST.TXT
#==================================================================
#==================================================================
#==================================================================

# Define the path to the model_poses_list.txt file
MODEL_POSES_TXT_FILE="$SCRIPT_DIR/../projects/$first_line/output_dataset_txt/model_poses_list.txt"

# Check if the file exists
if [ ! -f "$MODEL_POSES_TXT_FILE" ]; then
    echo "File $MODEL_POSES_TXT_FILE does not exist. Exiting."
    exit 1
fi

# THE FOLLOWING SECTION IS USED TO READ THE OBJECTS WITHIN MODEL
# INSIDE CROP_GEN
#==================================================================
#==================================================================
#==================================================================

# Define the path to the model directory inside crop_gen
CROP_GEN_MODEL_DIR="${var_values[0]}/resources/model"
# Check if the directory exists
if [ ! -d "$CROP_GEN_MODEL_DIR" ]; then
    echo "Directory $CROP_GEN_MODEL_DIR does not exist. Exiting."
    exit 1
fi

# Call the Python script with MODEL_POSES_TXT_FILE as an argument
python3.10 create_ground_truth_point_cloud.py "$MODEL_POSES_TXT_FILE" "$CROP_GEN_MODEL_DIR"

# Check the exit code of the Python script
python_exit_code=$?

# Check if the Python script exited with an error
if [ $python_exit_code -ne 0 ]; then
    echo "Python script create_ground_truth_point_cloud.py exited with an error (Exit Code: $python_exit_code). Exiting shell script."
    exit $python_exit_code
fi

echo "Success: Created the ground truth of the point cloud"















