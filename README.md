# Description
This repository seeks to document and automate the evaluation process of image poses generated during reconstruction when using colmap

## 1.0.0 General Info
OS: Ubuntu 22.04 <br>
"{i}" indicates specific directory paths for reference, where you need to install the following three repositories and other resources.
These paths can be chosen at your discretion, use your own paths instead of {i} and ensure their utilization within the 'configuration_flags.txt' file to configure the settings(following section).
When running the scripts do not change the contained files within the directories involved because that could cause unwanted problems

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
Open configuration_flags.txt which is located at {6} and paste your directory paths, follow the structure below: <br>
--crop_gen_path={1}/vrg_crop_gen <br>
--colmap_path={2}/colmap <br>
--slam_evaluation_path={3}/slam-evaluation <br>
--vrg_colmap_evaluation_path={6} <br>
{6} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation" <br>
This is the path of the current repository
  
## 1.0.5 Creating the dataset using vrg_crop_gen
First a dataset has to be created. Read the documentation of vrg_crop_gen to learn about the process. 
After modifying the vk_glasses_flags.txt inside vrg_crop_gen and following the documentation, and modifying the configuration_of_scenes/config_general/config0.yaml
(others yamls inside have been moved in order to run only one creation of one dataset), run the script inside the source directory found in {7} to create the dataset using the following command <br>
{7} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/source"
- bash create_dataset.sh

## 1.0.6 Reconstruction (manual process)
This is the manual process of reconstruction. This is the suggested path to follow because they are way more configurations to work with and that will lead to a better reconstruction.
If you will follow this section skip section ## 1.0.7 else skip this and go directly to ## 1.0.7 for the automated process

1) Preparing the dataset <br>
This script moves the images within the target directory found in latest.txt one parent directory up,
to avoid dublicates when reconstructing. The latest.txt has the directory name of the latest dataset created if you followed ## 1.0.5.
If you want to prepare another directory just change the line inside latest.txt to the directory name you want to prepare.
This script again just moves all the images inside around_view_rgb within output_dataset_images directly at output_dataset_images.
Navigate at {6}/source and execute "bash prepare_dataset.sh"

2) Manually reconstructing through colmap
- Navigate at {2}/colmap/build by typing in the terminal "cd {2}/colmap/build" 
- Open the colmap GUI by typing in the terminal "colmap gui"
- At the GUI navigate File -> Project
- Click "New" at the Database section, navigate inside the dataset directory created, located at {6}/projects/* where the * is the name of the directory containing the dataset you want to reconstruct, name it "database", click "Save"
- Click "Select" on Images section, navigate to {6}/projects/*/output_dataset_images directory and click open
- Click "Save"
- File -> Save project, navigate at {6}/projects/* directory and name it "project" 

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/a336bf98-323f-4ed6-abdc-60ca92ffacc8 "This is the structure you should have")

- Processing → Feature extraction 
- Some configurations should change depending on your dataset but this is just a demonstration of what I have been doing with the dataset created from vrg_crop_gen
- Change camera model by clicking on "SIMPLE_RADIAL" which is the default option, to "SIMPLE_PINHOLE"
- Check "Shared for all images"
- Check "Custom parameters"
- To write the custom parameters navigate to {1}/vrg_crop_gen/source through file explorer or terminal
- Open vk_glasses_csv_flags.txt  
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/681d2f9c-087a-4be4-aade-69620611d223 "Check f, cx, cy")
- Now depending on your vk_glasses_csv_flags.txt write in the colmap section the f, cx, cy you checked. Note that in my case fx, fy and f are all the same
- Again feel free to modify any configurations as you wish. This is why I recommend the manual process
- Click "Extract"
- Once the exctraction is finished, close the tab for extraction and go back to the colmap main gui
- Processing → Feature Matching
- If the number of images is a few hundreds select "Exhaustive" method or else check colmap documentation for recommendations. Again modify any configurations you find necessary
- Click "Run"
- Once finished close the Feature Matching tab
- Next back in the main colmap gui click Reconstruction → Start reconstruction
- Once finished File → Export all models and select the {6}/projects/* directory
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/64df17f0-79ca-4949-9594-2186e49d15b5 "This is the sparse reconstruction")
- At this point the sparse reconstruction has been created. Now exporting the model by following the previous step creates a directory that contains some binary files, but we care about images.bin which are the estimates for the images in binary format
- This is in binary form, for our convenience we want to create them in text format. Previous step was done just for book keeping
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/eadbdcd4-c841-4195-938f-60a20143ae10 "Inside * directory")

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/8154320f-05a8-41fe-95de-fc780f07d0fb "Inside 0 directory")

- File → Export model as text, and select the "0" directory to export as txt

## 1.0.7 Reconstruction (automated process)





















