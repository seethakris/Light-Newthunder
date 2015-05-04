# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing ICA
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/Ruey_Habenula/Habenula/Short_Stimulus/Fish104_Block2_Blue&UV1c/'
filename_save_prefix_forICA = 'Test1'
filename_save_prefix_for_textfile = 'Test1'

#Which files to do ICA on
files_to_do_ICA = [1,0,0] #Individual ICA, Each_exp ICA, All_exp ICA

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

#Redo ICA - 1
redo_ICA = 1


colors_ica = ['aqua','gold','mediumpurple','hotpink','red']

#ICA parameters for individual trial ICA
ICA_components_ind = 5 #Number of ICA components to detect from files
PCA_components_ind = 5 #Number of PCA components to detect from files
num_ICA_colors_ind = 5 #Number of colors on the ICA maps
color_map_ind = 'indexed' #Colormap for plotting ica components


#ICA parameters for each exp ICA
ICA_components_eachexp = 4 #Number of ICA components to detect from files
PCA_components_eachexp = 5 #Number of PCA components to detect from files
num_ICA_colors_eachexp = 150 #Number of colors on the ICA maps
color_map_eachexp = 'indexed' #Colormap for plotting principle components


#ICA parameters for all exp ICA
ICA_components_allexp = 4 #Number of ICA components to detect from files
PCA_components_allexp = 5 #Number of PCA components to detect from files
num_ICA_colors_allexp = 150 #Number of colors on the ICA maps
color_map_allexp= 'indexed' #Colormap for plotting principle components



#Stimulus on and off time and define onset and offset times of the light stimulus
stimulus_pulse = 1 ##Whether it is a long, medium or short light stimulus
num_fish_used = 1

if stimulus_pulse == 1:
    stimulus_on_time = [46,98,142,194]
    stimulus_off_time = [65,117,161,213]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000']

    
elif stimulus_pulse == 2:
    stimulus_on_time = [46,127,209,291,373]
    stimulus_off_time = [106,188,270,352,433]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000']

    
elif stimulus_pulse == 3:
    stimulus_on_time = [46,86,127,168, 209, 249, 291, 332, 373, 414, 455,496]
    stimulus_off_time = [65,106,147,188,229,269,310,352,393,434,475,516]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000', '#A52A2A','#FFA500','#FF0000','#00FF00','#008000','#808000','#FFFF00']
    
elif stimulus_pulse == 4:
    stimulus_on_time = [46,98,142,194,46+311,98+311,142+311,194+311]
    stimulus_off_time = [65,117,161,213,65+311,117+311,161+311,213+311]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000']

## How long is the baseline?
time_baseline = 30
######################################################################
########################## Run Scripts ###############################

# Load imput parameters that were saved from creating text file. 
import pickle

with open(Exp_Folder+filename_save_prefix_for_textfile +'_save_input_variables') as f:
    img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stimulus_pulse, stimulus_on_time, stimulus_off_time = pickle.load(f)
    
    
if use_existing_parameters == 1:
    with open(Exp_Folder+filename_save_prefix_forICA+'_save_ICA_variables') as f:
        ICA_components_ind, num_ICA_colors_ind, color_map_ind,\
        ICA_components_eachexp, num_ICA_colors_eachexp, color_map_eachexp,\
        ICA_components_allexp, num_ICA_colors_allexp, color_map_allexp,colors_ica = pickle.load(f)


# Go into the main function that does ICA for indiviudal trials
from ica_thunder_analysis import run_analysis_individualexps
from ica_thunder_analysis import run_analysis_eachexp
from ica_thunder_analysis import run_analysis_allexp

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderICA")

if files_to_do_ICA[0]== 1:
    run_analysis_individualexps(Exp_Folder, filename_save_prefix_forICA, filename_save_prefix_for_textfile, ICA_components_ind, PCA_components_ind, num_ICA_colors_ind, color_map_ind,\
    tsc,redo_ICA, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat, time_baseline,colors_ica )
    
if files_to_do_ICA[1]== 1:
    run_analysis_eachexp(Exp_Folder, filename_save_prefix_forICA, filename_save_prefix_for_textfile, ICA_components_eachexp, PCA_components_eachexp, num_ICA_colors_eachexp, color_map_eachexp,\
    tsc,redo_ICA, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat, time_baseline,colors_ica )

if files_to_do_ICA[2]== 1:
    run_analysis_allexp(Exp_Folder, filename_save_prefix_forICA, filename_save_prefix_for_textfile, ICA_components_allexp, PCA_components_allexp, num_ICA_colors_allexp, color_map_allexp,\
    tsc,redo_ICA, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat, time_baseline,colors_ica )
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix_forICA+'_save_ICA_variables', 'w') as f:
    pickle.dump([ICA_components_ind, PCA_components_ind, num_ICA_colors_ind, color_map_ind,\
        ICA_components_eachexp, PCA_components_eachexp, num_ICA_colors_eachexp, color_map_eachexp,\
        ICA_components_allexp, PCA_components_allexp, num_ICA_colors_allexp, color_map_allexp, colors_ica], f)
