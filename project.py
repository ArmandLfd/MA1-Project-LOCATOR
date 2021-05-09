#-------------- Library -------------#
import os, sys, subprocess
from shutil import copyfile
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#------------- Functions ------------#
def extract_parameters(path):
    print("Extracting parameters . . .")
    file = None
    try:
        file = open(path,"rt")
    except:
        exit("Error : impossible to open the file.")
    param = []
    lines = 0
    for line in file:
        if lines == 15:
            break
        param.append(line.split()[1])
        lines += 1
    file.close()
    print("Extraction done !!!")
    return param

def check_and_create(path):
    if not os.path.exists(path):
        if not os.path.isDir(path):
            file_tmp = open(path,"w+")
            file_tmp.close()
        else:
            os.makedirs(path)

def check_essential_file(path):
    if not os.path.exists(path):
        exit("This file/folder should exist . . .\n File/Folder:" + path)

def light_raw_img(path_to_raw_img,number_of_img,path_dst):
    print("Copying only few images . . .")
    number_of_raw_img = len(list(enumerate(os.listdir(path_to_raw_img))))
    count_img = 0
    count_img_copied = 1
    if number_of_img >= number_of_raw_img:
        count_img = -number_of_raw_img
    else:
        count_img = number_of_raw_img//number_of_img
    for count, filename in enumerate(os.listdir(path_to_raw_img)):
        if filename.split(".")[1] == "png":
            if count%count_img == 0 or count_img < 0:
                src = path_to_raw_img + filename
                dst = path_dst + "image_" + str(count_img_copied) + ".png"
                copyfile(src,dst)
                count_img_copied += 1
    print("Copying images done !!!")

def build_param_RLC(path_param_Raytrix,path_param_dir,path_raw_img_dir,path_output_dir,width,height):
    print("Building parameters for RLC . . .")
    ext_param = ".xml"
    endline = "\n"
    param1 = "viewNum            5 \n" + "rmode              1 \n" +"pmode              0 \n" +"mmode              2 \n" +"lmode              1 \n" +"Calibration_xml    " + path_param_Raytrix +" \n" +"RawImage_Path      " + path_raw_img_dir
    param3 = "Output_Path        " + path_output_dir + "img"
    param4 = "Debayer_mode       0 \n" +"Isfiltering        0 \n" +"isCLAHE            0 \n" +  "Gamma              1.0 \n" +"Lambda             0.05 \n" +"Sigma              0 \n" +"input_model        0 \n" +"output_model       0 \n" +"start_frame        1 \n" +"end_frame          1 \n" +"height             "+ str(height) + "\n" + "width             "+str(width) +"\n"
    img = "image_"

    for count, filename in enumerate(os.listdir(path_raw_img_dir)):
        count += 1
        dst = path_param_dir + "param" + str(count) + ".cfg"
        param = param1 + img + str(count) + ".png" + endline + param3 + str(count) + endline + param4
        f = open(dst, "w")
        f.write(param)
        f.close()
    print("Building param done !!!")

def MRLC(path_param_dir,path_raw_img,path_RLC):
    print("Starting MRLC . . .")
    param = path_param_dir + "param"
    ext = '.cfg'
    for count, filename in enumerate(os.listdir(path_raw_img)):
        count += 1
        path_param = param + str(count) + ext
        try:
            subprocess.call([path_RLC, path_param])
        except:
            exit("Error : RLC crashed . . .")
    print("MRLC done !!!")

