# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing PCA
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/Ruey_Habenula/Habenula/Short_Stimulus/Fish104_Block2_Blue&UV1c/'
filename_save_prefix_forPCA = 'Test1'
filename_save_prefix_for_textfile = 'Test1'

#Which files to do PCA on
files_to_do_PCA = [1,0,0] #Individual PCA, Each_exp PCA, All_exp PCA

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

#Redo pca - 1
redo_pca = 1

# Required pcs from what was received previously
required_pcs = 0

#PCA parameters for individual trial pca
pca_components_ind = 4 #Number of pca components to detect from files
num_pca_colors_ind = 100 #Number of colors on the pca maps
num_samples_ind = 10000 #number of random samples to select to do PCA reconstruction
thresh_pca_ind = 0.00001 #Threshold above which to plot the pca components
color_map_ind = 'polar' #Colormap for plotting principle components

#PCA parameters for each exp pca
pca_components_eachexp = 4 #Number of pca components to detect from files
num_pca_colors_eachexp = 150 #Number of colors on the pca maps
num_samples_eachexp = 10000 #number of random samples to select to do PCA reconstruction
thresh_pca_eachexp = 0.00001 #Threshold above which to plot the pca components
color_map_eachexp = 'polar' #Colormap for plotting principle components

#PCA parameters for all exp pca
pca_components_allexp = 4 #Number of pca components to detect from files
num_pca_colors_allexp = 150 #Number of colors on the pca maps
num_samples_allexp = 100000 #number of random samples to select to do PCA reconstruction
thresh_pca_allexp = 0.000001 #Threshold above which to plot the pca components
color_map_allexp= 'polar' #Colormap for plotting principle components


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
    with open(Exp_Folder+filename_save_prefix_forPCA+'_save_pca_variables') as f:
        pca_components_ind, num_pca_colors_ind, num_samples_ind, thresh_pca_ind, color_map_ind,\
        pca_components_eachexp, num_pca_colors_eachexp, num_samples_eachexp, thresh_pca_eachexp, color_map_eachexp,\
        pca_components_allexp, num_pca_colors_allexp, num_samples_allexp, thresh_pca_allexp, color_map_allexp,required_pcs  = pickle.load(f)


# Go into the main function that does pca for indiviudal trials
from pca_thunder_analysis import run_analysis_individualexps
from pca_thunder_analysis import run_analysis_eachexp
from pca_thunder_analysis import run_analysis_allexp

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderpca")

if files_to_do_PCA[0]== 1:
    run_analysis_individualexps(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components_ind, num_pca_colors_ind, num_samples_ind, thresh_pca_ind, color_map_ind,\
    tsc,redo_pca, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,required_pcs,time_baseline )
    
if files_to_do_PCA[1]== 1:
    run_analysis_eachexp(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components_eachexp, num_pca_colors_eachexp, num_samples_eachexp, thresh_pca_eachexp, color_map_eachexp,\
    tsc,redo_pca, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,required_pcs,time_baseline )

if files_to_do_PCA[2]== 1:
    run_analysis_allexp(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components_allexp, num_pca_colors_allexp, num_samples_allexp, thresh_pca_allexp, color_map_allexp,\
    tsc,redo_pca, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,required_pcs,time_baseline )
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix_forPCA+'_save_pca_variables', 'w') as f:
    pickle.dump([pca_components_ind, num_pca_colors_ind, num_samples_ind, thresh_pca_ind, color_map_ind,\
        pca_components_eachexp, num_pca_colors_eachexp, num_samples_eachexp, thresh_pca_eachexp, color_map_eachexp,\
        pca_components_allexp, num_pca_colors_allexp, num_samples_allexp, thresh_pca_allexp, color_map_allexp, required_pcs ], f)
