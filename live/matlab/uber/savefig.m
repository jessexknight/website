% [] = savefig(savename)
% 
% SAVEFIG saves the current onscreen figure to a .png file exactly as it
%   appears, using imwrite. Other figure export options tend to behave 
%   unexpectedly.
% 
% Jesse Knight 2016

function [] = savefig(savename)
drawnow;
frame = getframe(gcf);
imwrite(frame.cdata,savename,'PNG');

