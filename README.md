# Description
This repository seeks to document and automate the evaluation process of image poses generated during reconstruction when using colmap

## 1.0.0 General Info
OS: Ubuntu 22.04 <br>
"{i}" indicates specific directory paths for reference, where you need to install the following three repositories and other resources.
These paths can be chosen at your discretion, use your own paths instead of {i} and ensure their utilization within the 'configuration.txt' file to configure the settings in a subsequent section
When running the scripts do not change the items of the directories involved because that could cause unwanted problems

## 1.0.1 Install vrg_crop_gen
Follow the process at https://github.com/VIS4ROB-lab/vrg_crop_gen and install it in a specific folder {1} <br>
Warning! The vrglasses_csv that must be installed with vrg_crop_gen (in vrg_crop_gen documentation) must be placed inside the dedicated folder found within vrg_crop_gen or else the scripts 
will not work and manual changes must be done

{1} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/dataset-simulation-fixing"

## 1.0.2 Install colmap
Follow the installation process at https://colmap.github.io/install.html and install it in a specific folder {2} <br>
{2} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs"

## 1.0.3 Install slam-evaluation
Below you can find the steps to install it.
You can find the repository in this link https://github.com/ETH3D/slam-evaluation

{3} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs" <br>
{4} = "/home/christos/Downloads" <br>
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
  
## 1.0.4 Configuring the configuration_flags.txt
- Open configuration_flags.txt and paste your directory paths, follow the structure below:
--crop_gen_path={1}/vrg_crop_gen
--colmap_path={2}/colmap
--slam_evaluation_path={3}/slam-evaluation
--vrg_colmap_evaluation_path={6}
{6} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation"
This is the path of the current repository
  
## 1.0.5 Creating the dataset using vrg_crop_gen
First a dataset has to be created. Read the documentation of vrg_crop_gen to learn about the process. 
After modifying the vk_glasses_flags.txt inside vrg_crop_gen and following the documentation, and modifying the configuration_of_scenes/config_general/config0.yaml
(others yamls inside have been moved in order to run only one creation of one dataset), run the script inside the src directory {7} to create the dataset using the following command
{7} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/source"
- bash create_dataset.sh

## 1.0.6 





















