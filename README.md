# Description
This repository seeks to document and automate the evaluation process of the image poses and the scene generated using colmap

**Bachelor Thesis PDF:**  
[Download the full thesis](./Bachelor%27s%20Thesis%20Report%20by%20Christos%20Partasidis.pdf)

## 1.0.0 General Info
OS: Ubuntu 22.04 <br>
python: 3.10 <br>
colmap: 3.9 (Commit 2226fa1 on 2023-07-05 with CUDA) <br>
"{i}" indicates specific directory paths for reference, where you need to install the following three repositories and other resources.
These paths can be chosen at your discretion, use your own paths instead of {i} and ensure their utilization within the 'configuration_flags.txt' file to configure the settings(following section) <br>
When running the scripts do not change the contained files within the directories involved because that could cause unwanted problems. <br>
Also this README contains extra information to explain extra programs. Please watch out for indications of when to execute something in order to follow the MAIN PIPELINE.<br>
If you don't see an indication saying that this is not in the MAIN PIPELINE then it belong to it so execute it. <br>
To see any visualizations you must modify the variable within the scripts to run it in Debug mode (set it to TRUE) <br>
For further details check the report of this work <br>

## 1.0.1 Install vrg_crop_gen
Follow the process at https://github.com/VIS4ROB-lab/vrg_crop_gen and install it in a specific directory {1} <br>
Warning! The vrglasses_csv that must be installed with vrg_crop_gen (in vrg_crop_gen documentation) must be placed inside the dedicated folder found within vrg_crop_gen or else the scripts 
will not work and manual changes must be done

{1} = "/home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/dataset-simulation-fixing"<br>

