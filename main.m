clear all
close all
clc

%gp_subdirs = split(genpath('/Users/kenny/Documents/gptoolbox.github'),':');
%addpath(strjoin(gp_subdirs(~contains(gp_subdirs,'.git')),':'));

gptoolbox_paths = '/Users/kenny/Documents/gptoolbox.github:/Users/kenny/Documents/gptoolbox.github/external:/Users/kenny/Documents/gptoolbox.github/external/exactgeodesic:/Users/kenny/Documents/gptoolbox.github/external/exactgeodesic/src:/Users/kenny/Documents/gptoolbox.github/external/matlabPyrTools:/Users/kenny/Documents/gptoolbox.github/external/matlabPyrTools/MEX:/Users/kenny/Documents/gptoolbox.github/external/matlabPyrTools/TUTORIALS:/Users/kenny/Documents/gptoolbox.github/external/matlabPyrTools/TUTORIALS/.AppleDouble:/Users/kenny/Documents/gptoolbox.github/external/matlabPyrTools/TUTORIALS/.FBCLockFolder:/Users/kenny/Documents/gptoolbox.github/external/matlabPyrTools/TUTORIALS/HTML:/Users/kenny/Documents/gptoolbox.github/external/mls:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/data:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/html:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/anisotropic-fm-feth:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/backup:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/fheap:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_core:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_geodesic:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_maths:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_maths/test:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_maths/tnt:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_toolkit:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/mex/gw/gw_toolkit/ply:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/tests:/Users/kenny/Documents/gptoolbox.github/external/toolbox_fast_marching/toolbox:/Users/kenny/Documents/gptoolbox.github/imageprocessing:/Users/kenny/Documents/gptoolbox.github/images:/Users/kenny/Documents/gptoolbox.github/matrix:/Users/kenny/Documents/gptoolbox.github/mesh:/Users/kenny/Documents/gptoolbox.github/mex:/Users/kenny/Documents/gptoolbox.github/mex/cmake:/Users/kenny/Documents/gptoolbox.github/mex/winding_number:/Users/kenny/Documents/gptoolbox.github/quat:/Users/kenny/Documents/gptoolbox.github/utility:/Users/kenny/Documents/gptoolbox.github/wrappers:';

addpath(gptoolbox_paths);

load('data0.mat')
Z = imresize(height, 0.2) / 1000000;  % Kenny: I think we got color data and not height data in this file...
[xdim, ydim] = size(Z);
dx = xsize/(xdim-1);
dy = ysize/(ydim-1);
x = (0:xdim-1)*dx;
y = (0:ydim-1)*dy;
[X,Y] = meshgrid(x,y);
[f,v,~] = surf2patch(surf(X,Y,Z),'triangles'); 
writeOBJ('data0_resized.obj',v,f);
writeSTL('data0_resized.stl',v,f);

load('data1.mat')
Z = imresize(height, 0.2);
[xdim, ydim] = size(Z);
dx = xsize/(xdim-1);
dy = ysize/(ydim-1);
x = (0:xdim-1)*dx;
y = (0:ydim-1)*dy;
[X,Y] = meshgrid(x,y);
[f,v,~] = surf2patch(surf(X,Y,Z),'triangles'); 
writeOBJ('data1_resized.obj',v,f);
writeSTL('data1_resized.stl',v,f);
