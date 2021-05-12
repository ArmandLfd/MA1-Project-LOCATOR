# Localisation and Tracking of a Plenoptic Camera
This git refers to a project for a Master Degree. You should find the report in this git (report.pdf).
## Requirements
  1. Python version 3.7.X or newest
  2. Some python libraries
      * Numpy
      * Matplotlib
      * PyQt 5.0
  3. RLC 0.3 or newest. Make sure that the configuration file needed for RLC does not change of format for newer versions.
  4. COLMAP 3.6 or newest
  5. Dataset. My datasets will be available for short period [from here](https://universitelibrebruxelles-my.sharepoint.com/:f:/g/personal/armand_losfeld_ulb_be/EmN2edlo_F9Ggkt30lonaTIBIk5vfgKL2b4EijMppNxzHA?e=P5fbd8). You should be a member of the *Free University of Brussels* to have the access.
## Configuration file for the project
The script needs a configuration file. In that file, you should specify all the directory and the parameters for RLC and COLMAP.
Please refer to the file config_example.cfg to know more about.
## Launch the script
After done the configuration file, you can launch the script with:
```
python $PATH_TO_DIR/project.py $PATH_TO_CONFIG/$NAME_CONFIG
```
## Results
Results of the three data sets.
  1. Line
  <img align="center" src="https://user-images.githubusercontent.com/33875555/117998128-e3be1c80-b343-11eb-8423-a90a8e9c30db.png">
  
  2. Rectangle
  <img align="center" src="https://user-images.githubusercontent.com/33875555/117998185-f0db0b80-b343-11eb-9c72-3da639c9a3f9.png">
  
  3. V
  <img align="center" src="https://user-images.githubusercontent.com/33875555/117998233-fa647380-b343-11eb-8cb9-3912f18837b0.png">
