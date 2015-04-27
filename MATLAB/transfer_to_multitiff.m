function transfer_to_multitiff(Directory_Name, num_stack)

Result_Folder = [Directory_Name, filesep, 'All_Stacks', filesep];

if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end

for ii = 1:num_stack
    Sub_Directory = [Directory_Name, filesep, 'Z=', int2str(ii), filesep, 'Registered', filesep];
    files_present = dir([Sub_Directory,filesep, '*.tif']);
    
    disp(['Moving Stimulus...From Stack', int2str(ii)]);

    %% Loop through images and save as multitiffs of stacks for each timepoint
    for ff = 1:length(files_present)
        
        File_string = files_present(ff).name;
        find_t = strfind(File_string, 't');
        time = str2double(File_string(find_t(2)+1:find_t(2)+3));
        
        image = (imread([Sub_Directory, filesep, File_string]));

        if ii == 1
            imwrite(image,[Result_Folder, filesep, 'T=', int2str(time), '.tif'],'tif');
        else
            imwrite(image,[Result_Folder, filesep,'T=', int2str(time), '.tif'],'tif', 'WriteMode','append');
            
        end
    end
    
end