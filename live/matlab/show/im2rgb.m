function [RGB] = im2rgb(I,map)
N = size(map,1);
[IU,U] = biny(I,[],[1,N],N);
RGB(:,1) = map(IU,1);
RGB(:,2) = map(IU,2);
RGB(:,3) = map(IU,3);
RGB = reshape(RGB,[size(I),3]);

