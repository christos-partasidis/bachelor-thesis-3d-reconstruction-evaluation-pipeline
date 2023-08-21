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

# THE FOLLOWING SECTION IS USED TO CREATE THE DATASET
#==================================================================
#==================================================================
#==================================================================

around_height=${1:-20}
around_radius=${2:-18}
ground_fov=${3:-50}
folder="${var_values[0]}/source/configuration_of_scenes/config_general"
file_list=$(ls "$folder")
sum=0
results_folder="${var_values[0]}/results"

for file in $file_list
do
  plant=$(grep -m 1 "plant" "$folder/$file" | awk '{print $2}' | tr -d '\n')
  nb_of_images=$(grep "nb_of_images" "$folder/$file" | awk '{print $2}')
  view=$(grep "view" "$folder/$file" | awk '{print $2}' | tr -d '\n')
  
  vrg_crop_gen_source_dir="${var_values[0]}/source"

  if cd "$vrg_crop_gen_source_dir"; then
            echo "Changed directory to: $vrg_crop_gen_source_dir"
	else
            echo "Failed to change directory to: $vrg_crop_gen_source_dir"
	fi

  python3.10 create_scene.py --path_config $folder/$file
  python3.10 create_view.py --view $view --path_config $folder/$file --sum_dataset $sum --around_height $around_height --around_radius $around_radius --ground_fov $ground_fov
  if [ -d "output" ]; then
    # The "output" directory exists, so proceed to delete it
    rm -r output
    echo "Directory 'output' deleted successfully."
  else
    # The "output" directory does not exist
    echo "Directory 'output' does not exist. Nothing to delete."
  fi
  cd vulkan_vrglasses_csv/vrglasses_for_robots/build/
  ./vrglasses4robots_csv --flagfile=../../../vk_glasses_csv_flags.txt
  cd ../../..
  if [ "$view" == "around" ]; then
  python3.10 extract_images_or_semantic.py --view around --extract rgb --path_config $folder/$file --sum_dataset $sum 
  elif [ "$view" == "top" ]; then
  python3.10 extract_images_or_semantic.py --view top --extract rgb --path_config $folder/$file --sum_dataset $sum
  python3.10 extract_images_or_semantic.py --view top --extract semantic --focus plants --path_config $folder/$file --sum_dataset $sum
  elif [ "$view" == "ground" ]; then
  python3.10 extract_images_or_semantic.py --view ground --extract rgb --path_config $folder/$file --sum_dataset $sum
  python3.10 extract_images_or_semantic.py --view ground --extract semantic --focus background --path_config $folder/$file --sum_dataset $sum
  python3.10 create_sky.py --path_config $folder/$file --sum_dataset $sum
  fi
  
  
  # Get the current time and create a folder name
  current_time=$(date +'%Y%m%d_%H%M%S')
  time_folder="$results_folder/${plant}_${view}_$current_time"
  mkdir -p "$time_folder"

  # Moving output and images folder 
  # Check if "output" directory exists and move it to the the 'time_folder'
  if [ -d "output" ]; then
    mv "output" "$time_folder"
    echo "Moved 'output' directory to $time_folder"
  else  
    echo "Directory 'output' not found in the current folder."
  fi
  # Check if "images" directory exists and move it to the 'time_folder'
  if [ -d "images" ]; then  
    mv "images" "$time_folder"
    echo "Moved 'images' directory to $time_folder"
  else
    echo "Directory 'images' not found in the current folder."
  fi

  # Check and move additional files to the 'time_folder'
  if [ -f "model_poses_list.txt" ]; then
      mv "model_poses_list.txt" "$time_folder"
      echo "Moved 'model_poses_list.txt' to $time_folder"
  else
      echo "File 'model_poses_list.txt' not found in the current folder."
  fi

  if [ -f "model_def_list.txt" ]; then
      mv "model_def_list.txt" "$time_folder"
      echo "Moved 'model_def_list.txt' to $time_folder"
  else
      echo "File 'model_def_list.txt' not found in the current folder."
  fi

  if [ -f "image_poses.txt" ]; then
      mv "image_poses.txt" "$time_folder"
      echo "Moved 'image_poses.txt' to $time_folder"
  else
      echo "File 'image_poses.txt' not found in the current folder."
  fi

  sum=$((sum + nb_of_images))
  echo "Total nb_of_images: $sum"
  
  # Form the new target directory path
  target_directory="${var_values[3]}/projects"

  # Extract the directory name from $time_folder
  directory_name=$(basename "$time_folder")
  echo "directory_name:$directory_name"

  # Move $time_folder to the target directory
  if mv "$time_folder" "$target_directory"; then
      echo "Moved $time_folder to $target_directory"
  else
      echo "Failed to move $time_folder"
  fi

  project_directory="${target_directory}"
  echo "project_directory:$project_directory"


  # Change to the target directory
  cd "$target_directory"


  # Change to the directory using its name
  cd "$directory_name"
  

  # Rename the "output" directory to "output_dataset_h5"
  if mv output output_dataset_h5; then
      echo "Renamed 'output' directory to 'output_dataset_h5'"
  else
      echo "Failed to rename 'output' directory"
  fi

  # Create a new directory named "output_dataset_txt"
  if mkdir output_dataset_txt; then
      echo "Created 'output_dataset_txt' directory"
      
      # Move all .txt files (except 'vk_glasses_csv_flags.txt') to the "output_dataset_txt" directory
      for file in *.txt; do
          if [ "$file" != "vk_glasses_csv_flags.txt" ]; then
              mv "$file" output_dataset_txt/
          fi
      done
      
      echo "Moved all .txt files (except 'vk_glasses_csv_flags.txt') to 'output_dataset_txt' directory"
  else
      echo "Failed to create 'output_dataset_txt' directory"
  fi

  # Rename the "images" directory to "output_dataset_images"
  if mv images output_dataset_images; then
      echo "Renamed 'images' directory to 'output_dataset_images'"
  else
      echo "Failed to rename 'images' directory"
  fi


done











































