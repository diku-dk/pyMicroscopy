function [] = mat2obj( scale, input_file, output_file)

    gp_subdirs = split(genpath('/Users/nlp442/Documents/GitHub/gptoolbox'),':');
    addpath(strjoin(gp_subdirs(~contains(gp_subdirs,'.git')),':'));

    load(input_file)
    Z = imresize(height, scale);
    [xdim, ydim] = size(Z);
    dx = xsize/(xdim-1);
    dy = ysize/(ydim-1);
    x = (0:xdim-1)*dx;
    y = (0:ydim-1)*dy;
    [X,Y] = meshgrid(x,y);
    [f,v,~] = surf2patch(surf(X,Y,Z),'triangles'); 
    writeOBJ(output_file,v,f);

end