Within the report you will see experiments that have modified the view of the images. If you want to <br>
add degrees to the around trajectory (see explanation in report) like in the experiments the create_view.py <br>
with modifications is provided here so you can replace it with the default one<br>

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
After modifying the vk_glasses_flags.txt found in {1}/vrg_crop_gen/source in the following way <br>
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
- File -> Save project, navigate at {6}/projects/* directory, name it "project" , click "Save"

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/a336bf98-323f-4ed6-abdc-60ca92ffacc8 "This is the structure you should have")

- Processing → Feature extraction 
- Some configurations should change depending on your dataset but this is just a demonstration of what I have been doing with the dataset created from vrg_crop_gen
- Change camera model by clicking on "SIMPLE_RADIAL" which is the default option, to "SIMPLE_PINHOLE"
- Check "Shared for all images"
- Check "Custom parameters"
- To write the custom parameters navigate to {1}/vrg_crop_gen/source through file explorer or terminal
- Open vk_glasses_csv_flags.txt  <br><br>
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/681d2f9c-087a-4be4-aade-69620611d223 "Check f, cx, cy")
- Now depending on your vk_glasses_csv_flags.txt write in the colmap section the f, cx, cy you checked. Note that in my case fx, fy and f are all the same<br>
- Again feel free to modify any configurations as you wish. This is why I recommend the manual process<br>
- Click "Extract"<br>
- Once the exctraction is finished, close the tab for extraction and go back to the colmap main gui<br>
- Processing → Feature Matching<br>
- If the number of images is a few hundreds select "Exhaustive" method or else check colmap documentation for recommendations. Again modify any configurations you find necessary<br>
- Click "Run"<br>
- Once finished close the Feature Matching tab<br>
- Next back in the main colmap gui click Reconstruction → Start reconstruction<br>

#### Sparse point cloud
![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/64df17f0-79ca-4949-9594-2186e49d15b5 "This is the sparse reconstruction")

<br>

- Once finished click File → Export all models and select the {6}/projects/* directory and click "Open" <br>
- At this point the sparse reconstruction has been created. Now exporting the model by following the previous step creates a directory that contains some binary files, but we care about images.bin which are the estimates for the images in binary format
- This is in binary form, for our convenience we want to create them in text format. Previous step was done just for book keeping <br>

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/eadbdcd4-c841-4195-938f-60a20143ae10 "Inside * directory")

![image](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/8154320f-05a8-41fe-95de-fc780f07d0fb "Inside 0 directory")

- File → Export model as text, select the "0" directory and click "Open". This will export them as .txt <br><br>
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

## 1.1.2 Aligning models (v.1.0.0)
Using colmap model_aligner we are aligning the ground_truth and the estimated colmap scene

align_models.py <br>
Arguments: <br>
1. <path_to_project>: The path to the project <br>

Performs the following tasks: <br>
1. Creates "align" directory within the project directory <br>
2. Read poses of images from "image_poses.txt" from within the directory "output_dataset_txt" <br>
3. Modifies read poses and stores them in "ground_truth_geo_registration.txt" within "aligning" directory <br>

align_models.sh <br>
Arguments: None <br>
Peforms the following tasks: <br>
1. Read latest.txt <br>
2. Run align_models.py <br>
3. Run colmap model_aligner <br>

Execution: <br>
Run the align_models.sh - "bash align_models.sh" <br>

Result: <br>
After executing the above script, inside the project directory ({6}/projects/*) there will be an directory called "align". Within the "align" directory <br>
they will exist three .bin files. Using these we will reconstruct the aligned dense scene

## 1.1.3 Creating dense scene (manually)
This process is currently performed manually (in the future check colmap cli)<br>
Steps:
1. Navigate at {2}/colmap/build - "cd {2}/colmap/build" 
2. Open the colmap GUI by - "colmap gui"
3. "File" -> "Import model", and select the directory {6}/projects/*/align where the * is the project that is in {6}/projects/latest.txt (currently working on)
4. You will be asked to "specify a valid database and image path". Click "Yes"
5. In the "Database" section click "New", name it "database" and click "Save"
6. In the "Images" section click "Select", navigate one parent directory up at {6}/projects/* and select the "images" directory {6}/projects/*/images, Click "Open"
7. Click "Save"
8. "Reconstruction" -> "Dense reconstruction"
9. At the "Workspace" section, click "Select" and select the {6}/projects/*/align directory, and click "Open"
10. Click "Undistortion", when done click "Stereo", when done click "Fusion", if asked to visualize the scene click "Yes", click "Poisson"
11. Close the colmap gui, optionally save the project
   
## 1.1.4 Cropping models with bb and ground truth poses (v.1.0.4)
### crop_objects.py <br>
**Description:** <br>
For the ground truth scene and the colmap scene it crops the objects selected (the type of the objects is set statically within the file) and stores them in specific directories.
Also it combines the cropped objects and voxelizes them.

**Performs the following tasks:** <br>
1. Read object names (under criteria) used for the creation of the scene -> selected_objects (in model_def_list.txt) <br>
2. Read poses of selected_objects (in model_poses_list.txt) <br>
3. Read and visualize the ground point cloud <br>
4. Read and visualize the colmap (aligned) point cloud <br>
5. Reads all .ply from vrg_crop_gen/resources/model (or other specified directory) and stores for each selected <br>
   object their corresponding file path for the raw .ply <br>
6. Combines and visualizes bbs(both pcd and mesh) of selected_objects with ground truth and colmap (aligned) point clouds <br>
7. Combines and visualizes pcd of ground truth and colmap (aligned)
8. Crop objects from ground truth pcd and store them
9. Crop objects from colmap (aligned) pcd and store them
10. Visualize and store combined ground truth and colmap (aligned) cropped objects
11. Voxelize ground truth and colmap (aligned) cropped objects


**Arguments:** <br>
1. <file_path_to_project>: provide the path to the project that contains output_dataset_txt and ground_truth_point_cloud.xyz <br>
2. <file_path_to_model_dir>: provide the path to the parent directory that in resources/model has the models e.g. check vrg_crop_gen

**Example execution: (EXTRA NOT IN MAIN PIPELINE)** <br>
python3.10 crop_objects.py Apple_Winter_around_20231126_200513 /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/dataset-simulation-fixing/vrg_crop_gen/resources/model


### crop_objects.sh <br>
**Description:** <br>
Runs crop_objects.py based on the current repository meaning that it:
1. Reads the {6}/projects/latest.txt to find the project to perform the cropping
2. Reads the {6}/configurations_flags.txt to identify the path to the resources/model directory that contains the models of the objects

**Example execution:** <br>
bash crop_objects.sh <br>

### Ground truth
#### Ground truth pcd (side view)
![Screenshot from 2023-10-21 01-40-20](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/d79237a7-aa1e-4100-929c-d09c5adca094)

#### Combined pcd of ground truth and aabb (top view)
![Screenshot from 2023-10-21 01-42-01](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/e24da6b5-afc2-489c-b853-af0a17d1dc62)

#### Combined pcd of ground truth and aabb (side view)
![Screenshot from 2023-10-21 01-43-38](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/b72f6bc9-b860-4680-8d0f-337b2c87d942)

#### Combined pcd of ground truth and meshes of aabb (top view)
![Screenshot from 2023-10-21 01-44-44](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/58b6f895-26c5-4790-8980-eebe0e57cd6b)

#### Combined pcd of ground truth and meshes of aabb (side view)
![Screenshot from 2023-10-21 02-07-43](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/12e078d5-7a56-4abc-84d7-606a17a33d3a)




### Colmap aligned
#### Colmap aligned pcd (side view)
![Screenshot from 2023-10-21 01-31-02](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/8d49f148-ae29-4043-be99-6d8f87b6f2dc)

#### Combined pcd of colmap aligned and aabb (top view)
![Screenshot from 2023-10-21 01-24-33](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/e4be5471-6c38-4ef3-93ed-95bda008bbed)

#### Combined pcd of colmap aligned and aabb (side view)
![Screenshot from 2023-10-21 01-26-06](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/348d05ba-3cf7-4591-92ac-588dac8e3982)

#### Combined pcd of colmap aligned and meshes of aabb (top view)
![Screenshot from 2023-10-21 01-27-14](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/b2868371-1bd8-476e-ad0e-22d2baed0d71)

#### Combined pcd of colmap aligned and meshes of aabb (side view)
![Screenshot from 2023-10-21 01-28-30](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/ad61a4d5-8bae-496a-ad3d-678622fc9708)




### Ground truth and colmap aligned
#### Ground truth and colmap aligned (top view)
![Screenshot from 2023-10-21 03-08-13](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/e9d62a50-e4c8-4bdd-9efd-c0f957d96f3e)

#### Ground truth and colmap aligned (side view)
![Screenshot from 2023-10-21 03-09-04](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/941becd8-567a-4dca-abb4-79ca938b9262)

#### Ground truth and colmap aligned (zoomed at trees)
![Screenshot from 2023-10-21 03-10-47](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/74b3ef94-e2b5-4a76-8636-9f332fff19b5)

### Ground truth cropped 
#### Ground truth cropped object
![gt_cropped_object](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/7f736081-af0e-4880-a043-ea4dd31607fd)

#### Ground truth cropped object with bounding box
![gt_cropped_object_w_bb](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/9b5880e9-5a82-45ad-98ce-35186c3d7c71)

#### Ground truth combined cropped objects (top view)
![all_gt_cropped_object_top](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/ef4c580c-9cc4-48e3-8fc9-e8ea5291ad4b)

#### Ground truth combined cropped objects (side view)
![all_gt_cropped_object_side](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/ba3d40e4-b2ff-4785-8574-c850d61e3f3a)

#### Ground truth combined cropped objects with bounding boxes (top view)
![all_gt_cropped_object_top_w_bb](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/ab5e81d5-cd7f-4702-beae-d12b924d92f9)

#### Ground truth combined cropped objects with bounding boxes (side view)
![all_gt_cropped_object_top_w_bb_s](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/705646f8-af72-48d8-9d65-1386c1ec0ebd)





### Colmap aligned cropped 
#### Colmap aligned cropped object
![colmap_cropped_object](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/17fde309-8af4-4b57-830b-620d6ac059e9)

#### Colmap aligned cropped object with bounding box
![colmap_cropped_object_w_bb](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/f3fb5e90-ea1a-420f-bf51-10dd22ec6c24)

#### Colmap aligned combined cropped objects (top view)
![all_colmap_cropped_object_top](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/bff86783-c1af-4534-bcea-3fa8472f39a8)

#### Colmap aligned combined cropped objects (side view)
![all_colmap_cropped_object_side](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/4ab658dc-e15a-46bb-9590-e425f4e1da0b)

#### Colmap aligned combined cropped objects with bounding boxes (top view)
![all_colmap_cropped_object_top_w_bb](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/3b1739bc-7a25-403d-8d0d-4a70cd07c755)

#### Colmap aligned combined cropped objects with bounding boxes (side view)
![all_colmap_cropped_object_top_w_bb_s](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/0ec705e9-787f-4080-9440-2d2496ba6ad9)




### Combined cropped 
#### Combined cropped objects
#### Blue: Ground truth
#### Green: Colmap

![combined_1](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/eb3bc082-c831-4204-a2a9-dcc827731602)

![combined_2](https://github.com/VIS4ROB-lab/vrg_colmap_reconstruction_evaluation/assets/113234371/3df5ae5e-7057-4afa-9a61-1de4db9a8a06)

## 1.1.5 Comparing voxel grids (groundtruth, colmap)

### compare_voxel_grids_temp.py v.1.0.0 (not in main pipeline) <br>
**Description:** <br>
Contais all the tests that have been tried. This is not in the main pipeline. 
Keep in mind that if an unexpected error when running it is found it might be due to memory limitations (e.g. on VSCode). When I was using jupyter notebook no error was detected but when moved to VSCode the error occurs if all sections are runned at the same time. It was due to multiple plots not able to be windowed

### compare_voxel_grid_gt.py v.1.0.2 <br>
**Description:** <br>
Compares Ground truth -> Estimated (Colmap) for a single cropped object and stores metrics<br>

**Performs the following tasks:** <br>

**GENERAL**<br>

0. Importing modules and reading arguments
1. Defining functions
2. Configuration
3. Read voxel grids of ground truth and estimated (colmap)
4. Extract from the voxels the coordinates and the values from both ground truth and colmap
5. Extract from the coordinates the ground truth and colmap centers
   and create the respective point clouds
   
**TEST_1: VOXEL MATCHING GROUND TRUTH -> COLMAP (based on center w boundaries)** <br>

6. Find voxels in ground truth that exist in estimate (based on center w boundaries)
7. Convert matched voxel coords to point cloud and voxel grid
8. Color found voxels with original (blue) and not found with red
9. Print and save comparison metrics for matching (based on center w boundaries)

**TEST_2 VOXEL DISTANCE GROUND TRUTH -> COLMAP (based on center with boundaries)**

10. Find nearest voxel at estimated voxel grid for all ground truth voxels (based on center with boundaries)
11. Print and save comparison metrics for distances (based on center with boundaries)

**Arguments:** <br>
1. <path_to_gt_voxel_grid>: The path to the ground truth cropped object <br>
2. <path_to_colmap_voxel_grid>: The path to the colmap cropped object <br>
3. <voxel_size>: It is used when converting centers to point cloud and creating the corresponding voxel grid <br>
4. <-bound->:  It is used for searching the area around a center, both for matching and distance <br>
5. <random_colors_TF> (optional): True: the final voxel grids will have random colors, False (default): the final voxel grids will have original colors <br>
6. <color_map_value> (optional): It is the color map used to convert distances to colors (default: viridis:  Low:Blue, High: Yellow, check matplotlib doc for other) <br>

**Example execution: (EXTRA NOT IN MAIN PIPELINE)** <br>
python3.10 compare_voxel_grid_gt.py /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443/gt_cropped_objects/1_gt_Apple_Trunk1_light_voxelized.ply /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443/colmap_a_cropped_objects/1_colmap_Apple_Trunk1_light_voxelized.ply 0.3 0.3 false viridis

### compare_voxel_grid_colmap.py v.1.0.2<br>
**Description:** <br>
Compares Estimated (Colmap) -> Ground truth for a single cropped object and stores metrics<br>

**Performs the following tasks:** <br>

**GENERAL** <br>

0. Importing modules and reading arguments
1. Defining functions
2. Configuration
3. Read voxel grids of ground truth and estimated (colmap)
4. Extract from the voxels the coordinates and the values from both ground truth and colmap
5. Extract from the coordinates the ground truth and colmap centers
   and create the respective point clouds
 
**TEST_1: VOXEL MATCHING COLMAP -> GROUND TRUTH (based on center w boundaries)**

6. Find voxels in estimate that exist in ground truth (based on center w boundaries)
7. Convert matched voxel coords to point cloud and voxel grid
8. Color found voxels with original (green) and not found with red
9. Print and save comparison metrics for matching (based on center w boundaries)

**TEST_2 VOXEL DISTANCE COLMAP -> GROUND TRUTH  (based on center with boundaries)**

10. Find nearest voxel at ground truth voxel grid for all estimated voxels (based on center with boundaries)
11. Print and save comparison metrics for distances (based on center with boundaries)

**Arguments:** <br>
Same as compare_voxel_grid_gt.py<br>

**Example execution: (EXTRA NOT IN MAIN PIPELINE)** <br>
python3.10 compare_voxel_grid_colmap.py /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443/gt_cropped_objects/1_gt_Apple_Trunk1_light_voxelized.ply /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443/colmap_a_cropped_objects/1_colmap_Apple_Trunk1_light_voxelized.ply 0.3 0.3 false viridis

### compare_voxel_grids_all.py v1.0.2<br>
**Description:** <br>
Used to run both compare_voxel_grid_gt.py and compare_voxel_grid_colmap.py for all cropped objects. It also <br>
creates average metrics for all objects

**Performs the following tasks:** <br>

0. Import modules and read arguments
1. Defining classes and functions
2. Configuration
3. Read gt and colmap voxelized .ply files
4. Runs compare_voxel_grid_gt.py and compare_voxel_grid_colmap.py
   for voxelized cropped objects found in the project
5. Calculates and saves the total average metrics

**Arguments:** <br>
1. <path_to_project>: The path to the project that contains the cropped objects<br>
2. <voxel_size>: It is used when converting centers to point cloud and creating the corresponding voxel grid<br>
3. <-bound->: It is used for searching the area around a center, both for matching and distance<br>
4. <random_colors_TF> (optional): True: the final voxel grids will have random colors, False (default): the final voxel grids will have original colors<br>
5. <color_map_value> (optional): It is the color map used to convert distances to colors (default: viridis:  Low:Blue, High: Yellow, check matplotlib doc for other)<br>

**Example execution:** <br>
python3.10 compare_voxel_grids_all.py /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443 0.3 0.3 false viridis

### compare_voxel_grids_all_multiple.py v.1.0.0<br>
**Description:** <br>
Used to run compare_voxel_grids_all.py multiple times with different voxel sizes and bound sizes that are statically defined [0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.2, 1.5, 1.7,  2.0]
**Performs the following tasks:** <br>

0. Importing modules and reading arguments
1. Run multiple times compare_voxel_grids_all.py but change the voxel and bound size each time<br>

**Arguments:** <br>
1. <path_to_project>: provide the path to the project (that contains colmap_a_cropped_objects and gt_cropped_objects)<br>
2. <voxel_size>: provide the voxel size of the voxel grids<br>
3. <random_colors_TF (optional)>: true -> random colors to voxel grids, false (default) -> original colors<br>
4. <color_map_value (optinal)>: color mapping of distances is done using matplotlib and they are a lot of options<br>
   e.g. viridis (default): Low - Blue / High - Yellow, RdY1Gn: Low - Green / High - Red<br>

**Example execution: (EXTRA NOT IN MAIN PIPELINE)** <br>
python3.10 compare_voxel_grids_all_multiple.py /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443 0.3 false viridis

### compare_metrics_all.py v.1.0.1<br>
**Description:** <br>
After running compare_voxel_grids_all_multiple.py, running this script will create plots that plot different metrics in correspondence with the different bound values

**Performs the following tasks:** <br>
0. Importing modules and reading arguments <br>
1.Read metrics for different bound sizes <br>
2. Create plots for metrics of different bound sizes <br>

**Arguments:** <br>
1. <path_to_project>: provide the path to the project (that contains colmap_a_cropped_objects and gt_cropped_objects)<br>

**Example execution: (EXTRA NOT IN MAIN PIPELINE)** <br>
python3.10 compare_metrics_all.py /home/christos/Desktop/Gate/thesis/3d-reconstruction/programs/evaluation_repo/vrg_colmap_reconstruction_evaluation/projects/Apple_Winter_around_20231020_162443







