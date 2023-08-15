# Description
This repository seeks to document and automate the evaluation process of image poses generated during reconstruction when using colmap.

## General Info
OS: Ubuntu 22.04
"{i}" indicates specific directory paths for reference, where you need to install the following three repositories and other resources.
These paths can be chosen at your discretion, use your own paths instead of {i} and ensure their utilization within the 'configuration.txt' file to configure the settings in a subsequent section.

## Install vrg_crop_gen
Follow the process at https://github.com/VIS4ROB-lab/vrg_crop_gen and install it in a specific folder{1}.
{1} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/dataset-simulation-fixing/vrg_crop_gen"

## Install colmap
Follow the installation process at https://colmap.github.io/install.html and install it in a specific folder{2}.
{2} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/colmap"

## Install slam-evaluation
You can find the repo in this link https://github.com/ETH3D/slam-evaluation . There is no documentation on how
to install it so below you can find the steps to do so
{3} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/slam-evaluation"

1. Install the repository in a specific folder{3}. I followed the steps below. Type them in a terminal.
- cd {3}
- git clone https://github.com/ETH3D/slam-evaluation.git
- cd slam-evaluation/src
  
2. Download Eigen 3.4.0 (in .tar.bz2) from http://eigen.tuxfamily.org/index.php?title=Main_Page#Download 
- Open a terminal and navigate to the directory where you downloaded the Eigen archive{4}
- cd {4} 
- Use the following commands to extract the archive:
- tar -xjf eigen-eigen-*.tar.bz2





