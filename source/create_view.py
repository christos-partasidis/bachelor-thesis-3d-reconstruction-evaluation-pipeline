import numpy as np
from pathlib import Path
import argparse
import pywavefront
from scipy.spatial import KDTree
import math
import yaml
from yaml.loader import SafeLoader

class Crop:
    def __init__(self):
        self.name = 'Apple_Summer'
        self.size_crop_x = 10
        self.size_crop_y = 10
        self.terrain = 'Terrain'
        self.view = 'ground'
        self.nb_of_pictures = 0
        self.sum_dataset = 0
        self.can_walk_through_plant = False
        self.ground_fov = 50
        self.half_ground_fov = self.ground_fov/2
        self.around_height = 10
        self.around_radius = 32
        self.around_angle = -110 #-125

        self.yaw = 0
        self.x_spacing = 1
        self.y_spacing = 1


    def get_quaternion_from_euler(self, roll, pitch, yaw):

        qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(
            yaw / 2)
        qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)
        qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)
        qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(
            yaw / 2)

        return [qx, qy, qz, qw]


    def path_aerial_view(self):

        pov = ['timestamp, p_x, p_y,p_z, q_x, q_y,q_z, q_w\n']
        # depending of the density of the plants on the terrain, the ground and top view grid are set differently,
        # If it is a crop like an orchard, we set the grid to have view that are between trees (as if we walk through orchard)
        if self.can_walk_through_plant == True:
            y = np.arange(-self.size_crop_y / 2, self.size_crop_y / 2, self.y_spacing)
            x = np.linspace(-self.size_crop_x / 2, self.size_crop_x / 2, math.ceil(self.nb_of_pictures / np.shape(y)[0]))

        # If it is a crop like a field, we set the grid to be a square. This gird make sense only for top view as we can't walk through dense field plants
        else:
            nb_of_x_per_line = math.ceil(np.sqrt(self.nb_of_pictures))
            nb_of_y_per_line = math.ceil(np.sqrt(self.nb_of_pictures))
            y = np.linspace(-self.size_crop_y / 2, self.size_crop_y / 2, nb_of_y_per_line)
            x = np.linspace(-self.size_crop_x / 2, self.size_crop_x / 2, nb_of_x_per_line)

        #create the 2d grid
        xv, yv = np.meshgrid(x, y)
        nb_img_per_line = np.shape(xv)[1]
        column_x = xv.flatten()
        column_y = yv.flatten()

        # offset on x to have better views on orchards for PV2BEV (in order to see the first trees)
        if self.can_walk_through_plant == True:
            offset = 7
        else: offset = 0

        # reduce the variable column_x and column_y to have the same shape
        column_x = column_x[:self.nb_of_pictures] - offset
        column_y = column_y[:self.nb_of_pictures]

        # Add noise to the camera poses to have a better training set
        noise_height = np.random.normal(loc=0, scale=0.1, size=(np.shape(column_y)[0]))
        noise_y = np.random.normal(loc=0, scale=0.2, size=(np.shape(column_y)[0]))
        noise_rot_z = np.random.normal(loc=0, scale=0.3, size=(np.shape(column_y)[0]))
        noise_rot_x = np.random.normal(loc=0, scale=0.03, size=(np.shape(column_y)[0]))

        # add offset to be between plants and add noise
        column_y += self.y_spacing / 2 + noise_y
        column_z = np.zeros(column_x.shape[0], int)

        # height of drone to see the distance of self.half_ground_fov on the ground (represented by height of the image), we need AOV_y
        S_y = output_d = 480
        focal_length = 572
        AOV_y = 2 * math.atan2(S_y / 2.0, focal_length)
        height_drone = self.half_ground_fov / (np.tan(AOV_y / 2))  # 25/(np.tan(AOV_y/2)) #20/...

        # get z-coordinate of the terrain
        if self.terrain != "None":
            path_to_terrain = '../resources/model/Terrain/' + str(self.terrain) + '.obj'
            terrain = pywavefront.Wavefront(path_to_terrain)
            terrain_vertices = np.array(terrain.vertices)

            x = terrain_vertices[:, 0].ravel()
            y = terrain_vertices[:, 1].ravel()
            z = terrain_vertices[:, 2].ravel()

            grid_plant = np.stack((column_x, column_y), axis=1)

            tree = KDTree(np.c_[x, y])
            dd, ii = tree.query(grid_plant, k=1)
            # z_coordinate of camera adapted in fonction of terrain
            z_adapted = z[ii]
            column_z = z_adapted


        if self.view == "ground":
            ## Ground view: creation of the view through the trees
            with open('image_poses.txt', 'w') as f:
                list_quaternion = np.zeros((np.shape(column_x)[0], 4))

                # angle of camera adapted in fonction of slope
                rot_x_array = []
                for j in range(len(column_x)):
                    if j % (nb_img_per_line - 1) != 0 and j != len(column_x) - 1:
                        # y =tan(x)
                        # take the actual and the next z-axis to incline the camera in order to better see the crop
                        x = (column_z[j + 1] - column_z[j]) / (column_x[j + 1] - column_x[j])
                        rot_x_array.append(np.arctan(x))
                    else:
                        rot_x_array.append(0)
                rot_x_array = np.array(rot_x_array)

                # angle of the camera
                for i in range(np.shape(column_x)[0]):
                    rot_z = (-90) * np.pi / 180 + noise_rot_z[i]
                    rot_x = -90 * np.pi / 180 + noise_rot_x[i] + rot_x_array[i]
                    rot_y = 0
                    qx, qy, qz, qw = self.get_quaternion_from_euler(rot_x, rot_y, rot_z)
                    list_quaternion[i] = [qx, qy, qz, qw]

                # write each poses on a file
                for i in range(np.shape(column_x)[0]):
                    # height of an humain/ground_robot holding a camera + height of the terrain
                    height = 1.5 + column_z[i] #+ noise_height[i]
                    qx, qy, qz, qw = list_quaternion[i, :]
                    lines = 'DJI_' + str(i+self.sum_dataset) + '.JPG,' + str(column_x[i]) + ',' + str(column_y[i]) + ',' + str(
                        height) + ',' + str(qx) \
                            + ',' + str(qy) + ',' + str(qz) + ',' + str(qw) + "\n"
                    pov.append(lines)

                f.writelines(pov)


        if self.view == 'top':
            ##Top view: creation of the view above the scene
            with open('image_poses.txt', 'w') as f:
                column_x_top = column_x + self.half_ground_fov * np.cos(noise_rot_z) #25 #20
                column_y_top = column_y + self.half_ground_fov * np.sin(noise_rot_z) #25 #20

                list_quaternion = np.zeros((np.shape(column_x)[0], 4))
                # angle of the camera
                for i in range(np.shape(column_x_top)[0]):
                    rot_z = (-90) * np.pi / 180 + noise_rot_z[i]
                    rot_x = -180 * np.pi / 180 + noise_rot_x[i]
                    rot_y = 0
                    qx, qy, qz, qw = self.get_quaternion_from_euler(rot_x, rot_y, rot_z)
                    list_quaternion[i] = [qx, qy, qz, qw]

                # write each poses on a file
                for i in range(np.shape(column_x_top)[0]):
                    height = height_drone #59.47 #47.66 #+ column_z[i]
                    qx, qy, qz, qw = list_quaternion[i, :]
                    lines = 'DJI_' + str(i+self.sum_dataset) + '.JPG,' + str(column_x_top[i]) + ',' + str(column_y_top[i]) + ',' + str(
                        height) + ',' + str(qx) \
                            + ',' + str(qy) + ',' + str(qz) + ',' + str(qw) + "\n"
                    pov.append(lines)
                print('height_drone:', height)

                f.writelines(pov)

        if self.view == "around":
            with open('image_poses.txt', 'w') as f:
                ##MAKE A CIRCLE AROUND THE SCENE
                # angle in radian
                print("FIRST ITERATION")
                
                angle = -np.linspace(0, 3.3 * np.pi, num= self.nb_of_pictures)
                print("angle:", angle)

                radius = self.around_radius # 5
                print("angle:", angle)
                column_x_around = radius * np.cos(angle)
                print("column_x_around:", column_x_around)
                column_y_around = radius * np.sin(angle)
                print("column_y_around:", column_y_around)  

                rot_z = -np.linspace(0, 594, num= self.nb_of_pictures) * np.pi / 180 + 90 * np.pi / 180
                print("rot_z:", rot_z)
                rot_x = self.around_angle * np.pi / 180
                print("rot_x:", rot_x)
                rot_y = 0
                print("rot_y:", rot_y)

                list_quaternion = np.zeros((np.shape(angle)[0], 4))
                print("list_quaternion:", list_quaternion)

                for i in range(np.shape(angle)[0]):
                    qx, qy, qz, qw = self.get_quaternion_from_euler(rot_x, rot_y, rot_z[i])
                    list_quaternion[i] = [qx, qy, qz, qw]
                print("list_quaternion:", list_quaternion)

                for i in range(np.shape(column_x)[0]):
                    height = self.around_height + column_z[i] # 9
                    qx, qy, qz, qw = list_quaternion[i, :]
                    lines = 'DJI_' + str(i+self.sum_dataset) + '.JPG,' + str(column_x_around[i]) + ',' + str(column_y_around[i]) + ',' + str(
                        height) + ',' + str(qx) \
                            + ',' + str(qy) + ',' + str(qz) + ',' + str(qw) + "\n"
                    pov.append(lines)


                #==========================

                # self.around_height = self.around_height + 15
                # j = int(np.shape(column_x)[0] / 2)

                # for i in range(int(np.shape(column_x)[0]/2)):
                #     height = self.around_height + column_z[i + j] # 9
                #     qx, qy, qz, qw = list_quaternion[i + j, :]
                #     lines = 'DJI_' + str(i + j +self.sum_dataset) + '.JPG,' + str(column_x_around[i]) + ',' + str(column_y_around[i]) + ',' + str(
                #         height) + ',' + str(qx) \
                #             + ',' + str(qy) + ',' + str(qz) + ',' + str(qw) + "\n"
                #     pov.append(lines)

                f.writelines(pov)

        # This will create the top and ground view in the same time. This is usefull when we want to have the perfect
        # corresponding images for PV2BEV (because of the randomn noise of the camera)
        if self.view == 'top_and_ground':
            ##Ground view: creation of the view through the trees
            pov = ['timestamp, p_x, p_y,p_z, q_x, q_y,q_z, q_w\n']
            with open('image_poses_ground.txt', 'w') as f:
                list_quaternion = np.zeros((np.shape(column_x)[0], 4))

                #angle of camera adapted in fonction of slope
                rot_x_array = []
                for j in range(len(column_x)):
                    if j % (nb_img_per_line - 1) != 0 and j != len(column_x) - 1:
                        # y = tan(x)
                        x = (column_z[j + 1] - column_z[j])/(column_x[j + 1] - column_x[j])
                        rot_x_array.append(np.arctan(x))
                    else:
                        rot_x_array.append(0)
                rot_x_array = np.array(rot_x_array)

                # angle of the camera
                for i in range(np.shape(column_x)[0]):
                    rot_z = (-90) * np.pi / 180 + noise_rot_z[i]
                    rot_x = -90 * np.pi / 180 + noise_rot_x[i] + rot_x_array[i]
                    rot_y = 0
                    qx, qy, qz, qw = self.get_quaternion_from_euler(rot_x, rot_y, rot_z)
                    list_quaternion[i] = [qx, qy, qz, qw]

                # write each poses on a file
                for i in range(np.shape(column_x)[0]):
                    # height of a humain/ground_robot holding a camera + height of the terrain
                    height = 1.5 + column_z[i] + noise_height[i]
                    qx, qy, qz, qw = list_quaternion[i, :]
                    lines = 'DJI_' + str(i+self.sum_dataset) + '.JPG,' + str(column_x[i]) + ',' + str(column_y[i]) + ',' + str(
                        height) + ',' + str(qx) \
                            + ',' + str(qy) + ',' + str(qz) + ',' + str(qw) + "\n"
                    pov.append(lines)

                f.writelines(pov)


            pov = ['timestamp, p_x, p_y,p_z, q_x, q_y,q_z, q_w\n']
            ##Top view: creation of the view above the scene
            with open('image_poses_top.txt', 'w') as f:

                column_x_top = column_x + self.half_ground_fov * np.cos(noise_rot_z)  # 25 #20
                column_y_top = column_y + self.half_ground_fov * np.sin(noise_rot_z)  # 25 #20

                list_quaternion = np.zeros((np.shape(column_x)[0], 4))

                for i in range(np.shape(column_x_top)[0]):
                    rot_z = (-90) * np.pi / 180 + noise_rot_z[i]
                    rot_x = -180 * np.pi / 180 + noise_rot_x[i] #+rot_x_array[i]
                    rot_y = 0
                    qx, qy, qz, qw = self.get_quaternion_from_euler(rot_x, rot_y, rot_z)
                    list_quaternion[i] = [qx, qy, qz, qw]

                for i in range(np.shape(column_x_top)[0]):
                    height = height_drone + 1.5 + column_z[i] + noise_height[i]  # 59.47 #47.66
                    qx, qy, qz, qw = list_quaternion[i, :]
                    lines = 'DJI_' + str(i + self.sum_dataset) + '.JPG,' + str(column_x_top[i]) + ',' + str(
                        column_y_top[i]) + ',' + str(
                        height) + ',' + str(qx) \
                            + ',' + str(qy) + ',' + str(qz) + ',' + str(qw) + "\n"
                    pov.append(lines)
                print('height_drone_adapted:', height_drone+1.5+column_z[i])

                f.writelines(pov)