def extract_MV(path_viewpoint,path_output_MV,number_of_view):
    print("Start extracting viewpoints . . .")
    for count, filename in enumerate(os.listdir(path_viewpoint)):
        dst = path_viewpoint + "image_" + str(count) + ".png"
        os.remove(dst)

    if number_of_view != 0 and number_of_view != 2 and number_of_view != 1 and number_of_view != 3 and number_of_view != 4:
        exit("Enter a proper number_of_view : 0,1,2.")

    counter = 0
    count_dir = 1
    is_viewpoint = False
    for count, filename in enumerate(os.listdir(path_output_MV)):
        count += 1
        if os.path.isdir(path_output_MV + filename):
            for count2, filename2 in enumerate(os.listdir(path_output_MV + "img"+str(count_dir)+"/")):
                if number_of_view == 0:
                    if count2 == 12:
                        is_viewpoint = True
                if number_of_view == 1:
                    if count2 == 0 or count2 == 24:
                        is_viewpoint = True
                if number_of_view == 2 or number_of_view == 4:
                    if count2 == 0 or count2 == 4 or count2 == 20 or count2 == 24:
                        is_viewpoint = True
                if number_of_view == 3 or number_of_view == 4:
                    if count2 == 2 or count2 == 10 or count2 == 22 or count2 == 14:
                        is_viewpoint = True
                if is_viewpoint:
                    dst = "image_" + str(counter) + ".png"
                    src = path_output_MV+ "img"+str(count_dir) + "/" + filename2
                    dst = path_viewpoint + dst
                    counter += 1
                    copyfile(src, dst)
                    is_viewpoint = False
            count_dir += 1
    print("Extract viewpoints done !!!")

def colmap(colmap_path,image_path,database_path,project_path,output_path):
    print("Starting to use COLMAP . . .")
    try:
        if project_path != "None":
            subprocess.call([colmap_path,"feature_extractor","--project_path",project_path])
            subprocess.call([colmap_path,"exhaustive_matcher","--project_path",project_path])
            subprocess.call([colmap_path,"mapper","--project_path",project_path])
        else:
            subprocess.call([colmap_path,"feature_extractor","--image_path",image_path,"--database_path",database_path,"--ImageReader.camera_model","SIMPLE_RADIAL","--ImageReader.single_camera","1"])
            subprocess.call([colmap_path,"exhaustive_matcher","--database_path",database_path])
            subprocess.call([colmap_path,"mapper","--image_path",image_path,"--database_path",database_path,"--output_path",output_path,"--Mapper.init_min_tri_angle","10",])
        subprocess.call([colmap_path,"model_converter","--input_path",output_path+"0/","--output_path",output_path+"0/","--output_type","TXT"])
    except:
        exit("Error while calling COLMAP . . .")
    print("COLMAP Finished !!!")
    #------- Fct for BTraj -------#
#from colmap_to_json.py
def QuaternionToRotationMatrix(q):
	R1 = np.array([[q[0],q[3],-q[2],q[1]],
		[-q[3],q[0],q[1],q[2]],
		[q[2],-q[1],q[0],q[3]],
		[-q[1],-q[2],-q[3],q[0]]])
	R2 = np.array([[q[0],q[3],-q[2],-q[1]],
		[-q[3],q[0],q[1],q[2]],
		[q[2],-q[1],q[0],-q[3]],
		[q[1],q[2],q[3],q[0]]])
	R = R1.dot(R2)
	return R

def clean_line(line):
    args_line = line.split()
    quad = np.array([args_line[1],args_line[2],args_line[3],args_line[4]],dtype="float32")
    trans = np.array([[args_line[5]],[args_line[6]],[args_line[7]],[1]],dtype="float32")
    nb_img = args_line[9].split("image_")[1].split(".png")[0]
    return QuaternionToRotationMatrix(quad), trans, int(nb_img)

def build_coord(quad,trans):
    #quad_t = quad.transpose()
    #coord = -np.matmul(quad_t,trans)
    #return coord[2],-coord[0],-coord[1]
    return trans[2],trans[0],trans[1]
    #------------ End ------------#
