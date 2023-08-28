#!/bin/bash

cd ../projects

# Check if latest.txt exists
if [ ! -f "latest.txt" ]; then
    echo "Error: latest.txt is not present. It must be created before running this script."
    exit 1
fi

# Read the value from latest.txt and remove leading/trailing whitespace
directory_name=$(cat latest.txt | tr -d '[:space:]')

# Check if the specified directory exists
if [ ! -d "$directory_name" ]; then
    echo "Error: The directory '$directory_name' specified in latest.txt does not exist."
    exit 1
fi

# Navigate to the directory with the name from latest.txt
cd "$directory_name" || exit 1

# Move the images (both .jpg and .png) one level up
find "output_dataset_images/around_view_rgb" -type f \( -name "*.jpg" -o -name "*.png" \) -exec mv {} "output_dataset_images/" \;

# Remove the now-empty around_view_rgb directory
rm -r "output_dataset_images/around_view_rgb"

echo "Images moved and directories cleaned up."