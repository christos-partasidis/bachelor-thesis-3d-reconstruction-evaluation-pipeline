# Description
This repository seeks to document and automate the evaluation process of the image poses and the scene generated using colmap

## 1.0.0 General Info
OS: Ubuntu 22.04 <br>
python: 3.10 <br>
"{i}" indicates specific directory paths for reference, where you need to install the following three repositories and other resources.
These paths can be chosen at your discretion, use your own paths instead of {i} and ensure their utilization within the 'configuration_flags.txt' file to configure the settings(following section) <br>
When running the scripts do not change the contained files within the directories involved because that could cause unwanted problems

## 1.0.1 Install vrg_crop_gen
Follow the process at https://github.com/VIS4ROB-lab/vrg_crop_gen and install it in a specific directory {1} <br>
Warning! The vrglasses_csv that must be installed with vrg_crop_gen (in vrg_crop_gen documentation) must be placed inside the dedicated folder found within vrg_crop_gen or else the scripts 
will not work and manual changes must be done

{1} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/dataset-simulation-fixing"

## 1.0.2 Install colmap
Follow the installation process at https://colmap.github.io/install.html and install it in a specific directory {2} <br>
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

2. Install the repository in a specific directory {3}. I followed the steps below. Type them in a terminal
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
After modifying the vk_glasses_flags.txt found in {1}/vrg_crop_gen in the following way <br>
""" <br>
--output_folder_path={1}/vrg_crop_gen/source/output <br>
--fx=2559 <br>
--fy=2559 <br>
--cx=1536 <br>
--cy=1152 <br>
--far=1000 <br>
--near=0.10000000000000001 <br>
--output_h=2304 <br>
--output_w=3072 <br>
--mesh_obj_file= <br>
--mesh_texture_file= <br>
--model_folder={1}/vrg_crop_gen/resources <br>
--model_list_file={1}/vrg_crop_gen/source/model_def_list.txt <br>
--model_pose_file={1}/vrg_crop_gen/source/model_poses_list.txt <br>
--ortho=false <br>
--pose_file={1}/vrg_crop_gen/source/image_poses.txt <br>
--resource_folder=/media/secssd/tmp/render_test/a13 <br>
--shader_folder={1}/vrg_crop_gen/source/vulkan_vrglasses_csv/vrglasses_for_robots/shaders <br>
--step_skip=1 <br>
""" <br>
Note:
output_h, output_w (height and width of output images) and fx, fy, cx, cy (focal length, principal point) can be modified as you wish

Follow the documentation of vrg_crop_gen to modify the {1}/vrg_crop_gen/source/configuration_of_scenes/config_general/config0.yaml as you wish to create a specific scene.
(others yamls inside have been moved in order to run only one creation of one dataset). Run the script inside the source directory found in {7} to create the dataset using the following command <br>
{7} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/source"
- bash create_dataset_general.sh

## 1.0.6 Reconstruction (manual process)
This is the manual process of reconstruction. This is the suggested path to follow because they are way more configurations to work with and that will lead to a better reconstruction(instead of the automatic).
If you will follow this section skip section ## 1.0.7 else skip this and go directly to ## 1.0.7 for the automated process

1) Preparing the dataset for reconstruction <br>
This script moves the images within the target directory (that has to be in {6}/projects) one parent directory up to avoid dublicates when reconstructing. The name of the target directory is found in {6}/projects/latest.txt 
The latest.txt has the directory name of the latest dataset created if you followed ## 1.0.5.
If you want to prepare another directory just change the line inside latest.txt to the directory name you want to prepare.
This script again just moves all the images inside around_view_rgb within output_dataset_images directly at output_dataset_images.
Navigate at {6}/source and execute "bash prepare_dataset.sh"

