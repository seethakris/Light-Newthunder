function main_function_for_matlabprocessing

%% Few preprocessing techniques in Matlab can be run using this script
% 1. Register images


Main_Directory_Name = '~/Desktop/Ruey_Habenula/Habenula/Fish104-108/';
num_stack = 5;
Num_fish_to_include = 2;
template_folder = 4;

%Script
Result_Folder = [Main_Directory_Name, filesep, 'Combined_Data', filesep,  'Trial1', filesep];

if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end

if ~isdir([Result_Folder,'Figures/'])
    mkdir([Result_Folder,'Figures/'])
end


subfolders = dir(Main_Directory_Name);
subfolders = subfolders([subfolders.isdir]);
foldernames = struct2cell(subfolders);
foldernames = foldernames(1,:);
[sorted_foldernames, ~] = sort(foldernames);

count = 0;


%% Register data using a single template and combine them
for ii = 1:length(sorted_foldernames)
    if  ~strcmpi(sorted_foldernames{ii}, '.') && ~strcmpi(sorted_foldernames{ii}, '..') && ~strcmpi(sorted_foldernames{ii}, 'Combined_Data')
        
        Directory_Name = [Main_Directory_Name, sorted_foldernames{ii}, filesep, 'All_Stacks', filesep, 'Trial1', filesep];
        Template_Folder = [Main_Directory_Name, sorted_foldernames{template_folder}, filesep, 'All_Stacks', filesep,  'Trial1', filesep];
        count = count+1;
        
        % Plot normalized and combined data
%         fs = plot_normalized_data(Directory_Name, count, num_stack);
        
        Normalized_Directory_Name = [Directory_Name, filesep, 'Normalized_Data',filesep];
        
        %%Dont register and just append to combined folder
        combine_normalized_data(Normalized_Directory_Name, Result_Folder, num_stack, count);
        
        %Register if required
%         image_register_combined(Normalized_Directory_Name, Template_Folder, Result_Folder, num_stack, count);
        
        if count == Num_fish_to_include
            break
        end
        
    end
end

addpath(genpath('/Users/seetha/Desktop/Ruey_Habenula/Habenula/Scripts/MATLAB/export_fig/'));
export_fig(fs, [Result_Folder, 'Figures/mean_normalized_plots.pdf'], '-pdf','-append')