def read_config(crop,path_config):
    with open(path_config, 'r') as f:
        config = yaml.load(f, Loader=SafeLoader)
        crop.name = config['plant']
        crop.x_spacing = config['spacing']['x']
        crop.y_spacing = config['spacing']['y']
        crop.size_crop_x = config['size_crop']['x']
        crop.size_crop_y = config['size_crop']['y']
        crop.terrain = config['terrain']['type']
        crop.nb_of_pictures = config['nb_of_images']
        crop.view = config['view']

    if crop.y_spacing >= 1:
        crop.can_walk_through_plant = True
    else:
        crop.can_walk_through_plant = False

    return config


def main():
    #set the default directory
    default_path_folder = str(Path(__file__).parents[0])
    default_path_config = default_path_folder + '/config.yaml'

    # Initialization of the Class Crop
    crop = Crop()
    print('view')
    # get arguments
    parser = argparse.ArgumentParser(
        prog='ConfigView',
        description='Create path view',
        epilog='Text at the bottom of help')

    parser.add_argument('--view', choices=['top', 'ground', 'around', 'top_and_ground'], action='store',
                        default=crop.view, help='type of view (default: around)')
    parser.add_argument('--path_config', action='store', default=default_path_config,
                        help='path of the config.yaml file')
    parser.add_argument('--sum_dataset', action='store', default=0, type=int,
                        help='sum of the images of the dataset that are already produced')
    parser.add_argument('--ground_fov', action='store', default=50, type=int,
                        help='Ground field of view (y axis of sensor but x axis of scene)')
    parser.add_argument('--around_height', action='store', default=10, type=int,
                        help='height of the drone when doing the around view')
    parser.add_argument('--around_radius', action='store', default=32, type=int,
                        help='radius of the drone when doing the around view')
    parser.add_argument('--around_angle', action='store', default=-125, type=int,
                        help='angle of the drone from the z-axis when doing the around view')

    args = parser.parse_args()
    path_config = args.path_config
    crop.sum_dataset = args.sum_dataset
    crop.ground_fov = args.ground_fov
    crop.half_ground_fov = crop.ground_fov/2
    crop.around_height = args.around_height
    crop.around_radius = args.around_radius
    crop.around_angle = args.around_angle

    #yaml variables
    config_list = read_config(crop,path_config)

    #higher priority on arguments than yaml variables
    crop.view = args.view

    print('Configuration of the scene:',config_list)

    # Created the poses of the views of the scene
    crop.path_aerial_view()

    # update yaml if type_of_view is changed
    with open(path_config, 'w') as f:
        config_list['view'] = crop.view
        yaml.dump(config_list, f, sort_keys=False)


main()
