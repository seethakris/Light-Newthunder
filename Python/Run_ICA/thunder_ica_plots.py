# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 08:50:59 2014
Plot ICA components and maps for OB data 
@author: seetha
"""

#Import python libraries
import os
filesep = os.path.sep

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns #For creating nice plots
from mpl_toolkits.mplot3d import axes3d

from libtiff import TIFF

from thunder import Colorize
image = Colorize.image

z_direction = 'z'

def plot_ICA_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    ICA_components, maps, colors_ica, matched_pixels, stimulus_on_time, stimulus_off_time, flag, unique_clrs):
    

    # To save as pdf create file
    Figure_PDFDirectory = Working_Directory+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory)           
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'_ICA.pdf')
               
    sns.set_context("poster")  
    
    ########### Plot components ##################
    fig2 = plt.figure()
    sns.set_context("talk", font_scale=1.25)
    with sns.axes_style("darkgrid"):
        ax1 = plt.subplot(221)
        plot_ICA_components(ICA_components,ax1,stimulus_on_time, stimulus_off_time, colors_ica)
    
    #Plot mean projection   
    with sns.axes_style("white"):  
        fig2 = plt.subplot(223)        
        if len(maps.shape)==3:
            plt.imshow(maps)
        else:
            image(np.amax(maps,2))
            
        plt.axis('off')
        plt.title('Max projection')
    
    
    ########### Plot Boxplot of number of pixels ##################        
    with sns.axes_style("white"):
        fig2 = plt.subplot(222)
        fig2 = plot_boxplot(fig2, matched_pixels, colors_ica)
    
    plt.tight_layout()
    fig2 = plt.gcf()
    pp.savefig(fig2)
    plt.close()
    
    ################  Plot color maps individually #######################
    if flag == 0:
        plot_colormaps_ind(maps, Working_Directory, name_for_saving_figures, pp)
    elif flag == 1:
        plot_colormaps_each(maps, Working_Directory, name_for_saving_figures, pp,matched_pixels,colors_ica)
    elif flag == 2:
        plot_colormaps_all( maps, Working_Directory, pp, matched_pixels, colors_ica)
        plot_colormaps_all_z_plane_wise(maps, Working_Directory, pp,matched_pixels, colors_ica)
    

    pp.close()
                
def plot_colormaps_ind(maps, Working_Directory, name_for_saving_figures, pp):
###########  Plot color maps individually #######################
    if len(np.shape(maps)) == 3:
        #Plot colored maps for each stack
        with sns.axes_style("white"):
            fig1 = plt.figure()           
            plt.imshow(maps[:,:,:])
            plt.title(name_for_saving_figures + ' Z=1')
            plt.axis('off')                 
            fig1 = plt.gcf()
            pp.savefig(fig1)
            plt.close()
            
            
    else:
        with sns.axes_style("white"):
            for ii in range(0, np.size(maps,2)):
                fig1 = plt.imshow(maps[:,:,ii,:])
                plt.title(name_for_saving_figures + ' Z='+str(ii+1))
                plt.axis('off')
                fig1 = plt.gcf()
                pp.savefig(fig1)
                plt.close()

    
def plot_colormaps_each(maps, Working_Directory, name_for_saving_figures, pp, matched_pixels, unique_clrs):
    
    Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory)) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0] #Get only directories
    
    ## To find num z planes in each trial directory
    num_z_planes = np.zeros((np.size(Trial_Directories)), dtype=np.int)
    for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
        Image_Directory = os.path.join(Working_Directory, Trial_Directories[jj])+filesep    
        tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
        count = 1        
        for image in tif.iter_images():
            num_z_planes[jj] = count
            count = count+1
    
    count = 0     
    count_trial1 = 0
    for ii in xrange(0, np.size(Trial_Directories, axis = 0)):       
        count_subplot = 1
        for jj in xrange(0, num_z_planes[ii]):
            name_for_saving_figures1 = name_for_saving_figures + ' ' + Trial_Directories[ii] + ' Z=' + str(jj+1)
            with sns.axes_style("darkgrid"):           
                fig2 = plt.subplot(2,2,count_subplot)
                plt.imshow(maps[:,:,count,:])
                plt.title(name_for_saving_figures1)
                plt.axis('off')
            count = count+1
            count_subplot = count_subplot + 1
            
            # If there are more than 6 panel, save and start new figure
            if count_subplot == 5:
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
                count_subplot = 1
                    
        #Plot boxplots for each trial
        if count_subplot <= 4:
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,2,count_subplot)
                fig2 = plot_boxplot(fig2, matched_pixels[:,count_trial1:count_trial1+num_z_planes[ii]], unique_clrs)
#                plt.tight_layout()            
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
            count_trial1 = count_trial1 + num_z_planes[ii]
            
        else:
            with sns.axes_style("darkgrid"):
                fig3 = plt.figure()
                fig3 = plot_boxplot(fig3, matched_pixels[:,count_trial1:count_trial1+num_z_planes[ii]], unique_clrs)
#                plt.tight_layout()            
                fig3 = plt.gcf()
                pp.savefig(fig3)
                plt.close()
            count_trial1 = count_trial1 + num_z_planes[ii]

        

    
def  plot_colormaps_all(maps, Working_Directory, pp, matched_pixels, unique_clrs):
    
    Stimulus_Directories = [f for f in os.listdir(Working_Directory) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0]
    
    ## To find num z planes in each trial directory
    num_z_planes = []
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        temp_num_z_planes = np.zeros((np.size(Trial_Directories)), dtype=np.int)    
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Image_Directory = os.path.join(Working_Directory, Stimulus_Directories[ii], Trial_Directories[jj])+filesep    
            tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
            count = 1        
            for image in tif.iter_images():
                temp_num_z_planes[jj] = count
                count = count+1
        
        num_z_planes.append(temp_num_z_planes)
                
    ### Plot maps - each stimulus in one page            
    count = 0
    count_exp1 = 0
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        count_subplot = 1
        
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            for kk in xrange(0, num_z_planes[ii][jj]):
                name_for_saving_figures1 = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj] + ' Z=' + str(kk+1)                
                with sns.axes_style("darkgrid"):
                    fig2 = plt.subplot(2,2,count_subplot)
                    plt.imshow(maps[:,:,count,:])
                    plt.title(name_for_saving_figures1)
                    plt.axis('off')
                    
                count = count+1
                count_subplot = count_subplot+1
                

                # If there are more than 6 panel, save and start new figure
                if count_subplot == 5:
                    fig2 = plt.gcf()
                    pp.savefig(fig2)
                    plt.close()
                    count_subplot = 1
                    
        #Plot boxplots for each exp        
        if count_subplot <= 4:
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,2,count_subplot)
                fig2 = plot_boxplot(fig2, matched_pixels[:,count_exp1:count_exp1+\
                np.sum(num_z_planes[ii])], unique_clrs)
                plt.tight_layout()            
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
            count_exp1 = count_exp1+np.sum(num_z_planes[ii])
            
        else:
            with sns.axes_style("darkgrid"):
                fig3 = plt.figure()
                fig2 = plot_boxplot(fig3, matched_pixels[:,count_exp1:count_exp1+\
                num_z_planes[ii][jj]], unique_clrs)
                plt.tight_layout()            
                fig3 = plt.gcf()
                pp.savefig(fig3)
                plt.close()
            count_exp1 = count_exp1+np.sum(num_z_planes[ii])



## Plot maps - each plane in one slide                  
def plot_colormaps_all_z_plane_wise(maps, Working_Directory, pp, matched_pixels, unique_clrs):
    
    
    Stimulus_Directories = [f for f in os.listdir(Working_Directory) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0]
    
    ## To find num z planes in each trial directory
    num_z_planes = []
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        temp_num_z_planes = np.zeros((np.size(Trial_Directories)), dtype=np.int)    
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Image_Directory = os.path.join(Working_Directory, Stimulus_Directories[ii], Trial_Directories[jj])+filesep    
            tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
            count = 1        
            for image in tif.iter_images():
                temp_num_z_planes[jj] = count
                count = count+1       
        num_z_planes.append(temp_num_z_planes)
        
        
    
    ## First rearrange maps according to planes instead of stimulus
    ## 1. Name the figures in maps one by one and then select those that are of a particular z
    name_for_saving_figures1 = []
    count = 0
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):        
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories                
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            for kk in xrange(0, num_z_planes[ii][jj]):
                name_for_saving_figures1.append(Stimulus_Directories[ii] + ' ' + Trial_Directories[jj] + ' Z=' + str(kk+1))        
                
    ### Plot maps - each z-plane one page          
    ## FInd maximum z planes
    Max_z = max(max(num_z_planes, key=lambda x:np.max(x)))
    for ii in xrange(1, Max_z+1):
        Matching_file_index = [name_for_saving_figures1.index(s) for s in name_for_saving_figures1 if "Z="+str(ii) in s]
        Matching_file_names = [s for s in name_for_saving_figures1 if "Z="+str(ii) in s]        
        temp_maps = maps[:,:,Matching_file_index,:]    
        temp_matched_pixels = matched_pixels[:,Matching_file_index]
        count_subplot=1        
        for jj in xrange(0,np.size(temp_maps,2)):
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,3,count_subplot)
                plt.imshow(temp_maps[:,:,jj,:])
                plt.title(Matching_file_names[jj],fontsize=11)
                plt.axis('off')
            
            count_subplot = count_subplot+1
    
            if count_subplot == 7:
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
                count_subplot = 1
                
        #Plot boxplots for each exp        
        if count_subplot <= 6:
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,3,count_subplot)
                fig2 = plot_boxplot(fig2, temp_matched_pixels, unique_clrs)
                plt.tight_layout()            
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
            
        else:
            with sns.axes_style("darkgrid"):
                fig3 = plt.figure()
                fig2 = plot_boxplot(fig3, temp_matched_pixels, unique_clrs)
                plt.tight_layout()            
                fig3 = plt.gcf()
                pp.savefig(fig3)
                plt.close()
        
        
    
def plot_ICA_components(ICA_components,ax1,stimulus_on_time, stimulus_off_time, colors_ica):
########### Plot components ##################    
    for ii in range(np.size(ICA_components,1)):
        plt.plot(ICA_components[:,ii], color=colors_ica[ii])
    
    plt.locator_params(axis = 'y', nbins = 4)
    sns.axlabel("Time (seconds)","a.u")
    
    A = []
    for ii in xrange(0,np.size(ICA_components, 1)):
        A = np.append(A, [str(ii)])
        
    ax1.legend(A, loc=4)
    plt.axhline(y=0, linestyle='-', color='k', linewidth=1)
    plot_vertical_lines_onset(stimulus_on_time)
    plot_vertical_lines_offset(stimulus_off_time)
        
def plot_ICA_components_in3d(ICA_components,ax1,num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat,required_pcs,z_direction):
    
    ########### Plot components in 3D ##################    
    if stimulus_pulse>3:
        plot_stimulus_in_3d_combined_fish(ax1, ICA_components, num_fish_used, stimulus_on_time, stimulus_off_time,color_mat,required_pcs,z_direction)
    else:
        plot_stimulus_in_3d(ax1, ICA_components, stimulus_on_time, stimulus_off_time,color_mat,required_pcs,z_direction)
    ## plot axis labels according to zdirection
    plot_axis_labels_byzdir(ax1,z_direction,required_pcs)
    

    
def plot_ICA_components_in2d(ICA_components,ax1,num_fish_used, stimulus_pulse, stimulus_on_time, stimulus_off_time,color_mat, required_pcs):
    ########### Plot components in 3D ##################  
    if stimulus_pulse>3:
        plot_stimulus_in_2d_combined_fish(ax1, ICA_components, num_fish_used, stimulus_on_time, stimulus_off_time, color_mat,required_pcs)
    else:
        plot_stimulus_in_2d(ax1, ICA_components, stimulus_on_time, stimulus_off_time,color_mat,required_pcs)
    
    legend_for_2d_plot(ax1, stimulus_off_time)
        
    ax1.set_xlabel('PC'+str(required_pcs[0]))
    ax1.set_ylabel('PC'+str(required_pcs[1]))
        
    
    
def plot_boxplot(fig2, matched_pixels, unique_clrs):
#### Plot Boxplot of number of pixels
    ## Dont plot boxplot if there is only one Z
    if np.size(matched_pixels,1) == 1:
        with sns.axes_style("darkgrid"):
            for ii in xrange(0,np.size(matched_pixels,0)):
                fig2 = plt.plot(ii+1,np.transpose(matched_pixels[ii,:]),'o', color=unique_clrs[ii])
                plt.xlim([0,np.size(matched_pixels,0)+1])
    else:
        fig2 = sns.boxplot(np.transpose(matched_pixels),linewidth=3, widths=.5, color=unique_clrs)
        
    for ii in range(0,np.size(unique_clrs,0)):
        fig2 = plt.plot(np.repeat(ii+1,np.size(matched_pixels,1)), np.transpose(matched_pixels[ii,:]),'s', \
        color=unique_clrs[ii], markersize=5, markeredgecolor='k', markeredgewidth=2) 
    
    plt.locator_params(axis = 'y', nbins = 2)
    sns.axlabel("Colors", "Number of Pixels")
    sns.despine(offset=10, trim=True)
    return fig2
    
    
def plot_axis_labels_byzdir(ax1,z_direction,required_pcs):
    
    if z_direction == 'y':
        ax1.set_xlabel('PC'+str(required_pcs[0]), linespacing=10, labelpad = 50)
        ax1.set_ylabel('PC'+str(required_pcs[2]), linespacing=10, labelpad = 50)
        
        ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
        ax1.set_zlabel('PC'+str(required_pcs[1]), rotation=90, linespacing=10, labelpad = 10)

    elif z_direction == 'z':
        ax1.set_xlabel('PC'+str(required_pcs[0]), linespacing=10, labelpad = 50)
        ax1.set_ylabel('PC'+str(required_pcs[1]), linespacing=10, labelpad = 50)
        
        ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
        ax1.set_zlabel('PC'+str(required_pcs[2]), rotation=90, linespacing=10, labelpad = 10)
    
    elif z_direction == 'x':
        ax1.set_xlabel('PC'+str(required_pcs[1]), linespacing=10, labelpad = 50)
        ax1.set_ylabel('PC'+str(required_pcs[2]), linespacing=10, labelpad = 50)
        
        ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
        ax1.set_zlabel('PC'+str(required_pcs[0]), rotation=90, linespacing=10, labelpad = 10)
    
    ax1.locator_params(axis = 'x',  pad=50)
    ax1.locator_params(axis = 'y', pad=50)
    ax1.locator_params(axis = 'z',  pad=50)
         

def plot_vertical_lines_onset(stimulus_on_time):
    for ii in xrange(0,np.size(stimulus_on_time)):
        plt.axvline(x=stimulus_on_time[ii], linestyle='-', color='k', linewidth=1)

def plot_vertical_lines_offset(stimulus_off_time):
    for ii in xrange(0,np.size(stimulus_off_time)):
        plt.axvline(x=stimulus_off_time[ii], linestyle='--', color='k', linewidth=1)
                
    
def plot_stimulus_in_3d(ax1, ICA_components, stimulus_on_time, stimulus_off_time, color_mat, required_pcs,z_direction):
    
    ## Plot Baseline at beginning
    ax1.plot(ICA_components[0:stimulus_on_time[0],required_pcs[0]], \
    ICA_components[0:stimulus_on_time[0],required_pcs[1]],\
    ICA_components[0:stimulus_on_time[0],required_pcs[2]],  zdir=z_direction,color='#808080', linewidth=3)
    
    print np.shape(ICA_components)
    
    #Plot light on times
    for ii in xrange(0,np.size(stimulus_on_time)):
        ax1.plot(ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[0]], \
        ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[1]],\
        ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[2]],  zdir=z_direction,color=color_mat[ii], linewidth=3)
    
    #Plot light off times
    for ii in xrange(0,np.size(stimulus_on_time)):
        
        if ii == np.size(stimulus_on_time)-1:
#            print ii
            ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[0]], \
            ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[1]],\
            ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[2]],  zdir=z_direction,color=color_mat[ii], linewidth=2, linestyle='--')
        else:

            ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[0]], \
            ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[1]],\
            ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[2]],  zdir=z_direction,color=color_mat[ii], linewidth=2, linestyle='--')
    
    ## Plot Baseline at end of stimulus
    ax1.plot(ICA_components[stimulus_off_time[ii]+20:,required_pcs[0]], \
    ICA_components[stimulus_off_time[ii]+20:,required_pcs[1]],\
    ICA_components[stimulus_off_time[ii]+20:,required_pcs[2]],  zdir=z_direction,color='#000000', linewidth=3)

def plot_stimulus_in_3d_combined_fish(ax1, ICA_components, num_fish_used, stimulus_on, stimulus_off, color_mat, required_pcs, z_direction):
    
    # Initialize soem parameters
    size_stimulus = np.size(stimulus_on)/num_fish_used
    size_time = np.size(ICA_components,0)/num_fish_used
    count = 0
    time_start = 0
    time_end = size_time
    
    for nn in xrange(0, num_fish_used):
        #print some stuff for verification   
        print size_stimulus, size_time, time_end, time_start
        
        #Create a matrix for stimulus on time of individual fish
        stimulus_on_time = stimulus_on[count:count+size_stimulus] 
        stimulus_off_time = stimulus_off[count:count+size_stimulus]
        count += size_stimulus
        
        print stimulus_on_time, stimulus_off_time
        
        ## Plot Baseline
        ax1.plot(ICA_components[time_start:stimulus_on_time[0],required_pcs[0]], \
        ICA_components[time_start:stimulus_on_time[0],required_pcs[1]],\
        ICA_components[time_start:stimulus_on_time[0],required_pcs[2]],\
        color='#808080', linewidth=3+(nn))
            
        for ii in xrange(0,np.size(stimulus_on_time)):
            ax1.plot(ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[0]], \
            ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[1]],\
            ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[2]],\
            color=color_mat[ii], linewidth=3+(nn))
        
        ## Plot Baseline
        ax1.plot(ICA_components[stimulus_off_time[ii]+20:time_end,required_pcs[0]], \
        ICA_components[stimulus_off_time[ii]+20:time_end,required_pcs[1]],\
        ICA_components[stimulus_off_time[ii]+20:time_end,required_pcs[2]],\
        color='#000000', linewidth=3+(nn))
        
        for ii in xrange(0,np.size(stimulus_on_time)):
            if ii == np.size(stimulus_on_time)-1:
                ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[0]], \
                ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[1]],\
                ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[2]],\
                color=color_mat[ii], linewidth=2+(nn), linestyle='--')
            else:
                ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[0]], \
                ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[1]],\
                ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[2]],\
                color=color_mat[ii], linewidth=2+(nn), linestyle='--')
        
        #Create a matric for time start and time end of each fish        
        time_start += time_end
        time_end += time_end+size_time
        
    
def plot_stimulus_in_2d(ax1, ICA_components, stimulus_on_time, stimulus_off_time, color_mat, required_pcs):
    
    ## Plot Baseline
    ax1.plot(ICA_components[0:stimulus_on_time[0],required_pcs[0]], \
    ICA_components[0:stimulus_on_time[0],required_pcs[1]],\
    color='#808080', linewidth=3)
        
    for ii in xrange(0,np.size(stimulus_on_time)):
        ax1.plot(ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[0]], \
        ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[1]],\
        color=color_mat[ii], linewidth=3)
    
    ## Plot Baseline
    ax1.plot(ICA_components[stimulus_off_time[ii]+20:,required_pcs[0]], \
    ICA_components[stimulus_off_time[ii]+20:,required_pcs[1]],\
    color='#000000', linewidth=3)
    
    for ii in xrange(0,np.size(stimulus_on_time)):
        if ii == np.size(stimulus_on_time)-1:
            ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[0]], \
            ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[1]],\
            color=color_mat[ii], linewidth=2, linestyle='--')
        else:
            ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[0]], \
            ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[1]],\
            color=color_mat[ii], linewidth=2, linestyle='--')
    
def plot_stimulus_in_2d_combined_fish(ax1, ICA_components, num_fish_used, stimulus_on, stimulus_off, color_mat, required_pcs):
    
    # Initialize soem parameters
    size_stimulus = np.size(stimulus_on)/num_fish_used
    size_time = np.size(ICA_components,0)/num_fish_used
    count = 0
    time_start = 0
    time_end = size_time
    
    for nn in xrange(0, num_fish_used):
        #print some stuff for verification   
        print size_stimulus, size_time, time_end, time_start
        
        #Create a matrix for stimulus on time of individual fish
        stimulus_on_time = stimulus_on[count:count+size_stimulus] 
        stimulus_off_time = stimulus_off[count:count+size_stimulus]
        count += size_stimulus
        
        print stimulus_on_time, stimulus_off_time
        
        ## Plot Baseline
        ax1.plot(ICA_components[time_start:stimulus_on_time[0],required_pcs[0]], \
        ICA_components[time_start:stimulus_on_time[0],required_pcs[1]],\
        color='#808080', linewidth=3+(nn))
            
        for ii in xrange(0,np.size(stimulus_on_time)):
            ax1.plot(ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[0]], \
            ICA_components[stimulus_on_time[ii]:stimulus_off_time[ii],required_pcs[1]],\
            color=color_mat[ii], linewidth=3+(nn))
        
        ## Plot Baseline
        ax1.plot(ICA_components[stimulus_off_time[ii]+20:time_end,required_pcs[0]], \
        ICA_components[stimulus_off_time[ii]+20:time_end,required_pcs[1]],\
        color='#000000', linewidth=3+(nn))
        
        for ii in xrange(0,np.size(stimulus_on_time)):
            if ii == np.size(stimulus_on_time)-1:
                ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[0]], \
                ICA_components[stimulus_off_time[ii]:stimulus_off_time[ii]+20,required_pcs[1]],\
                color=color_mat[ii], linewidth=2+(nn), linestyle='--')
            else:
                ax1.plot(ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[0]], \
                ICA_components[stimulus_off_time[ii]:stimulus_on_time[ii+1],required_pcs[1]],\
                color=color_mat[ii], linewidth=2+(nn), linestyle='--')
        
        #Create a matric for time start and time end of each fish        
        time_start += time_end
        time_end += time_end+size_time
        
        
    
def legend_for_2d_plot(ax1, stimulus_off_time):
    A = []
    A.append( 'Start')
    for ii in xrange(0,np.size(stimulus_off_time)):
        A.append(str(ii))
    A.append('End')
    
    
    ax1.legend(A, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True)
