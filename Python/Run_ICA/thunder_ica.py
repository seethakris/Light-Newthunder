# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:05:40 2015
Run ICA and get colormaps
@author: seetha
"""

#Import python libraries
from numpy import newaxis, squeeze, size, where, array, mean, zeros, round, reshape, float16, delete
from scipy import stats
from numpy import asarray
import webcolors


#Import thunder libraries
from thunder import ICA
from thunder import Colorize


def run_ICA(data,ICA_components,PCA_components):
    model = ICA(k=PCA_components, c=ICA_components).fit(data)
    imgs = model.sigs.pack()
    

    return model, imgs
    
#Make maps and scatter plots of the ICA scores with colormaps for plotting 
def make_ICA_maps(data,ICA, imgs, img_size_x, img_size_y,  num_ICA_colors, color_map, colors_ica):
    
    reference = data.seriesMean().pack()
    maps = Colorize(cmap=color_map, colors = colors_ica, scale=num_ICA_colors).transform(abs(imgs),background=reference, mixing=0.5)
       
    #Count number of unique colors in the images
    #Get number of planes based on map dimesnions
    if len(maps.shape)==3:
        num_planes = 1
    else:
        num_planes = size(maps,2)
    
    
    unique_clrs = []
    for ii in xrange(0, size(colors_ica)):
        unique_clrs.append( round(array(webcolors.name_to_rgb(colors_ica[ii]), dtype=float)/255))
        
    #From maps get number of pixel matches with color for each plane
    matched_pixels = zeros((size(unique_clrs,0),num_planes))
    array_maps = round(maps.astype(float16))
    matched_pixels = zeros((size(unique_clrs,0),num_planes))
    if len(maps.shape) == 3:
        array_maps_plane = reshape(array_maps, (size(array_maps,0)*size(array_maps,1),3))
        matched_pixels[:,0] = [size(where((array(array_maps_plane) == match).all(axis=1))) for match in unique_clrs]
    else:     
        for ii in xrange(0,num_planes):
            array_maps_plane = reshape(array_maps[:,:,ii,:], (size(array_maps,0)*size(array_maps,1),3))
            matched_pixels[:,ii] = [size(where((array(array_maps_plane) == match).all(axis=1))) for match in unique_clrs]


    
    return maps, matched_pixels, unique_clrs
class structtype():
    pass