2) Manually reconstructing through colmap
- Navigate at {2}/colmap/build by typing in the terminal "cd {2}/colmap/build" 
- Open the colmap GUI by typing in the terminal "colmap gui"
- At the GUI navigate File -> New project
- Click "New" at the "Database" section, navigate inside the dataset directory created, located at {6}/projects/* where the * is the name of the directory containing the dataset you want to reconstruct, name it "database", click "Save"
- Click "Select" at the "Images" section, navigate to {6}/projects/*/output_dataset_images directory and click open
- Click "Save"
- File -> Save project, navigate at {6}/projects/* directory, name it "project" , slick "Save"

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
- Once finished click File → Export all models and select the {6}/projects/* directory and click "Open"
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/64df17f0-79ca-4949-9594-2186e49d15b5 "This is the sparse reconstruction")
- At this point the sparse reconstruction has been created. Now exporting the model by following the previous step creates a directory that contains some binary files, but we care about images.bin which are the estimates for the images in binary format
- This is in binary form, for our convenience we want to create them in text format. Previous step was done just for book keeping
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/eadbdcd4-c841-4195-938f-60a20143ae10 "Inside * directory")

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/8154320f-05a8-41fe-95de-fc780f07d0fb "Inside 0 directory")

- File → Export model as text, select the "0" directory and click "Open". This will export them as .txt <br>
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/9fcfd29e-1043-4d4e-b915-b014e2583c48 "Inside 0 directory")
- At this point this is enough to create the evaluation of the image poses, dense reconstruction can be skipped if you only want to evaluate the estimated poses(the following steps of this section). If you want to <br>
also evaluate the estimated scenes continue with the dense reconstruction
- Reconstruction → Dense reconstruction
- Click "Select" to select a workspace, choose {6}/projects/* directory
- Click "Undistortion"
- Click "Stereo"
- Click "Fusion"
- Click "Poisson"
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/aa2e8ee9-088f-4f78-a408-e0c908c42edd)


## 1.0.7 Reconstruction (automated process)
* paused *

## 1.0.8 Preparing the text files of the poses for the evaluation
Before continuing some clarifications
1) The {6}/projects/*/output_dataset_txt/image_poses.txt text file contains the ground truth of the image poses
2) The {6}/projects/*/0/images.txt text file contains the estimated image poses <br>
- To remove any extra data, and to bring it in a format acceptable by the slam_evaluation repository run the following script. Please keep in mind that the script will perform the formatting on the directory found within "latest.txt" found in {6}/projects/ much like before
- Within {6}/source run "bash format_all.sh" <br>
This will create a directory called "evaluation" within {6}/projects/*/ that will include ground_truth.txt for the ground truth of the image poses and estimated_trajectory.txt for the estimated image poses but all formatted

## 1.0.9 Running the evaluation of the image poses
At {6}/source run the evaluation script. Keep in mind that the project that will be evaluated is the project that is in latest.txt
- bash evaluate.sh <br>
Check within {6}/projects/*/evaluation the trajectories
![Screenshot from 2023-10-13 22-33-01](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/30616fe6-c5cb-4d7c-93c5-f8cace6b4a05)
![Screenshot from 2023-10-13 22-31-56](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/9b445a62-2936-42ad-8b20-d3a81439e9db)


## 1.0.10 Creating the ground truth point cloud
At {6}/source run the script. Keep in mind that the project that will be the base for the creation is in latest.txt
- bash create_ground_truth_point_cloud.sh

## 1.1.0 Python script to remake the .mtl files in the models
The models found in {1}/vrg_crop_gen/resources/model need to have an appropriate .mtl file. For most of the objects that file might be missing or needs a modification.
The script named "create_mtls.py" found in the {6}/source (this repository) automates the process of the creating the .mtl files.
There is an exception for the Fence objects. Only the Fence2 object has a valid texture. If you want to add other fence objects the script must be modified.
Below you can find the steps to run the script
1) Take the script "create_mtls.py" and place it at {1}/vrg_crop_gen/resources
2) Run the python script

## 1.1.1 Creating bounding boxes(aabb) for all the objects(.ply)
To create bounding boxes for all objects(.ply) in {1}/vrg_crop_gen/resources/model run create_aabb.sh that is found in {6}/source
1) bash create_aabb.sh <br>
Note: If you want to create bounding boxes for other .ply files not in vrg_crop_gen check create_aabb.py

## 1.1.2 Cropping models with aabb and ground truth poses (v.1.0.1)
crop_objects.py <br>
Performs the following tasks: <br>
1. Read object names (under criteria) used for the creation of the scene -> selected_objects (in model_def_list.txt) <br>
2. Read poses of selected_objects (in model_poses_list.txt) <br>
3. Read the ground point cloud <br>
4. Reads all .ply from vrg_crop_gen/resources/model (or other specified directory) and stores for each selected <br>
   object their corresponding file path for the raw .ply and the _bounding_box.ply <br>
5. Combines and visualizes aabbs(both pcd and mesh) of selected_objects with ground truth point cloud <br>

crop_objects.sh <br>
Runs crop_objects.py based on the current repository

To run the script execute: <br>
bash crop_objects.sh <br>

TODO: <br>
1) Align colmap on ground truth <br>
2) Crop models from ground truth <br>
3) Crop models from colmap <br>
4) Compare cropped models <br>

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/5e783c23-4306-4dd8-ba08-1c8ed08b5840)

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/5f06cdfe-e6d9-4218-91b7-e7a156fb2ad1)

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/7c58ba3c-765b-4804-b501-7801b4abfa5a)

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/59dd2d6f-0064-4e3d-b44a-2f8700eea8f8)












