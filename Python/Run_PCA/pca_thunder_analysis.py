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

from thunder_pca import run_pca
from thunder_pca import make_pca_maps
from thunder_pca_plots import plot_pca_maps

from thunder import Colorize
image = Colorize.image

## PCA on individual exps
def run_analysis_individualexps(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components, num_pca_colors, num_samples, thresh_pca,\
color_map, tsc,redo_pca,stimulus_pulse,required_pcs,time_baseline):


    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj])+filesep        
                    
            name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        

            ## Check if textfile exists to do PCA            
            name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_for_textfile+'_individualtrial'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'.txt')==0)]    
            
            if len(txt_file)>0:
                #Load data        
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3)#.toTimeSeries().detrend(method='linear', order=8)
                data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                
#                data_plotting = copy(data_filtered)
#                plot_preprocess_data(Working_Directory, name_for_saving_files, data_plotting, stimulus_pulse,time_baseline)
                
                data_filtered.center()
#                data_filtered.zscore(time_baseline)
                data_filtered.cache()
                
                flag = 0
                name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_forPCA+'_individualtrial'
                run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data_filtered,\
                data_background,pca_components, num_pca_colors, num_samples, thresh_pca, color_map,  flag,stimulus_pulse,required_pcs)
                
    
def run_analysis_eachexp(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components, num_pca_colors, num_samples, thresh_pca, color_map,\
tsc,redo_pca,stimulus_pulse,required_pcs,time_baseline):
    
    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]            
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
        
        name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix_for_textfile+'_eachexp'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]                    
        name_for_saving_figures = Stimulus_Directories[ii]       

        if len(txt_file)>0:
           #Load data                    
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=8)
            data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
            
            
            data_filtered.center()
#            data_filtered.zscore(time_baseline)
            data_filtered.cache()
                
            flag = 1
            name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix_forPCA+'_eachexp'
            run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data_filtered,\
            data_background, pca_components, num_pca_colors, num_samples, thresh_pca, color_map, flag,stimulus_pulse,required_pcs)
            
    
def run_analysis_allexp(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components, num_pca_colors, num_samples, thresh_pca, color_map,\
 tsc,redo_pca,stimulus_pulse,required_pcs,time_baseline):
    
    Working_Directory = Exp_Folder
        
    name_for_saving_files = 'All_exps_'+ filename_save_prefix_for_textfile+'_eachexp'
    txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
    
    if len(txt_file)>0:
       #Load data                    
        data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=8)
        data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                
        data_filtered.center()
#        data_filtered.zscore(time_baseline)
        data_filtered.cache()
            
        name_for_saving_figures = Working_Directory
        flag = 2
        name_for_saving_files = 'All_exps_'+ filename_save_prefix_forPCA +'_eachexp'
        run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data_filtered,\
        data_background, pca_components, num_pca_colors, num_samples, thresh_pca, color_map, flag,stimulus_pulse,required_pcs)

    
def run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data,data_background,\
pca_components, num_pca_colors, num_samples, thresh_pca, color_map,  flag,stimulus_pulse, required_pcs):
    
    
    ### If pca result files exists, then dont run any more pca, just do plotting, 
    ## Else run pca and save all outputs
    pickle_dump_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'_pca_results')==0)]    
    
    if len(pickle_dump_file)==0 or redo_pca==1:
        #Run PCA
        start_time = time.time()
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Running pca in %s \n" % Working_Directory)
        print 'Running pca for all files...in '+ Working_Directory
        pca, imgs_pca, new_imgs = run_pca(data,pca_components,required_pcs)
        print 'Running PCA took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Running pca took %s seconds \n" %  str(int(time.time()-start_time)))
        
        
        #Create PCA maps
        start_time = time.time()
        text_file.write("Making pca color maps in %s \n" % Working_Directory)
        print 'Making pca color maps for all files...in '+ Working_Directory
        img_size_x = np.size(new_imgs,1)
        img_size_y = np.size(new_imgs,2)
        maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = make_pca_maps(data_background,pca, new_imgs, required_pcs, img_size_x,\
        img_size_y, num_pca_colors, num_samples, thresh_pca, color_map)
        print 'Making pca color maps '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Making pca color maps took %s seconds \n" %  str(int(time.time()-start_time)))
       
        print 'Matched_Pixels........' + str(np.shape(matched_pixels))
        pca_components = pca.comps.T
        ## save input parameters
        ############# Save all imput parameters
        with open(Working_Directory+name_for_saving_files+'_pca_results', 'w') as f:
            pickle.dump([pca_components, imgs_pca,new_imgs, maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal],f)
    
    else:        
        print 'Using existing pickled parameters....'
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Plotting Using existing pickled parameters....\n")
        with open(Working_Directory+name_for_saving_files+'_pca_results') as f:
            pca_components, imgs_pca, new_imgs, maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = pickle.load(f)
    
    
