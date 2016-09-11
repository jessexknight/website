% TIMSHOW is a flexible function for displaying multiple images tightly on the
%         same figure. Padding between images, grid dimensions, contrast scale, 
%         and colourmaps can be specified. Attributes apply to all images. Best
%         results with same sized images. Grayscale or colour images.
% 
% Input arguments: (any order, no string names required, just arguments)
%    image(s)  - any number of 2D grayscale or colour images. Rendered in the
%                order they are presented, top to bottom, left to right. 
%                * The x-dimension of any image should not have a size of 3,
%                  else it will be confused for a colourmap.
% 
%    padval    - decimal value on the interval (0, 0.5) dictating the relative
%                padded spacing between images.
%                Default: 0.005
% 
%    gridstr   - string like "5x2", specifying the number of images to tile
%                horizontally (5) and vertically (2)
%                Default: square as possible based on num. images, wider bias
% 
%    minmax    - minmax specification for contrast scaling, as in imshow(I,[]).
%                array of size: 1 by 2, or a empty array: []. Applies to all
%                images equally.
%                Default: []
% 
%    colourmap - colourmap used for displaying images:
%                array of size: M by 3 or a colourmap function
%                Default: curent default figure colormap
% 
%              * if 2+ non-image arguments are given, only the last one is used.
% 
% Examples:
% 
%    timshow(I1, I2, I3, I4, hot, 0, [0,1], '4x1');
%                Show images I1, I2, I3, I4 using the hot colourmap, with no
%                space between, contrast from 0 to 1, and in a horizontal line.
% 
%    timshow(DB(:).I);
%                Show all image fields .I in the struct array DB using the
%                default figure colourmap, automatic contrast scaling per image,
%                with 0.5% of total figure size padded between, and arranged as
%                close to square as possible.
% 
% Jesse Knight 2016

function [varargout] = timshow(varargin)
[data] = parseargs(varargin);
[data] = initaxes(data);
[data] = showims(data);
if nargout == 1
  varargout{1} = data.ax;
end
  
function [data] = parseargs(vargs)
% default values
data.img       = [];
data.minmax    = [];
data.colourmap = get(0,'defaultfigurecolormap');
data.pad       = 0.005;

% handle input arguments based on dimensions / attributes
for v = 1:numel(vargs)
    sizev = size(vargs{v});
    % padval
    if (numel(sizev) == 2) && (all(sizev == [1,1])) && (vargs{v} < 0.5)
        data.pad = vargs{v};
    % gridstr
    elseif ischar(vargs{v}) && numel(sscanf(vargs{v},'%dx%d')) == 2
        xy = sscanf(vargs{v},'%dx%d');
        data.nSubx = xy(1);
        data.nSuby = xy(2);
    % colourmap
    elseif sizev(2) == 3
        data.colourmap = vargs{v};
    % minmax (numerical)
    elseif (numel(sizev) == 2) && (all(sizev == [1,2]))
        data.minmax = vargs{v};
    % minmax ([])
    elseif sizev(1) == 0
        data.minmax = [];
    % image
    elseif (numel(sizev) == 2) || (numel(sizev) == 3 && sizev(3) == 3)
        data.img(end+1).data  = vargs{v};
        data.img(end).size    = size(data.img(end).data);
    % argument not recognized: ignoring
    else
        warning(['Ignoring argument number ',num2str(v),'.']);
    end
end

function [data] = initaxes(data)
% optimize display grid square-ish if not user specified
data.N = numel(data.img);
if ~all(isfield(data,{'nSubx','nSuby'}))
    data.nSubx = ceil(sqrt(data.N));
    data.nSuby = ceil(data.N/data.nSubx);
end
% subplot handles initialization
for a = 1:data.N
    data.ax(a) = subplot(data.nSuby,data.nSubx,a);
end
% optimize figure display size for the current monitor and first image size
% centres the figure in onscreen too.
screensize = get(0,'screensize');
aspect     = (size(data.img(1).data,1) / size(data.img(1).data,2));
imgSize = min(800, (0.4*screensize(3)) / data.nSubx);
set(gcf,'color','k','position',...
   [(screensize(3) - (imgSize*data.nSubx))/2,... % Lower-left corner X
    (screensize(4) - (imgSize*data.nSuby))/2,... % Lower-left corner Y
    (imgSize*data.nSubx),...                     % Width in X
    (imgSize*data.nSuby*aspect)]);               % Width in Y
 
function [data] = showims(data)
% show the images in default subplot locations
for i = 1:data.N
    imshow(data.img(i).data,data.minmax,'parent',data.ax(i));
end
% set the positions of the axes
% (must be done after due to axes disappearing if they overlap)
for i = 1:data.N
    y = ceil(i / data.nSubx);
    x = mod(i, data.nSubx);
    x(~x) = data.nSubx;
    set(data.ax(i),'position',[(x - 1) / data.nSubx + 0.5*data.pad,  ...
                                1 - (y / data.nSuby - 0.5*data.pad), ...
                                     1 / data.nSubx - data.pad,      ...
                                     1 / data.nSuby - data.pad]);
end
% apply colourmap
colormap(data.colourmap);
