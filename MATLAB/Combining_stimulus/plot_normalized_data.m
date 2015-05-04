function fs = plot_normalized_data(Data_Folder, count, num_stack)

%% Normlize data from all fish, plot and save
Result_Folder = [Data_Folder, filesep, 'Normalized_Data',filesep];

if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end


color_mat = ['b','r','g', 'm', 'c','y'];

files_present = dir([Data_Folder,filesep, '*.tif']);

for zz = 1:num_stack
    A = zeros(512,512,311);
    C1 = zeros(512,512,311);
    
    for ff = 1:length(files_present)
        A(:,:,ff) = (imread([Data_Folder, filesep, 'T=', num2str(ff),'.tif'], zz));
    end
    
    A1 = im2double(A);
    B1 = mean(A1,3);
    B2 = (std(A1, [], 3)+0.1);
    
    %Zscore
    disp(['Normalizing...',Data_Folder,' Stack..', num2str(zz)]);
    
    for ii = 1:length(files_present)
        C1(:,:,ii) = (A1(:,:,ii)-B1)./B2;
    end
    
    %Remove NaNs
    C1(isnan(C1)) = 0;
    C2 = reshape(C1, size(C1,1)*size(C1,2), size(C1,3)); %Reshape and get mean
    
    C2_mean = mean(C2,1);
    
    %Plot zscores
    fs = figure(1);
    subplot(2,3,zz)
    title(['Z=',num2str(zz)])
    set(fs, 'color','white', 'visible','on')
    hold on
    plot(C2_mean, 'color',color_mat(count))
    xlim([0,311])
    
    
    for ii = 1:length(files_present)
        %Save as 16 bit images
        C1_uint8 = uint8(round(C1(:,:,ii)*255));
        
        if zz == 1
            imwrite(C1_uint8,[Result_Folder, filesep,'T=',int2str(ii), '.tif'],'tif');
        else
            imwrite(C1_uint8,[Result_Folder, filesep,'T=',int2str(ii), '.tif'],'tif', 'WriteMode','append');
        end
    end
    
end