def build_trajectory(path_to_coord,nb_views):
    print("Building trajectory . . .")
    nb_files = len(os.listdir(path_to_coord))
    nb_dir = 0
    for i in range(nb_files-1,-1,-1):
        if os.path.isdir(path_to_coord+str(i)+"/"):
            nb_dir = i
            break
    file = None
    try:
        file = open(path_to_coord+str(nb_dir)+"/images.txt","rt")
    except:
        exit("Error occured : do not suceed to open the file from ColMap.")
    #Skip commentaries
    for i in range(3):
        file.readline()
    number_of_viewpoints = file.readline().split(",")[0].split(" ")
    number_of_viewpoints = int(number_of_viewpoints[len(number_of_viewpoints)-1])
    if nb_views == 0:
        nb_views = 1
    elif nb_views == 1:
        nb_views = 2
    elif nb_views == 3 or nb_views == 2:
        nb_views = 4
    else:
        nb_views = 8
    #Loop and skip one line after reading one
    line_read = False
    x,y,z = np.zeros(number_of_viewpoints),np.zeros(number_of_viewpoints),np.zeros(number_of_viewpoints)
    for line in file:
        if not line_read:
            quad, trans, indx = clean_line(line)
            x_new, y_new, z_new = build_coord(quad, trans)
            x[indx] = x_new
            y[indx] = y_new
            z[indx] = z_new
        line_read =  not line_read
    file.close()

    print("Starting to plot in 3D . . .")
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title("3D Trajectory of the cameras")
    ax.plot(x,y,z,label="Lines",color='g')
    if nb_views != 1:
        ax.scatter(x[0:nb_views-1],y[0:nb_views-1],z[0:nb_views-1],label="Starting Point")
        ax.scatter(x[nb_views:len(x)-nb_views-1],y[nb_views:len(x)-nb_views-1],z[nb_views:len(x)-nb_views-1],label="Points",color='g')
        ax.scatter(x[len(x)-nb_views:len(x)-1],y[len(x)-nb_views:len(x)-1],z[len(x)-nb_views:len(x)-1],label="End Point")
    else:
        ax.scatter(x[0],y[0],z[0],label="Starting Point")
        ax.scatter(x[nb_views:len(x)-nb_views-1],y[nb_views:len(x)-nb_views-1],z[nb_views:len(x)-nb_views-1],label="Points",color='g')
        ax.scatter(x[len(x)-1],y[len(x)-1],z[len(x)-1],label="End Point")
    ax.set_xticks([-7,-5,-2.5,0,2.5,5,7])
    ax.set_yticks([-7,-5,-2.5,0,2.5,5,7])
    ax.set_zticks([-7,-5,-2.5,0,2.5,5,7])
    ax.set_xlim(-7,7)
    ax.set_ylim(-7,7)
    ax.set_zlim(-7,7)
    ax.legend()
    plt.show()
    #plt.savefig("mygraph.png")
    print("Job done !!!")
#--------------- Main ---------------#
    #------ Check Parameter ------#
if len(sys.argv) == 1:
    exit("The script is launched with one parameter : path to parameters.cfg.")
path_parameters = sys.argv[1]
    #------ Extract Param -------#
parameters = extract_parameters(path_parameters)
path_raw_img = parameters[0]
number_of_img = int(parameters[1])
path_dst = parameters[2]
path_param_Raytrix = parameters[3]
width = int(parameters[4])
height = int(parameters[5])
path_param_dir = parameters[6]
path_output_dir = parameters[7]
path_RLC = parameters[8]
path_viewpoint = parameters[9]
number_of_view = int(parameters[10])
colmap_path = parameters[11]
database_path = parameters[12]
project_path = parameters[13]
output_path = parameters[14]
 #--- Check file/folders ----#
check_essential_file(path_raw_img)
check_and_create(path_dst)
check_essential_file(path_param_Raytrix)
check_and_create(path_param_dir)
check_and_create(path_output_dir)
check_essential_file(path_RLC)
check_and_create(path_viewpoint)
check_essential_file(colmap_path)
if project_path != "None":
    check_essential_file(project_path)
check_and_create(output_path)
    #------ Light raw img -------#
light_raw_img(path_raw_img,int(number_of_img),path_dst)
    #----- Build param RLC ------#
build_param_RLC(path_param_Raytrix,path_param_dir,path_dst,path_output_dir,width,height)
    #---------- MRLC ------------#
MRLC(path_param_dir,path_dst,path_RLC)
    #------- Extract MV ---------#
extract_MV(path_viewpoint,path_output_dir,int(number_of_view))
    #---------- ColMap ----------#
colmap(colmap_path,path_viewpoint,database_path,project_path,output_path)
    #----- Build Trajectory -----#
build_trajectory(output_path,number_of_view)
#---------------- End ---------------#
