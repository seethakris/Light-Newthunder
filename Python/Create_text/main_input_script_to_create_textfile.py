# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 13:35:15 2015
@author: seetha

For Light Data Analysis
Take user input in this file and call other routines
"""

## Enter Main Folder containing stimulus folders to create text files

Exp_Folder ='/Users/seetha/Desktop/Ruey_Habenula/Habenula/Fish104-108/Combined_Data/'
filename_save_prefix = 'Test1'

#Rewrite text files. 1- Yes
rewrite_flag = 1

#Experiment parameters
img_size_x = 300 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 512
img_size_crop_y1 = 280 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_y2 = 10
img_size_crop_x1 = 0 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_x2 = 0

# Time period within which to do the analysis
time_start = 0
time_end = 622

#Stimulus on and off time and define onset and offset times of the light stimulus
stimulus_pulse = 4 ##Whether it is a long, medium or short light stimulus

if stimulus_pulse == 1:
    stimulus_on_time = [46,98,142,194]
    stimulus_off_time = [65,117,161,213]
    
elif stimulus_pulse == 2:
    stimulus_on_time = [46,127,209,291,373]
    stimulus_off_time = [106,188,270,352,433]
    
elif stimulus_pulse == 3:
    stimulus_on_time = [46,86,127,168, 209, 249, 291, 332, 373, 414, 455,496]
    stimulus_off_time = [65,106,147,188,229,269,310,352,393,434,475,516]
    
elif stimulus_pulse == 4:
    stimulus_on_time = [46,98,142,194,46+311,98+311,142+311,194+311]
    stimulus_off_time = [65,117,161,213,65+311,117+311,161+311,213+311]
    
## Median filter - threshold
median_filter_threshold = 1
######################################################################


######################################################################
########################## Run Scripts ###############################

# Go into the main function that takes thunder data and 
from main_file_for_textfiles_for_thunder import initial_function

initial_function(Exp_Folder, filename_save_prefix, img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, \
 time_start,time_end, median_filter_threshold, rewrite_flag, stimulus_on_time, stimulus_off_time)

import pickle

with open(Exp_Folder+filename_save_prefix+'_save_input_variables', 'w') as f:
    pickle.dump([img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stimulus_pulse, stimulus_on_time, stimulus_off_time], f)


