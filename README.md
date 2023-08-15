# Description
This repository seeks to document and automate the evaluation process of image poses generated during reconstruction when using colmap

## General Info
OS: Ubuntu 22.04 <br>
"{i}" indicates specific directory paths for reference, where you need to install the following three repositories and other resources.
These paths can be chosen at your discretion, use your own paths instead of {i} and ensure their utilization within the 'configuration.txt' file to configure the settings in a subsequent section

## Install vrg_crop_gen
Follow the process at https://github.com/VIS4ROB-lab/vrg_crop_gen and install it in a specific folder {1} <br>
{1} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/dataset-simulation-fixing"

## Install colmap
Follow the installation process at https://colmap.github.io/install.html and install it in a specific folder {2} <br>
{2} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs"

## Install slam-evaluation
Below you can find the steps to install it.
You can find the repository in this link https://github.com/ETH3D/slam-evaluation

{3} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs"
{4} = "/home/christos/Downloads"
{5} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/slam-evaluation/src"

1. Download Eigen 3.4.0 (in .tar.bz2) from http://eigen.tuxfamily.org/index.php?title=Main_Page#Download 
- Open a terminal and navigate at the directory where it contains the archive by typing "cd {4}"
- Extract the archive by typing "tar -xjf eigen-*.tar.bz2". Use the "tab" button to fill the *

2. Install the repository in a specific folder {3}. I followed the steps below. Type them in a terminal
- cd {3}
- git clone https://github.com/ETH3D/slam-evaluation.git

3. Compile the program
- Navigate within the slam-evaluation/src directory using "cd {5}"
- Type "g++ -o main_executable main.cc -I {4}/eigen-*". Use the "tab" button to fill the *
  
## Creating the dataset using vrg_crop_gen
First a dataset has to be created. Read the documentation of vrg_crop_gen to learn about the process. 
After modifying the vk_glasses_flags.txt inside vrg_crop_gen and following the documentation, and modifying the configuration_of_scenes/config_general/config0.yamkl
(others yamls inside have been moved in order to run only one creation of a dataset), run the script inside src to...























