function main_function_for_matlabpreprocessing

%% Few preprocessing techniques in Matlab can be run using this script
% 1. Convert nd2 files to tiff using BioFormats reader for Matlab
% 2. Register images
% 3. Sort into stimulus folders for thunderization


Main_Directory_Name = '~/Desktop/Ruey_Habenula/Habenula/Data/';
num_stack = 5;

subfolders = dir(Main_Directory_Name);
subfolders = subfolders([subfolders.isdir]);
foldernames = struct2cell(subfolders);
foldernames = foldernames(1,:);
[sorted_foldernames, ~] = sort(foldernames);


for ii = 1:length(sorted_foldernames)
    if  ~strcmpi(sorted_foldernames{ii}, '.') && ~strcmpi(sorted_foldernames{ii}, '..')
        for jj = 1:num_stack
            Directory_Name = [Main_Directory_Name, sorted_foldernames{ii}, filesep, 'Z=', int2str(jj)];
            
            %% Normalize Images
            
            %% Register images
            disp(['Registering images....for ', Directory_Name])
            image_register(Directory_Name)
            
        end
        
        %%Find images from each stack and combine the multitiffs together
        %%for thunderization
        
        Sub_Directory = [Main_Directory_Name, sorted_foldernames{ii}];
        disp(['Sorting sitmulus folders....for ', Sub_Directory])
        transfer_to_multitiff(Sub_Directory, num_stack)
    end
end