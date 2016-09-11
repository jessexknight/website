function [cmap] = spiderman(m)
% colormap: blue-black-red (for difference images)
if nargin < 1
   m = size(get(gcf,'colormap'),1);
end
n = fix(m/2)-1;
r = [zeros(1,n+2) (1:+1:n)/n]';
g = zeros(1,m)';
b = [(n:-1:1)/n zeros(1,n+2)]';
cmap = [r,g,b];
