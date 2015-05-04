function image_register_combined(Data_Folder, Template_Folder,  Result_Folder, num_stack, count)

%Find files in the folder and remove those that start with . or are folders
files_present = dir([Data_Folder,filesep, '*.tif']);

if count == 1
    time_start = 1;
else
    time_start = length(files_present)*(count-1)+1;
end


%Now register all images using base. Save as multitiff
for zz = 1:num_stack
    
    time_for_saving = time_start;
    base = (imread([Template_Folder, filesep, 'T=1.tif'], zz));
    [yb,xb] = size(base);
    
    for ff = 1:length(files_present)
        
        
        unregistered = (imread([Data_Folder, filesep, 'T=', num2str(ff),'.tif'], zz));
        
        [yc,xc] = size(unregistered);
        
        %If image is not same size as base, resize
        if yc~=yb || xc~=xb
            unregistered = imresize(unregistered, [yb,xb]);
            [yc,xc] = size(unregistered);
        end
        
        c = normxcorr2(base,unregistered); %Calculate correlation between base and unregistered image
        
        %% Register image by calculating shift
        [y,x] = find(c == max(c(:)),1);
        
        %Find offset
        yoff = y - yc;
        xoff = x - xc;
        
        
        disp(['Filename...', 'T=', num2str(ff), ' Stack..', num2str(zz),  ' X offset...', num2str(xoff), ' Y offset...', num2str(yoff)]);
        
        
        if xoff < 0
            xoffa = abs(xoff)+1;
        else
            xoffa = xoff;
        end
        if yoff < 0
            yoffa = abs(yoff)+1;
        else
            yoffa = yoff;
        end
        
        if abs(xoff)>=20 || abs(yoff)>=20
            xoff=0;
            yoff=0;
        end
        
        register_by_offsets(unregistered, Result_Folder, xc, yc, xoffa, yoffa, xoff, yoff, zz, time_for_saving)
        time_for_saving = time_for_saving+1;
        
        
    end
    
end
end



function register_by_offsets(unregistered, Result_Folder, xc, yc, xoffa, yoffa, xoff, yoff, zz, time_for_saving)

% Adjust according to peak correlation
registered = uint16(zeros(yc+abs(yoffa), xc+abs(xoffa)));

if xoff~=0 && yoff==0
    if xoff < 0
        registered(:, xoffa:(xc+xoffa-1)) = unregistered;
        registered(:,end-xoffa+1:end) = [];
    else
        registered(:, 1:xc) = unregistered;
        registered(:,1:xoffa) = [];
    end
elseif xoff==0 && yoff~=0
    if yoff < 0
        registered(yoffa:(yc+yoffa-1), :) = unregistered;
        registered(end-yoffa+1:end,:) = [];
    else
        registered(1:yc, :) = unregistered;
        registered(1:yoffa,:) = [];
    end
elseif xoff~=0 && yoff~=0
    if xoff < 0 && yoff < 0
        registered(yoffa:(yc+yoffa-1), xoffa:(xc+xoffa-1)) = unregistered;
        registered(end-yoffa+1:end,:) = [];
        registered(:,end-xoffa+1:end) = [];
    elseif xoff > 0 && yoff > 0
        registered(1:yc, 1:xc) = unregistered;
        registered(1:yoffa,:) = [];
        registered(:,1:xoffa) = [];
    elseif xoff < 0 && yoff > 0
        registered(1:yc, xoffa:(xc+xoffa-1)) = unregistered;
        registered(1:yoffa,:) = [];
        registered(:,end-xoffa+1:end) = [];
    elseif xoff > 0 && yoff < 0
        registered(yoffa:(yc+yoffa-1), 1:xc) = unregistered;
        registered(end-yoffa+1:end,:) = [];
        registered(:,1:xoffa) = [];
    end
elseif xoff==0 && yoff==0
    registered = (unregistered);
end

% Save images
if zz==1
    imwrite(registered,[Result_Folder, filesep,'T=',int2str(time_for_saving),'.tif'],'tif');
else
    imwrite(registered,[Result_Folder, filesep,'T=',int2str(time_for_saving), '.tif'],'tif','WriteMode','append');
end
end

