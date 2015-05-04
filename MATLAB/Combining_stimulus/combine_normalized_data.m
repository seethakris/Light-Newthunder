function combine_normalized_data(Data_Folder, Result_Folder, num_stack, count)

%Find files in the folder and remove those that start with . or are folders
files_present = dir([Data_Folder,filesep, '*.tif']);

if count == 1
    time_start = 1;
else
    time_start = length(files_present)*(count-1)+1;
end


for zz = 1:num_stack
    
    time_for_saving = time_start;
    
    for ff = 1:length(files_present)
        
        image = (imread([Data_Folder, filesep, 'T=', num2str(ff),'.tif'], zz));
        
        disp(['Saving...', Data_Folder,' Stack..', num2str(zz)]);
        
        % Save images
        if zz==1
            imwrite(image,[Result_Folder, filesep,'T=',int2str(time_for_saving),'.tif'],'tif');
        else
            imwrite(image,[Result_Folder, filesep,'T=',int2str(time_for_saving), '.tif'],'tif','WriteMode','append');
        end
        time_for_saving = time_for_saving+1;
        
    end
end