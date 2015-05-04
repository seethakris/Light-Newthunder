# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:00:39 2015
Main function to load data and start thunder analysis
@author: chad
"""
import os
filesep = os.path.sep
from copy import copy
import time
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pickle

from thunder_ica import run_ICA
from thunder_ica import make_ICA_maps
from thunder_ica_plots import plot_ICA_maps

from thunder import Colorize
image = Colorize.image

## ICA on individual exps
def run_analysis_individualexps(Exp_Folder, filename_save_prefix_forICA, filename_save_prefix_for_textfile, ICA_components, PCA_components, num_ICA_colors, \
color_map, tsc,redo_ICA, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,time_baseline,colors_ica):


    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj])+filesep        
                    
            name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        

            ## Check if textfile exists to do ICA            
            name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_for_textfile+'_individualtrial'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'.txt')==0)]    
            
            if len(txt_file)>0:
                #Load data        
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
                data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                                
                data_filtered.center()
#                data_filtered.zscore(time_baseline)
                data_filtered.cache()
                
                flag = 0
                name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_forICA+'_individualtrial'
                run_ICA_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ICA, data_filtered,\
                data_background,ICA_components, PCA_components, num_ICA_colors, color_map,  flag,num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat, colors_ica)
                
    
def run_analysis_eachexp(Exp_Folder, filename_save_prefix_forICA, filename_save_prefix_for_textfile, ICA_components, PCA_components, num_ICA_colors, color_map,\
tsc,redo_ICA,num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,time_baseline,colors_ica):
    
    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]            
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
        
        name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix_for_textfile+'_eachexp'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]                    
        name_for_saving_figures = Stimulus_Directories[ii]       

        if len(txt_file)>0:
           #Load data                    
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
            data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
            
            
            data_filtered.center()
#            data_filtered.zscore(time_baseline)
            data_filtered.cache()
                
            flag = 1
            name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix_forICA+'_eachexp'
            run_ICA_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ICA, data_filtered,\
            data_background, ICA_components, PCA_components, num_ICA_colors, color_map, flag,num_fish_used, stimulus_pulse,\
            stimulus_on_time, stimulus_off_time,color_mat,colors_ica)
            
    
def run_analysis_allexp(Exp_Folder, filename_save_prefix_forICA, filename_save_prefix_for_textfile, ICA_components, PCA_components, num_ICA_colors, color_map,\
 tsc,redo_ICA, num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat, time_baseline, colors_ica):
    
    Working_Directory = Exp_Folder
        
    name_for_saving_files = 'All_exps_'+ filename_save_prefix_for_textfile+'_eachexp'
    txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
    
    if len(txt_file)>0:
       #Load data                    
        data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
        data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                
        data_filtered.center()
#        data_filtered.zscore(time_baseline)
        data_filtered.cache()
            
        name_for_saving_figures = Working_Directory
        flag = 2
        name_for_saving_files = 'All_exps_'+ filename_save_prefix_forICA +'_eachexp'
        run_ICA_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ICA, data_filtered,\
        data_background, ICA_components, PCA_components, num_ICA_colors, color_map, flag,num_fish_used, stimulus_pulse,\
        stimulus_on_time, stimulus_off_time,color_mat,colors_ica)

    
def run_ICA_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ICA, data,data_background,\
ICA_components, PCA_components, num_ICA_colors, color_map,  flag,num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,colors_ica):
    
    
    ### If ICA result files exists, then dont run any more ICA, just do plotting, 
    ## Else run ICA and save all outputs
    pickle_dump_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'_ICA_results')==0)]    
    
    if len(pickle_dump_file)==0 or redo_ICA==1:
        #Run ICA
        start_time = time.time()
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Running ICA in %s \n" % Working_Directory)
        print 'Running ICA for all files...in '+ Working_Directory
        ICA, imgs_ICA = run_ICA(data,ICA_components,PCA_components)
        print 'Running ICA took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Running ICA took %s seconds \n" %  str(int(time.time()-start_time)))
        
        
        #Create ICA maps
        start_time = time.time()
        text_file.write("Making ICA color maps in %s \n" % Working_Directory)
        print 'Making ICA color maps for all files...in '+ Working_Directory
        img_size_x = np.size(imgs_ICA,1)
        img_size_y = np.size(imgs_ICA,2)
        
        maps, matched_pixels, unique_clrs = make_ICA_maps(data_background,ICA, imgs_ICA, img_size_x,\
        img_size_y, num_ICA_colors, color_map, colors_ica)

        print 'Making ICA color maps '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Making ICA color maps took %s seconds \n" %  str(int(time.time()-start_time)))
       
        print 'Matched_Pixels........' + str(np.shape(matched_pixels))
        ICA_components = ICA.a
        
        ## save input parameters
        ############# Save all imput parameters
        with open(Working_Directory+name_for_saving_files+'_ICA_results', 'w') as f:
            pickle.dump([ICA_components, imgs_ICA, maps, matched_pixels,unique_clrs],f)
    
    else:        
        print 'Using existing pickled parameters....'
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Plotting Using existing pickled parameters....\n")
        with open(Working_Directory+name_for_saving_files+'_ICA_results') as f:
            ICA_components, imgs_ICA,  maps, matched_pixels, unique_clrs = pickle.load(f)
    
    
# Plot ICA
    start_time = time.time()
    text_file.write("Plotting ICA in %s \n" % Working_Directory)
    print 'Plotting ICA in for all files...in '+ Working_Directory
   
    plot_ICA_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    ICA_components, maps, colors_ica, matched_pixels, stimulus_on_time, stimulus_off_time, flag, unique_clrs)
    
    print 'Plotting ICA in '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Plotting ICA in took %s seconds \n" %  str(int(time.time()-start_time)))
    
