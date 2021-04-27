# Localisation and Tracking of a Plenoptic Camera
This git refers to a project for a Master Degree. You should find the report in this git (report.pdf).
## Requirements
  1. Python version 3.7.X or newest
  2. Some python libraries
    a. Numpy
    b. Matplotlib
    c. PyQtl 5.0
  3. RLC 0.3 or newest. Make sure that the configuration file needed for RLC does not change of format for newer versions.
  4. COLMAP 3.6 or newest
  5. Dataset. My datasets will be available for short period [from here](https://www.google.com).
## Configuration file for the project
The script needs a configuration file. In that file, you should specify all the directory and the parameters for RLC and COLMAP.
Please refer to the file config_example.cfg to know more about.
## Launch the script
After done the configuration file, you can launch the script with:
```
python $PATH_TO_DIR/project.py $PATH_TO_CONFIG/$NAME_CONFIG
```
