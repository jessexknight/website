% [RGB] = im2rgb(I,map)
% 
% IM2RGB generates an RGB image from the grayscale N-D image I, using the 
%   user- specified colormap map. Note: requires biny function.
% 
% Args:
%   I      - ND array of real-valued data
%   map    - colormap(function or lookup table, not string)
% 
% Returns:
%   RGB    - [size(I),3] size-image with the RGB dimension appended last.
% 
% Jesse Knight 2016

function [RGB] = im2rgb(I,map)
N = size(map,1);
[IU,U] = biny(I,[],[1,N],N);
RGB(:,1) = map(IU,1);
RGB(:,2) = map(IU,2);
RGB(:,3) = map(IU,3);
RGB = reshape(RGB,[size(I),3]);

