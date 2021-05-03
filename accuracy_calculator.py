# --------- Library ---------#
import sys, os
import numpy as np
import matplotlib.pyplot as plt
# -------- Function ---------#
def clean_line(line):
    args_line = line.split()
    quad = np.array([args_line[1],args_line[2],args_line[3],args_line[4]],dtype="float32")
    trans = np.array([[args_line[5]],[args_line[6]],[args_line[7]],[1]],dtype="float32")
    nb_img = args_line[9].split("image_")[1].split(".png")[0]
    return trans, int(nb_img)

def build_array(path_to_coord,nb_views):
    file = None
    try:
        file = open(path_to_coord+"0/images.txt","rt")
    except:
        exit("Error occured : do not suceed to open the file from ColMap.")
    #Skip commentaries
    for i in range(3):
        file.readline()
    number_of_img = file.readline().split(",")[0].split(" ")
    number_of_img = int(number_of_img[len(number_of_img)-1])
    if nb_views == 0:
        nb_views = 1
    elif nb_views == 1:
        nb_views = 2
    elif nb_views == 3 or nb_views == 2:
        nb_views = 4
    else:
        nb_views = 8
    x,y,z = np.array([np.zeros(number_of_img//nb_views)]*nb_views),np.array([np.zeros(number_of_img//nb_views)]*nb_views),np.array([np.zeros(number_of_img//nb_views)]*nb_views)
    #Loop and skip one line after reading one
    line_read = False
    for line in file:
        if not line_read:
            trans, indx = clean_line(line)
            index = indx%nb_views
            idx = indx//nb_views
            x_new, y_new, z_new = trans[2],trans[0],trans[1]
            x[index][idx] = x_new
            y[index][idx] = y_new
            z[index][idx] = z_new
        line_read =  not line_read
    file.close()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title("3D Trajectory of the cameras")
    ax.plot(x[0],y[0],z[0],label="Lines")
    ax.scatter(x[0],y[0],z[0],label="Points")
    ax.set_xticks([-7,-5,-2.5,0,2.5,5,7])
    ax.set_yticks([-7,-5,-2.5,0,2.5,5,7])
    ax.set_zticks([-7,-5,-2.5,0,2.5,5,7])
    ax.set_xlim(-7,7)
    ax.set_ylim(-7,7)
    ax.set_zlim(-7,7)
    ax.legend()
    plt.show()
    return x,y,z

def read_sys():
    if len(sys.argv) != 6:
        exit("Need 5 arguments, path to the 5 results.")
    arrays = [0]*5
    for i in range(1,6):
        if os.path.isdir(sys.argv[i]):
            arrays[i-1]=build_array(sys.argv[i],i-1)
        else:
            exit("Not a directory." + sys.argv[i])
    return arrays

def calculate_slope(arrays):
    idx_array = 0
    sigma = [0]*len(arrays)
    for m in arrays:
        x,y = m[1], m[0]
        ecart_type = 0
        plt.figure()
        for views in range(len(x)):
            # Figure
            plt.plot(x[views],y[views])

            slope_view = 0
            for cam in range(0,len(x[0])-1):
                slope_view += abs((y[views][cam+1]-y[views][cam])/(x[views][cam+1]-x[views][cam]))
            slope_mean = slope_view/len(x[0])
            for cam in range(0,len(x[0])-1):
                ecart_type += (abs(abs(slope_mean - (y[views][cam+1]-y[views][cam])/(x[views][cam+1]-x[views][cam]))))**2
            ecart_type = (ecart_type/len(x[0]))**0.5
        sigma[idx_array] = ecart_type/len(x)
        # figure
        plt.title("Config" +str(idx_array) +": Line trajectory seen by the different views\n Average standard deviation = "+str(sigma[idx_array]))
        plt.show()

        idx_array += 1
    return sigma
# ---------- Main -----------#
arrays = read_sys()
#print(arrays)
slope = calculate_slope(arrays)
print(slope)
file = open("./data/save_slope.txt","w+")
for a in slope:
    file.write(str(a)+"\n")
