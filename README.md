# Localisation and Tracking of a Plenoptic Camera
This git refers to a project for a Master Degree. You should find the report in this git (report.pdf).
## Requirements
  1. Python version 3.7.X or newest
  2. Some python libraries
      * Numpy
      * Matplotlib
      * PyQtl 5.0
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
  <img align="left" src="https://user-images.githubusercontent.com/33875555/117044140-632d6980-ad0e-11eb-93d1-c1747f4af02f.png">
  
  2. Rectangle
  <img align="left" src="https://user-images.githubusercontent.com/33875555/117044178-6d4f6800-ad0e-11eb-8b50-2a55078edb3a.png">
  
  3. V
  <img align="left" src="https://user-images.githubusercontent.com/33875555/117044158-67f21d80-ad0e-11eb-8151-35f2c32cdc94.png">
