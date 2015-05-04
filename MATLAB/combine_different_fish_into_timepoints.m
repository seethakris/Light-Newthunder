function combine_different_fish_into_timepoints

%% Take files from seperate fish and combine them to do a PCA

% User Input
Main_Directory_Name = '/Users/seetha/Desktop/Ruey_Habenula/Habenula/Short_Stimulus/';

%Number of fish to be included.
Num_fish_to_include = 2;


Result_Folder = [Main_Directory_Name, 'Combined_Data', filesep];

if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end



subfolders = dir(Main_Directory_Name);
subfolders = subfolders([subfolders.isdir]);
foldernames = struct2cell(subfolders);
foldernames = foldernames(1,:);
[sorted_foldernames, ~] = sort(foldernames);

count = 0; 
for ii = 1:length(sorted_foldernames)
    if  ~strcmpi(sorted_foldernames{ii}, '.') && ~strcmpi(sorted_foldernames{ii}, '..') && ~strcmpi(sorted_foldernames{ii}, 'Combined_Data')
        Directory_Name = [Main_Directory_Name, sorted_foldernames{ii}, filesep, 'All_Stacks', filesep];
        count = count+1;
        
        %Find files and copy to respective folders
        files_present = dir([Data_Folder,filesep, '*.tif']);
        
        if count == 1
            for jj = 1:length(files_present)
                copyfile([Directory_Name, files_present(jj).name], [Result_Folder, ]);
            end
        else
            
        end
        
        if count == Num_fish_to_include
            break
        end
    end
end
