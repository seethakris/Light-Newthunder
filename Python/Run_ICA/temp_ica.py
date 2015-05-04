Exp_Folder ='/Users/seetha/Desktop/Ruey_Habenula/Habenula/Short_Stimulus/Fish104_Block2_Blue&UV1c/'
filename_save_prefix = 'Test1'


from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderICA")
import os
filesep = os.path.sep

import matplotlib.pyplot as plt 

import numpy as np
from thunder_ica import run_ICA
from thunder_ica import make_ICA_maps
from thunder_ica_plots import plot_ICA_maps

from thunder import Colorize
image = Colorize.image

Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
#Stimulus_Directories
ii = 0
Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0]
Trial_Directories
jj = 0

stim_start = 10 #Stimulus Starting time point
stim_end = 14 #Stimulus Ending time point

flag = 0

name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        
Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj])+filesep       
name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
#Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
#name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
#name_for_saving_figures = Stimulus_Directories[ii]       

#Working_Directory = Exp_Folder
#name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
#name_for_saving_figures = Working_Directory

data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=10)
data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
data_background.cache()
#plot_preprocess_data(Working_Directory, name_for_saving_files, data_filtered, stim_start, stim_end)
                
data_filtered.center()
#data_filtered.zscore(10)
data_filtered.cache()

ICA, imgs_ICA = run_ICA(data_filtered,5,5)
ICA_components = ICA.a
colors_ica = ['aqua','gold','mediumpurple','hotpink','red']

for ii in range(np.size(ICA_components,1)):
    plt.plot(ICA_components[:,ii])##

img_size_x = np.size(imgs_ICA,1)
img_size_y = np.size(imgs_ICA,2)
#
maps,matched_pixels,unique_clrs = make_ICA_maps(data_background,ICA, imgs_ICA, img_size_x, img_size_y, 5, 'indexed', colors_ica)
stimulus_on_time = [46,98,142,194]
stimulus_off_time = [65,117,161,213]
plot_ICA_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    ICA_components, maps, colors_ica, matched_pixels, stimulus_on_time, stimulus_off_time, flag, unique_clrs)