# Plot PCA
    start_time = time.time()
    text_file.write("Plotting pca in %s \n" % Working_Directory)
    print 'Plotting pca in for all files...in '+ Working_Directory
    plot_pca_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    pca_components, maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals,  flag,stimulus_pulse,required_pcs, data_background)
    print 'Plotting pca in '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Plotting pca in took %s seconds \n" %  str(int(time.time()-start_time)))
    


def plot_preprocess_data(Working_Directory, name_for_saving_files, data, stimulus_pulse,time_baseline):
    
    #### Plot subset of data to view ######## 
    
        # To save as pdf create file
    start_time = time.time()
    print 'Plotting centered data...in '+ Working_Directory
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Plotting centered data in %s \n" % Working_Directory)
    
    #Save some data wide statistics to text file
    
    print 'Data Statistics :'
    print 'Series Mean :' + str(data.seriesMean().first())
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Series Mean : %s \n" % str(data.seriesMean().first()))
    
    print 'Series Std :' + str(data.seriesStdev().first())
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Series Std : %s \n" % str(data.seriesStdev().first()))

    from numpy import random
    signal = random.randn(data.index.shape[0])
    print 'Series Corrrelation :' + str(data.correlate(signal).first())
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Series Corrrelation : %s \n" % str(data.correlate(signal).first()))

        
    ## Plot some data related figures
    Figure_PDFDirectory = Working_Directory+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory)           
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'_PreprocessedData.pdf')
    

    with sns.axes_style("darkgrid"):    
        fig2 = plt.figure()
        examples = data.center().subset(nsamples=100, thresh=1)
        if np.size(examples)!=0:        
            plt.plot(examples.T[:,:]);
            plot_vertical_lines(stimulus_pulse)
            plt.tight_layout()
            fig2 = plt.gcf()
            pp.savefig(fig2)
            plt.close()
        
    with sns.axes_style("darkgrid"):  
        fig3 = plt.figure()
        
        examples = data.zscore(time_baseline).subset(nsamples=100, thresh=2)
        if np.size(examples)!=0:
            plt.plot(examples.T[:,:]);
            plot_vertical_lines(stimulus_pulse)
            plt.tight_layout()
            fig2 = plt.gcf()
            pp.savefig(fig3)
            plt.close()
            
        fig4 = plt.figure()
        plt.plot(data.center().max());
        plt.plot(data.center().mean());
        plt.plot(data.center().min());
        plot_vertical_lines(stimulus_pulse)
        plt.tight_layout()
        fig2 = plt.gcf()
        pp.savefig(fig4)
        
        
        plt.close()
        pp.close()
        
        print 'Plotting centered data took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Plotting centered data took %s seconds \n" %  str(int(time.time()-start_time)))

def plot_vertical_lines(stimulus_pulse):
  
    if stimulus_pulse == 1:
        
        plt.axvline(x=46, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=65, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=98, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=117, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=142, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=161, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=194, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=213, linestyle='--', color='k', linewidth=1)
    
    elif stimulus_pulse == 2:
        
        plt.axvline(x=46, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=106, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=127, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=188, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=209, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=270, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=291, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=352, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=373, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=433, linestyle='--', color='k', linewidth=1)
                      
    elif stimulus_pulse==3:
        
        plt.axvline(x=46, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=65, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=86, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=106, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=127, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=147, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=168, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=188, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=209, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=229, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=249, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=269, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=291, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=310, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=332, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=352, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=373, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=393, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=414, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=434, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=455, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=475, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=496, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=516, linestyle='--', color='k', linewidth=1)
        
    
        
    
    
        
        

